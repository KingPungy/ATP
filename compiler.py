import sys
import secrets
from lex import lex
from typing import *
from interpreter import InterpretType
from AST import Expression, Variable, Value, Loop, Function, Call, If, parse, ASTType

sys.setrecursionlimit(20000)  # core dumped at 21804

Register        = str
VariableName    = str
AsmCode         = str
DataSegmentType = Dict[str, str]
CompMemType     = Dict[VariableName, Register]

def beginFile(dataSegment: DataSegmentType = "", fileName: str = "") -> str:
    return f".cpu cortex-m0\n.align 2\n\n{dataSegment}.text\n.global {fileName}\n\n{fileName}:\n"


def getRegister(allRegisters: List[Register], memory: CompMemType) -> List[Register]:
    return [x for x in allRegisters if x.lower() not in memory.values() and x.upper() not in memory.values()][0]


# puts an inline value in an available register
def valueToRegister(value: Value, memory: CompMemType, allRegisters: List[Register]) -> Tuple[AsmCode, CompMemType]:
    register = "r0"
    func, sign = ("mov", "#") if value.content < 256 else ("ldr", "=")
    assembly = f"{func} {register}, {sign}{value.content}\n"
    return assembly, memory


def stringtoRegister(value: Value, data: DataSegmentType, register: Register = "r0") -> Tuple[AsmCode, DataSegmentType]:
    key = f"LIT{len(data)}"
    data[key] = value.content
    assembly = f"ldr {register}, ={key}\n"
    return assembly, data


def intToRegister(value: Value, register: Register="r0") -> AsmCode:
    content = int(value.content)
    func, sign = ("mov", "#") if content < 256 else ("ldr", "=")
    assembly = f"{func} {register}, {sign}{content}\n"
    return assembly


def ShowHelper(arg: Union[Value, Variable], memory: CompMemType, data: DataSegmentType) -> Tuple[AsmCode, CompMemType, DataSegmentType]:
    match arg:
        case Variable(name):
            register = memory[name]
            if register[0].isupper():  # again quite hacky, but very useful
                func = "smartPrint"
            else:
                func = "smartPrint"
            return f"mov r0, {register}\nbl {func}\n", memory, data
        case Value(content):
            if '"' in content:
                assembly, data = stringtoRegister(arg, data)
                return assembly+"bl smartPrint\n", memory, data
            assembly = intToRegister(arg)
            return assembly+"bl smartPrint\n", memory, data


def compileShow(toCompile: Expression, memory: CompMemType, data: DataSegmentType) -> Tuple[AsmCode, CompMemType, DataSegmentType]:
    assembly, memory, data = ShowHelper(toCompile.args[0], memory, data)
    assembly2 = ""
    if rest := toCompile.args[1:]:
        assembly2, memory, data = compileShow(
            Expression("show", len(rest), rest), memory, data)
    return assembly+assembly2, memory, data

# Returns string of assembly needed for this statement


def compileMake(toCompile: Expression, memory: CompMemType, data: DataSegmentType, allRegisters: List[Register]) -> Tuple[AsmCode, CompMemType, DataSegmentType]:
    if len(toCompile.args) < 3:
        if type(toCompile.args[1]) == Value:
            register = getRegister(allRegisters, memory)
            if type(toCompile.args[1].content) == str:
                # this is really shitty, but the capital R denotes a register holding a string
                memory[toCompile.args[0].name] = register.upper()
                assembly, data = stringtoRegister(
                    toCompile.args[1], data, register.upper())
                return assembly, memory, data
            else:
                memory[toCompile.args[0].name] = register
                func, sign = ("mov", "#") if toCompile.args[1].content < 256 else (
                    "ldr", "=")
                immed = sign + str(toCompile.args[1].content)
                return f"{func} {register}, {immed}\n", memory, data
        else:
            return f"mov {memory[toCompile.args[0].name]}, {memory[toCompile.args[1].name]}\n", memory, data
    else:
        register = getRegister(allRegisters, memory)
        memory[toCompile.args[0].name] = register
        return f"mov {register}, r{toCompile.args[2].content}\n", memory, data


def loadNameIfComponent(arg: Union[Variable, Value], memory: CompMemType, register: Register="r0") -> AsmCode:
    match arg:
        case Variable(name): return f"mov {register}, {memory[name]}\n"
        case Value(_): return intToRegister(arg, register)


def compileComparison(toCompile: If, memory: CompMemType) -> AsmCode:
    # load lhs
    lhsAssem = loadNameIfComponent(toCompile.LHS, memory)
    # load rhs
    rhsAssem = loadNameIfComponent(toCompile.RHS, memory, "r1")
    return lhsAssem + rhsAssem + "cmp r0, r1\n"


def compileIf(toCompile: If, memory: CompMemType, data: DataSegmentType) -> Tuple[AsmCode, CompMemType, DataSegmentType]:
    comparison = compileComparison(toCompile, memory)
    body, _, _ = compile(toCompile.body, memory, data)
    ifHex = secrets.token_hex(5)
    ifEnd = f"ifEnd_{ifHex}"
    assembly = f"{comparison}bne {ifEnd}\n{body}{ifEnd}:\n"
    return assembly, memory, data


def compileWhileComparison(toCompile: Loop, memory: CompMemType) -> AsmCode:
    # load variable
    lhsAssem = loadNameIfComponent(toCompile.Variable, memory)
    # load value
    rhsAssem = loadNameIfComponent(toCompile.Value, memory, "r1")
    return lhsAssem + rhsAssem + "cmp r0, r1\n"


