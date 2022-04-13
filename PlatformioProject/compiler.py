import sys
import secrets
from lex import lex
from typing import *
from interpreter import InterpretType, functionalDictAdd
from AST import Expression, Variable, Value, Loop, Function, Call, If, parse, ASTType

sys.setrecursionlimit(20000)  # core dumped at 21804


Register        = str                           # Register strings
VariableName    = str                           # Variable name string
AsmCode         = str                           # Assembly code as string
DataSegmentType = Dict[str, str]                # Key and content of a string data segment
CompMemType     = Dict[VariableName, Register]  # 

# beginFile :: DataSegmentType -> str -> str 
def beginFile(dataSegment: DataSegmentType = "", fileName: str = "") -> str:
    """Formats the top part of an assembly file, inserts the .data segment and the function/file name"""
    return f".cpu cortex-m0\n.align 2\n\n{dataSegment}.text\n.global {fileName}\n\n{fileName}:\n"

# getRegister :: [Register] -> CompMemType -> Register
def getRegister(allRegisters: List[Register], memory: CompMemType) -> Register:
    """Returns the lowest register without anything stored in it"""
    return [x for x in allRegisters if x.lower() not in memory.values() and x.upper() not in memory.values()][0]


# puts an inline value in r0
# valueToR0 :: Value -> CompMemType -> (AsmCode, CompMemType)
def valueToR0(value: Value, memory: CompMemType) -> Tuple[AsmCode, CompMemType]:
    """Moves a Value into r0, returns both the necessary assembly code and the new memory
    Depending on the size of the value uses oad register instead"""
    register = "r0"
    func, sign = ("mov", "#") if value.content < 256 else ("ldr", "=")
    assembly = f"{func} {register}, {sign}{value.content}\n"
    return assembly, memory


# stringToRegister :: Value -> DataSegmentType -> Register -> (AsmCode, DataSegmentType)
def stringtoRegister(value: Value, data: DataSegmentType, register: Register = "r0") -> Tuple[AsmCode, DataSegmentType]:
    """Adds string to data segment that goes at the top of the file and puts data pointer in the given register
    Returns needed assembly code to load the data and new data segment"""
    key = f"LIT{len(data)}"
    assembly = f"ldr {register}, ={key}\n"
    return assembly, functionalDictAdd(data, {key:value.content})


# intToRegister :: Value -> Register -> AsmCode
def intToRegister(value: Value, register: Register="r0") -> AsmCode:
    """Adds an interger to given register
    Returns needed assembly code to load an interger
    depending on the size of the interger uses load register instead"""
    content = int(value.content)
    func, sign = ("mov", "#") if content < 256 else ("ldr", "=")
    assembly = f"{func} {register}, {sign}{content}\n"
    return assembly


# showHelper :: Value | Variable -> CompMemType -> DataSegmentType -> (AsmCode, CompMemType, DataSegmentType)
def showHelper(arg: Union[Value, Variable], memory: CompMemType, data: DataSegmentType) -> Tuple[AsmCode, CompMemType, DataSegmentType]:
    """Helper function for printing
    Loads value into r0 and branches to smartPrint which is found in a premade print.S file in /src
    Returns needed assembly code, new memory and new data segment if a string was used"""
    match arg:
        case Variable(name): # In case of a variable move said Variable to R0 to be printed
            register = memory[name]
            return f"mov r0, {register}\nbl smartPrint\n", memory, data
        case Value(content):# in case of a string load the string into R0 to be printed
            if '"' in content:
                assembly, newdata = stringtoRegister(arg, data)
                return assembly+"bl smartPrint\n", memory, newdata
            assembly = intToRegister(arg)
            return assembly+"bl smartPrint\n", memory, data

# compileShow :: Expression -> CompMemType -> DataSegmentType -> (AsmCode, CompMemType, DataSegmentType)
def compileShow(compExp: Expression, memory: CompMemType, data: DataSegmentType) -> Tuple[AsmCode, CompMemType, DataSegmentType]:
    """Compiles show Expression to assembly code
    Returns needed assembly code, new memory and new data segment if a string was used"""
    assembly, memory2, data2 = showHelper(compExp.args[0], memory, data)
    if rest := compExp.args[1:]:
        assembly2, memory3, data3 = compileShow(
            Expression("show", len(rest), rest), memory2, data2)
        return assembly+assembly2, memory3, data3
    return assembly, memory2, data2


