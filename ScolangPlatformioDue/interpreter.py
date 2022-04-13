from collections import *
from AST import Expression, Variable, Value, Loop, Function, Call, If, ASTType
import operator as op
from typing import *

# Dictionary of variables and Expressions with their variables
MemType = Dict[str, Union[str, int, List[Union[Function, Call, If, Loop, Expression]], List[Union[str, int]]]]
InterpretType = Union[If, Loop, Call, Function, Expression]


# functionalDictAdd :: Dict -> Dict -> Dict
def functionalDictAdd(Dict: Dict, newEntry: Dict) ->  Dict:
    """Add the values of a dict to an existing dict, without changing state of the program"""
    return {**{ k : Dict[k] for k in set(Dict) - set(newEntry) }, **newEntry}
   

def IfLoopConditionArgExtractor(x: Union[Variable, Value], memory: MemType):
    """Returns a the value of a number or variable depending on what is present"""
    return int(x.content) if type(x) == Value else int(memory[x.name])


# interpretLoop :: InterpretType -> MemType -> MemType
def interpretLoop(expr: InterpretType, memory: MemType) -> MemType:
    """Interprets the body of the loop until the condition is fullfilled and returns new memory"""
    LHS = IfLoopConditionArgExtractor(expr.LHS, memory)
    RHS = IfLoopConditionArgExtractor(expr.RHS, memory)
    if LHS != RHS:
        newmemory = interpret(expr.body, memory)
        return interpretLoop(expr, newmemory)
    else:
        return memory

# interpretIf :: If -> MemType -> MemType
def interpretIf(expr: If, memory: MemType) -> MemType:
    """Interpret an If Expression and return new memory"""
    LHS = IfLoopConditionArgExtractor(expr.LHS, memory)
    RHS = IfLoopConditionArgExtractor(expr.RHS, memory)
    if LHS == RHS:
        return interpret(expr.body, memory)
    else:
        return memory

# interpretCall :: Call -> MemType -> MemType
def interpretCall(expr: Call, memory: MemType) -> MemType:
    """
    Interprets a function call and returns the memory after executing the function
    """
    if expr.name in memory:
        args = {"args" : list(map(lambda x: x.content if type(x) == Value else memory[x.name], expr.args))}
        tmp = dict(filter(lambda x: type(x[1]) == list and x[0] != "args", memory.items()))
        args = {**args, **tmp}
        temp = interpret(memory[expr.name], args)
        # checks for the name of the returnVar
        if expr.result != None: 
            # add the result value to the main memory assigned return variable
            return functionalDictAdd(memory, {expr.result : temp[k] for k in temp.keys() if k == "result"})
        return memory
    else:
        raise Exception("Unknown function. Define First: %s"% expr.name)

# interpretMake :: Expression -> MemType -> MemType
def interpretMake(expr: Expression, memory: MemType) -> MemType:
    """
    Interprets an assignment Expression and returns the new memory with either a new variable or the given variable with altered content
    """
    if expr.argCount == 2:
        if type(expr.args[1]) == Value:
            return functionalDictAdd(memory, {expr.args[0].name : expr.args[1].content})
        elif type(expr.args[1]) == Variable:
            if type(memory[expr.args[0].name]) == type(memory[expr.args[1].name]):
                return functionalDictAdd(memory, {expr.args[0].name : memory[expr.args[1].name]})
            else:
                raise Exception("Make, when used with two variables only works with equal types, not %s %s = %s and %s %s = %s" % (type(memory[expr.args[0].name]), expr.args[0].name, memory[expr.args[0].name], type(memory[expr.args[1].name]), expr.args[1].name, memory[expr.args[1].name]))
    elif expr.argCount == 3:
        memory[expr.args[0].name] = memory["args"][expr.args[2].content]
        return functionalDictAdd(memory, {expr.args[0].name:memory["args"][expr.args[2].content]})
    return memory

# interpretMath :: Expression -> MemType -> (int -> int -> int) -> MemType
def interpretMath(expr: Expression, memory: MemType, op: Callable[[int, int], int]) -> MemType:
    """
    Uses the given operator on arguments in the expression and returns the new memory
    """
    if type(expr.args[1]) == Value:
        if type(memory[expr.args[0].name]) == type(expr.args[1].content):
            return functionalDictAdd(memory, {expr.args[0].name:op(memory[expr.args[0].name], expr.args[1].content)})
        else:
            raise Exception("Math only works with equal types, not %s and %s" % (type(memory[expr.args[0].name]), type(expr.args[1].content)))
    elif (type(expr.args[0]) == Variable) and (type(expr.args[1]) == Variable):
        if type(memory[expr.args[0].name]) == type(memory[expr.args[1].name]):
            return functionalDictAdd(memory, {expr.args[0].name:op(memory[expr.args[0].name], memory[expr.args[1].name])})
        else:
            raise Exception("Math with two variables only works with equal types, not %s and %s" % (type(memory[expr.args[0].name]), type(memory[expr.args[1].content])))
    else:
        if type(memory[expr.args[0].name]) == type(memory[expr.args[1].name]):
            return functionalDictAdd(memory, {expr.args[0].name:op(memory[expr.args[0].name], memory[expr.args[1].name])})
        else:
            raise Exception("Math only works with equal types, not %s %s and %s %s" % (type(memory[expr.args[0].name]), memory[expr.args[0].name], type(memory[expr.args[1].name]),memory[expr.args[1].name]))
    return memory

# myPrint :: Expression -> MemType -> None
def myPrint(expr: Expression, memory: MemType) -> None:
    """
    Prints the content of the show expression to the terminal
    """
    print(*map(lambda x: x.content[1:-1] if type(x) == Value and '"' in x.content else (
        memory[x.name] if type(memory[x.name]) == int else memory[x.name][1:-1]), expr.args))

# interpretFunction :: Function -> MemType -> MemType
def interpretFunction(expr: Function, memory: MemType) -> MemType:
    """ Interpret the body of a Function and return the new memory"""
    return functionalDictAdd(memory, {expr.name:expr.body})

# interpretExpression :: InterpretType -> MemType -> MemType
def interpretExpression(expr: InterpretType, memory: MemType) -> MemType:
    """Interpret the Expression by matching the appropriate interpreter function
    returns the new memory"""
    match expr:
        case If(_, _, _):           return interpretIf(expr, memory)
        case Loop(_, _, _):         return interpretLoop(expr, memory)
        case Call(_, _, _, _):      return interpretCall(expr, memory)
        case Function(_, _):        return interpretFunction(expr, memory)
        case Expression("show", _, _):      myPrint(expr, memory); return memory
        case Expression("make", _, _):      return interpretMake(expr, memory)
        case Expression("plus", _, _):      return interpretMath(expr, memory, op.add)
        case Expression("minus", _, _):     return interpretMath(expr, memory, op.sub)
        case Expression("times", _, _):     return interpretMath(expr, memory, op.mul)
        case Expression("divide", _, _):    return interpretMath(expr, memory, op.floordiv)
        case _: raise Exception("Expected BuiltIn or Variable, got %s" % expr.function)

# interpet :: ASTType -> MemType -> MemType
def interpret(ast: ASTType, memory: MemType = None) -> MemType:
    """Main interpreter function
    Interpret an ASTType and return final memory"""
    if not memory:
        memory = {}
    newmemory = interpretExpression(ast[0], memory)
    if rest := ast[1:]:
        return interpret(rest, newmemory)
    return newmemory
    