def compileLoop(toCompile: Loop, memory: CompMemType, data: DataSegmentType) -> Tuple[AsmCode, CompMemType, DataSegmentType]:
    comparison = compileWhileComparison(toCompile, memory)
    body, _, _ = compile(toCompile.body, memory, data)
    whileHex = secrets.token_hex(5)
    whileEnd = f"whileEnd_{whileHex}"
    whileBegin = f"whileBegin_{whileHex}"
    branch = f"beq {whileEnd}\n"
    assembly = f"{whileBegin}:\n{comparison}{branch}{body}b {whileBegin}\n{whileEnd}:\n"
    return assembly, memory, data


def compileDefinition(toCompile: Function) -> None:
    mainCompiler(toCompile.name, toCompile.body)


def compileCall(toCompile: Call, memory: CompMemType, data: DataSegmentType, allRegisters: List[Register]) -> Tuple[AsmCode, CompMemType, DataSegmentType]:
    argument1 = ""
    if toCompile.argc >= 1:
        match toCompile.args[0]:
            case Value(_):
                if '"' in toCompile.args[0].content:
                    argument1, data = stringtoRegister(toCompile.args[0], data)
                else:
                    argument1 = intToRegister(toCompile.args[0])
            case Variable(name):
                argument1 = f"mov r0, {memory[name]}\n"
    if toCompile.result:
        register = getRegister(allRegisters, memory)
        memory[toCompile.result] = register
        resultAssembly = f"mov {register}, r0\n"
    else:
        resultAssembly = ""
    callAssembly = f"bl {toCompile.name}\n"
    print(f"{argument1}{callAssembly}{resultAssembly}")
    return f"{argument1}{callAssembly}{resultAssembly}", memory, data

def compileDivide(toCompile: Expression, memory: CompMemType) -> AsmCode:
    # load lhs
    lhsAssem = loadNameIfComponent(toCompile.args[0], memory)
    # load rhs
    rhsAssem = loadNameIfComponent(toCompile.args[1], memory, "r1")
    return lhsAssem + rhsAssem + "bl divide\n"
    


def compileExpression(toCompile: InterpretType, memory: CompMemType, data: DataSegmentType) -> Tuple[AsmCode, CompMemType, DataSegmentType]:
    allRegisters = ["r4", "r5", "r6", "r7", "r8", "r9", "r10", "r11", "r12"]
    funcToAssem = {"times": "mul", "plus": "add", "minus": "sub"}
    match toCompile:
        case If(_, _, _):
            return compileIf(toCompile, memory, data)
        case Loop(_, _, _):
            return compileLoop(toCompile, memory, data)
        case Function(_, _):
            compileDefinition(toCompile)
            return f"@definition of {toCompile.name} was performed\n", memory, data
        case Call(_, _, _, _):
            return compileCall(toCompile, memory, data, allRegisters)
        case Expression(a, _, _) if a in funcToAssem.keys():
            if type(toCompile.args[1]) == Value:
                memAssem, memory = valueToRegister(
                    toCompile.args[1], memory, allRegisters)
                snd = "r0"
            else:
                memAssem = ""
                snd = memory[toCompile.args[1].name]
            # "memory" will store the location of the data, so a register name or a memory address
            return memAssem + f"{funcToAssem[a]} {memory[toCompile.args[0].name]}, {memory[toCompile.args[0].name]}, {snd}\n", memory, data
        case Expression("make", _, _):
            return compileMake(toCompile, memory, data, allRegisters)
        case Expression("show",_ ,_):
            return compileShow(toCompile, memory, data)
        case Expression("divide", _,_):
            return compileDivide(toCompile, memory), memory, data
        case _:
            print(":(")
            return


def compileData(data: DataSegmentType) -> str:
    bruh = [f"{key}: .asciz {value}\n" for key, value in data.items()]
    if bruh:
        return ".data\n\n" + "".join(bruh) + "\n"
    return ""


def compile(ast: ASTType, memory: CompMemType = {}, data: DataSegmentType = {}) -> Tuple[AsmCode, CompMemType, DataSegmentType]:
    if not memory:
        memory = {}
    assembly, memory, data = compileExpression(ast[0], memory, data)
    assembly2 = ""
    if rest := ast[1:]:
        assembly2, memory, data = compile(rest, memory, data)
    return assembly+assembly2, memory, data


def mainCompiler(fileName: str, ast: ASTType = []) -> None:
    if not ast:
        ast = parse(lex(f"{fileName}"))
    compiledCode, memory, data = compile(ast, {}, {})
    registerList = memory.values()
    exceptedRegisters = ["r0", "r1", "r2", "r3"]
    popPushRegisters = sorted([x for x in registerList if x not in exceptedRegisters])
    popPushRegisterString = ", ".join(popPushRegisters)

    entryList = memory.keys()
    if "result" in entryList:
        result = memory["result"]
        returnStatement = f"mov r0, {result}\n"
    else:
        returnStatement = ""

    push = "push { " + popPushRegisterString + ", lr }\n"
    pop = "pop { " + popPushRegisterString + ", pc }\n"
    dataSegment = compileData(data)
    fileBegin = beginFile(dataSegment, fileName)
    with open(f"{fileName}.S", 'w') as f:
        f.write(fileBegin + push + compiledCode + returnStatement + pop)