# compilemake :: Expression -> CompMemType -> DataSegmentType -> [Register] -> (AsmCode, CompMemType, DataSegmentType)
def compileMake(compExp: Expression, memory: CompMemType, data: DataSegmentType, allRegisters: List[Register]) -> Tuple[AsmCode, CompMemType, DataSegmentType]:
    """Compiles Make Expression (assignment) to assembly code
    Returns needed assembly code, new memory and new data segment"""
    register = getRegister(allRegisters, memory)
    newmemory = functionalDictAdd(memory, {compExp.args[0].name:register})
    if len(compExp.args) < 3:
        if type(compExp.args[1]) == Value:
            if type(compExp.args[1].content) == str:
                assembly, newdata = stringtoRegister(
                    compExp.args[1], data, register)
                return assembly, newmemory, newdata
            else:
                func, sign = ("mov", "#") if compExp.args[1].content < 256 else (
                    "ldr", "=")
                immed = sign + str(compExp.args[1].content)
                return f"{func} {register}, {immed}\n", newmemory, data
        else:
            return f"mov {newmemory[compExp.args[0].name]}, {newmemory[compExp.args[1].name]}\n", newmemory, data
    else:
        return f"mov {register}, r{compExp.args[2].content}\n", newmemory, data

# loadComparison :: Variable | Value -> CompMemType -> Register -> AsmCode
def loadComparison(arg: Union[Variable, Value], memory: CompMemType, register: Register="r0") -> AsmCode:
    """Returns the needed assembly to load the LHS/RHS of a comparison into 'r0' and 'r1'"""
    match arg:
        case Variable(name): return f"mov {register}, {memory[name]}\n"
        case Value(_): return intToRegister(arg, register)

# compileComparison :: Loop | If -> CompMemType -> AsmCode
def compileComparison(compExp: Union[Loop,If], memory: CompMemType) -> AsmCode:
    """Compiles the comparison of a loop or an If expression to assembly code"""
    # load lhs
    lhsAssem = loadComparison(compExp.LHS, memory)
    # load rhs
    rhsAssem = loadComparison(compExp.RHS, memory, "r1")
    return lhsAssem + rhsAssem + "cmp r0, r1\n"

# compileIf :: If -> CompMemType -> DataSegmentType -> (AsmCode, CompMemType, DataSegmentType)
def compileIf(compExp: If, memory: CompMemType, data: DataSegmentType) -> Tuple[AsmCode, CompMemType, DataSegmentType]:
    """Compiles an If statement to assembly code
    Returns the needed assembly code, the new memory and new datasegment type"""
    comparison = compileComparison(compExp, memory)
    body, memory, data = compile(compExp.body, memory, data)
    # Generate random code to link begin and end of if statement
    ifHex = secrets.token_hex(5)
    ifEnd = f"ifEnd_{ifHex}"
    assembly = f"{comparison}bne {ifEnd}\n{body}{ifEnd}:\n"
    return assembly, memory, data

# compileLoop :: Loop -> CompMemType -> DataSegmentType -> (AsmCode, CompMemType, DataSegmentType)
def compileLoop(compExp: Loop, memory: CompMemType, data: DataSegmentType) -> Tuple[AsmCode, CompMemType, DataSegmentType]:
    """Compiles a loop to assembly code 
    Returns the needed assembly code, memory and datasegment"""
    comparison = compileComparison(compExp, memory)
    body, memory, data = compile(compExp.body, memory, data)
    # Generate random code to link begin and end of loop
    whileHex = secrets.token_hex(5)
    whileEnd = f"whileEnd_{whileHex}"
    whileBegin = f"whileBegin_{whileHex}"
    branch = f"beq {whileEnd}\n"
    assembly = f"{whileBegin}:\n{comparison}{branch}{body}b {whileBegin}\n{whileEnd}:\n"
    return assembly, memory, data

# compileDefinition :: Function -> None
def compileDefinition(compExp: Function) -> None:
    """Starts a new compiler to compile a function definition which is put in a seperate assembly file"""
    mainCompiler(compExp.name, compExp.body)

def loadArg(arg: Union[Variable, Value], register: Register, memory: CompMemType, data: DataSegmentType, allRegisters: List[Register]) -> Tuple[AsmCode, CompMemType, DataSegmentType]:
    match arg:
        case Value(_):
            if '"' in arg.content:
                argument, newdata = stringtoRegister(arg, data)
                return argument, memory, newdata
            else:
                argument = intToRegister(arg)
        case Variable(name):
            argument = f"mov {register}, {memory[name]}\n"
    return argument, memory, data

# compileCall :: Call -> CompMemType -> DataSegmentType -> [Register] -> (AsmCode, CompMemType, DataSegmentType)
def compileCall(compExp: Call, memory: CompMemType, data: DataSegmentType, allRegisters: List[Register]) -> Tuple[AsmCode, CompMemType, DataSegmentType]:
    """Compiles a function call by loading the parameters into temp registers, branching and moving the result into a new register"""
    if compExp.argCount <= 4:
        registers = ["r0", "r1", "r2", "r3"]
        ArgTuples = list(zip(compExp.args[:compExp.argCount], registers[:compExp.argCount]))
        arguments = "".join([loadArg(*x, memory, data, allRegisters)[0] for x in ArgTuples])
    else:
        return  
    if compExp.result:
        register = getRegister(allRegisters, memory)
        newmemory = functionalDictAdd(memory, {compExp.result:register})
        resultAssembly = f"mov {register}, r0\n"
    else:
        newmemory = {}
        resultAssembly = ""
    callAssembly = f"bl {compExp.name}\n"
    if newmemory:
        returnMemory = newmemory
    else:
        returnMemory = memory
    return f"{arguments}{callAssembly}{resultAssembly}", returnMemory, data

