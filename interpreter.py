from collections import *
from AST import Expression, Variable, Value, Loop, Function, Call, If, ASTType
import operator as op
from typing import *

MemType = Dict[str, Union[str, int, List[Union[Function, Call, If, Loop, Expression]], List[Union[str, int]]]]
InterpretType = Union[If, Loop, Call, Function, Expression]

def interpretLoop(exp: InterpretType, memory: MemType) -> MemType:
    """
    Interprets the body of the loop until the condition is fullfilled
    """
    if not memory[exp.Variable.name] == exp.Value.content:
        memory = interpret(exp.body, memory)
        return interpretLoop(exp, memory)
    else:
        return memory

def interpretIf(exp: If, memory: MemType) -> MemType:
    """
    Executes the body of the if statement if the condition is fullfilled
    """
    extractor = lambda x: int(x.content) if type(x) == Value else int(memory[x.name])
    LHS = extractor(exp.LHS)
    RHS = extractor(exp.RHS)
    if LHS == RHS:
        memory = interpret(exp.body, memory)
    return memory

def interpretCall(exp: Call, memory: MemType) -> MemType:
    """
    Interprets a function call and returns the result after executing the function
    """
    if exp.name in memory:
        args = {"args" : list(map(lambda x: x.content if type(x) == Value else memory[x.name], exp.args))}
        tmp = dict(filter(lambda x: type(x[1]) == list and x[0] != "args", memory.items()))
        args = {**args, **tmp}
        temp = interpret(memory[exp.name], args)
        if exp.result: 
            memory[exp.result] = temp["result"]
        return memory
    else:
        raise Exception("Onbekende functie. Eerst Definieren")

def interpretMake(exp: Expression, memory: MemType) -> MemType:
    """
    Assigns the second argument in the expression the to first one
    """
    if exp.argc == 2:
        if type(exp.args[1]) == Value:
            memory[exp.args[0].name] = exp.args[1].content
        else:
            memory[exp.args[0].name] = memory[exp.args[1].name]
    elif exp.argc == 3:
        memory[exp.args[0].name] = memory["args"][exp.args[2].content]
    return memory

def interpretMath(exp: Expression, memory: MemType, op: Callable[[int, int], int]) -> MemType:
    """
    Uses the given operator on arguments in the expression and returns the memory
    """
    if type(exp.args[1]) == Value:
        if type(memory[exp.args[0].name]) == type(exp.args[1].content):
            memory[exp.args[0].name] = op(memory[exp.args[0].name], exp.args[1].content)
        else:
            raise Exception("Math only works with equal types, not %s and %s" % (type(memory[exp.args[0].name]), type(exp.args[1].content)))
    else:
        if type(memory[exp.args[0].name]) == type(memory[exp.args[1].name]):
            memory[exp.args[0].name] = op(memory[exp.args[0].name], memory[exp.args[1].name])
        else:
            raise Exception("Math only works with equal types, not %s and %s" % (type(memory[exp.args[0].name]), type(memory[exp.args[1].name])))
    return memory

def myPrint(exp: Expression, memory: MemType) -> None:
    """
    Prints the content of he show expression
    """
    print(*map(lambda x: x.content[1:-1] if type(x) == Value and '"' in x.content else (
        memory[x.name] if type(memory[x.name]) == int else memory[x.name][1:-1]), exp.args))

def interpretFunction(exp: Function, memory: MemType) -> MemType:
    """
    Returns the body of the given function so it will be executed next
    """
    memory[exp.name] = exp.body
    return memory


def interpretExpression(exp: InterpretType, memory: MemType) -> MemType:
    """
    Makes sure the correct interpreter function is used on the given expresion
    """
    match exp:
        case If(_, _, _):      return interpretIf(exp, memory)
        case Loop(_, _, _):    return interpretLoop(exp, memory)
        case Call(_, _, _, _): return interpretCall(exp, memory)
        case Function(_, _):   return interpretFunction(exp, memory)
        case Expression("show", _, _):     myPrint(exp, memory); return memory
        case Expression("make", _, _):     return interpretMake(exp, memory)
        case Expression("plus", _, _):     return interpretMath(exp, memory, op.add)
        case Expression("minus", _, _):    return interpretMath(exp, memory, op.sub)
        case Expression("times", _, _):    return interpretMath(exp, memory, op.mul)
        case Expression("divide", _, _):   return interpretMath(exp, memory, op.floordiv)
        case _: raise Exception("Expected BuiltIn or Identifier, got %s" % exp.function)

def interpret(ast: ASTType, memory: MemType = None) -> MemType:
    if not memory:
        memory = {}
    memory = interpretExpression(ast[0], memory)
    if rest := ast[1:]:
        memory = interpret(rest, memory)
    return memory
    