# compiledivide :: Expression -> CompMemType -> AsmCode
def compileDivide(compExp: Expression, memory: CompMemType) -> AsmCode:
    """compiles a Divide (division) statement"""
    # load lhs
    lhsAssem = loadComparison(compExp.args[0], memory)
    # load rhs
    rhsAssem = loadComparison(compExp.args[1], memory, "r1")
    return lhsAssem + rhsAssem + "bl divide\n" + f"mov {memory[compExp.args[0].name]}, r0\n"
    

# compileExpression :: InterpretType -> CompMemType -> DataSegmentType -> (AsmCode, CompMemType, DataSegmentType)
def compileExpression(compExp: InterpretType, memory: CompMemType, data: DataSegmentType) -> Tuple[AsmCode, CompMemType, DataSegmentType]:
    """Compile the Expression with the correct compile function into assembly code"""
    allRegisters = ["r4", "r5", "r6", "r7", "r8", "r9", "r10", "r11"]
    funcToAssem = {"times": "mul", "plus": "add", "minus": "sub"}
    match compExp:
        case If(_, _, _):
            return compileIf(compExp, memory, data)#, memory, data
        case Loop(_, _, _):
            return compileLoop(compExp, memory, data)#, memory, data
        case Function(_, _):
            compileDefinition(compExp)
            return f"@definition of {compExp.name} was performed\n", memory, data
        case Call(_, _, _, _):
            return compileCall(compExp, memory, data, allRegisters)
        case Expression(a, _, _) if a in funcToAssem.keys():
            if type(compExp.args[1]) == Value:
                memAssem, memory = valueToR0(
                    compExp.args[1], memory)
                snd = "r0"
            else:
                memAssem = ""
                snd = memory[compExp.args[1].name]
            # "memory" will store the location of the data, so a register name or a memory address
            return memAssem + f"{funcToAssem[a]} {memory[compExp.args[0].name]}, {memory[compExp.args[0].name]}, {snd}\n", memory, data
        case Expression("make", _, _):
            return compileMake(compExp, memory, data, allRegisters)
        case Expression("show",_ ,_):
            return compileShow(compExp, memory, data)
        case Expression("divide", _,_):
            return compileDivide(compExp, memory), memory, data
        case _:
            print(":(")
            return

# compileData :: DataSegmentType -> str
def compileData(data: DataSegmentType) -> str:
    """Compile/Format the datasegment of strings that will be pasted at the top of the assembly file"""
    dataSegment = [f"{key}: .asciz {value}\n" for key, value in data.items()]
    if dataSegment:
        return ".data\n\n" + "".join(dataSegment) + "\n"
    return ""

# compile :: ASTTYPE -> CompMemType -> DataSegmentType -> (AsmCode, CompMemType, DataSegmentType)
def compile(ast: ASTType, memory: CompMemType = {}, data: DataSegmentType = {}) -> Tuple[AsmCode, CompMemType, DataSegmentType]:
    """Compiles the AST and the Expressions it contains into assembly code, memory and data segment"""
    if not memory:
        memory = {}
    assembly, memory2, data2 = compileExpression(ast[0], memory, data)
    if rest := ast[1:]:
        assembly2, memory3, data3 = compile(rest, memory2, data2)
        return assembly+assembly2, memory3, data3
    return assembly, memory2, data2

# mainCompiler -> str -> ASTType -> None
def mainCompiler(fileName: str, ast: ASTType = []) -> None:
    """Main Compiler function that writes compiled code to the assembly files
    Calls all functions and keeps track of registers and data 
    Result is the main assembly file and all functions call in the main compiled into assembly as well"""
    if not ast:
        ast = parse(lex(f"{fileName}.sco"))
    compiledCode, memory, data = compile(ast, {}, {})

    entryList = memory.keys()
    if "result" in entryList:
        result = memory["result"]
        returnStatement = f"mov r0, {result}\n"
    else:
        returnStatement = ""

    registerList = memory.values()
    exceptedRegisters = ["r0", "r1", "r2", "r3"]
    popPushRegisters = sorted([x for x in registerList if x not in exceptedRegisters])
    popPushRegisterString = ", ".join(popPushRegisters)
    if popPushRegisterString:
        push = "push { " + popPushRegisterString + ", lr }\n"
        pop = "pop { " + popPushRegisterString + ", pc }\n"
    else:
        push = "push { lr }\n"
        pop = "pop { pc }\n"

    dataSegment = compileData(data)
    fileBegin = beginFile(dataSegment, fileName)
    with open(f"src/{fileName}.S", 'w') as f:
        f.write(fileBegin + push + compiledCode + returnStatement + pop)

