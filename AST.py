from ast import AST
from collections import namedtuple
from time import time
from dataclasses import dataclass
from unittest import expectedFailure
from lex import lex, Token
from typing import *

# My AST contains Functions, Calls, Ifs, Loops and Expressions, but Function and If contain an ASTType
ASTType = List #[Union[Function, Call, If, Loop, Expression]]

@dataclass
class Variable:
    name: str

@dataclass
class Value:
    content: Union[str, int]
@dataclass
class Call:
    name: str
    result: str
    argc: int
    args: List[Value | Variable]

@dataclass
class Expression:
    function: str
    argc: int 
    args: List[Variable | Value]

@dataclass
class Loop:
    body: ASTType
    Variable: Variable
    Value: Value

@dataclass
class If:
    body: ASTType
    LHS: Variable
    RHS: Value

@dataclass
class Function:
    name: str
    body: ASTType


def parseMake(tokensLine: List[Token], variables: List[str]) -> Tuple[Expression, List[str]]:
    """
    parses the make token to assign a variable or grab arguments in a function
    """
    if len(tokensLine) == 3:
        if tokensLine[1].type == "Identifier":
            if tokensLine[2].type == "Number":
                return Expression("make", len(tokensLine[1:]),[Variable(tokensLine[1].text), Value(int(tokensLine[2].text))]), variables+[tokensLine[1].text]
            elif tokensLine[2].type == "String":
                return Expression("make", len(tokensLine[1:]),[Variable(tokensLine[1].text), Value(tokensLine[2].text)]), variables+[tokensLine[1].text]
            elif tokensLine[2].type == "Identifier":
                    if tokensLine[2].text in variables:
                        return Expression("make", len(tokensLine[1:]),[Variable(tokensLine[1].text), Variable(tokensLine[2].text)]), variables+[tokensLine[1].text]   
                    else:
                        raise Exception("Unknown variable name: %s" % tokensLine[2].text)
            else:
                raise Exception("Expected a Number or a String, but got an %s, %s instead." % (tokensLine[2].type, tokensLine[2].text))
        else:
            raise Exception("Expected an Identifier, but got an %s, %s instead." % (tokensLine[0].type, tokensLine[0].text))
    elif len(tokensLine) == 4: # while in a function a line of 4 tokens can be used to grab one of te arguments that was given
        if tokensLine[2].text == "args":
            if tokensLine[3].type == "Number":
                return Expression("make", len(tokensLine[1:]), [Variable(tokensLine[1].text), Variable(tokensLine[2].text), Value(int(tokensLine[3].text))]), variables+[tokensLine[1].text]
            else:
                raise Exception("Only tokens of type Number can be used as an index, got %s instead" % tokensLine[3].type)
        else:
            raise Exception("Passing 3 arguments to make is only allowed when indexing an argument list:{ %s }" % tokensLine[2].text )             
    else:
        raise Exception("Make only takes 2 or arguments. (3 when using indexes) %s were given." % len(tokensLine[1:]))

def parseMathStatement(tokensLine: List[Token], variables: List[str]) -> Tuple[Expression, List[str]]:
    """
    Parses a math statement into one of the Built in functions
    """
    if len(tokensLine) == 3:
        if tokensLine[1].type == "Identifier":
            if tokensLine[1].text in variables:
                if tokensLine[2].type == "Number":
                    return Expression(tokensLine[0].text, len(tokensLine[1:]),[Variable(tokensLine[1].text), Value(int(tokensLine[2].text))]), variables
                elif tokensLine[2].type == "Identifier":
                    if tokensLine[2].text in variables:
                        return Expression(tokensLine[0].text, len(tokensLine[1:]),[Variable(tokensLine[1].text), Variable(tokensLine[2].text)]), variables
                    else:
                        raise Exception("Unknown variable name: %s" % tokensLine[2].text)   
                else:
                    raise Exception("Expected a Number or an Identifier, but got an %s, %s instead." % (tokensLine[2].type, tokensLine[2].text))    
            else:
                raise Exception("Unknown variable name: %s" % tokensLine[1].text) 
        else:
            raise Exception("Expected an Identifier, but got an %s, %s instead." % (tokensLine[1].type, tokensLine[1].text))
    else:
        raise Exception("A Math statement only takes 2 arguments. %s was given %s arguments." % (tokensLine[0].text, len(tokensLine[1:])))

def parseDefinition(tokensLine: List[Token], variables: List[str]) -> Tuple[Function, List[str]]:
    """
    Parses function definition and parses & Lex the file with the function name
    """
    if len(tokensLine) == 3:
        if all(map(lambda x: x.type == "Identifier", tokensLine[1:])):
            tmp = list(filter(lambda x: x[-1] == '~', variables))
            return Function(tokensLine[1].text, parse(lex(tokensLine[2].text + ".sco"), tmp)), variables+[tokensLine[1].text + '~']
        else:
            raise Exception("Defunc expects two Identifiers. Got %s instead" % list(map(lambda x: x.type, tokensLine[1:])))
    else:
        raise Exception("Defunc expects two arguments, a function name and a file name. Got %s instead" % list(map(lambda x: x.text, tokensLine[1:])))

def parseFunctionCall(tokensLine: List[Token], variables: List[str]) -> Tuple[Call, List[str]]:
    """
    Parses a function call with all given arguments
    """
    if all(map(lambda x: True if x.type == "String" or x.type == "Number" else (True if x.text in variables else False), tokensLine[2:])):
        if tokensLine[1].type == "Identifier" and tokensLine[1].text == "void":
            return Call(tokensLine[0].text, None, len(tokensLine[2:]), list(map(lambda x: Value(x.text) if x.type == "String" or x.type == "Number" else Variable(x.text), tokensLine[2:]))), variables
        elif tokensLine[1].type == "Identifier" and tokensLine[1].text not in variables:
            return Call(tokensLine[0].text, tokensLine[1].text, len(tokensLine[2:]), list(map(lambda x: Value(x.text) if x.type == "String" or x.type == "Number" else Variable(x.text), tokensLine[2:]))), variables+[tokensLine[1].text]
        else:
            raise Exception("A Function Call expects an unused variable name or 'void'\nException: Or you misspelled a BuiltIn Function: {%s}" % tokensLine[0].text)

    else:
        raise Exception("Only strings, numbers or known variable names are allowed as an Argument")

def parseShow(tokensLine: List[Token], variables: List[str]) -> Tuple[Expression, List[str]]:
    """
    Parses the Built in show function
    """
    return Expression(("show"), len(tokensLine[1:]), [Variable(x.text) if x.type == "Identifier" else Value(x.text) for x in tokensLine[1:]]), variables


def parseLine(tokensLine: List[Token], variables: List[str]) -> Tuple[Union[Expression, Call, Function], List[str]]:
    """
    Parses a line of tokens based on the first token
    """
    if tokensLine[0].type == "BuiltIn":
        if tokensLine[0].text == "show":
            return parseShow(tokensLine, variables)
        if tokensLine[0].text == "make":
            return parseMake(tokensLine, variables)   
        elif tokensLine[0].text in ["plus", "minus", "divide", "times"]:
            return parseMathStatement(tokensLine, variables)
        elif tokensLine[0].text == "defunc":
            return parseDefinition(tokensLine, variables)
    elif tokensLine[0].type == "Identifier":
        return parseFunctionCall(tokensLine, variables)
    else:
        raise Exception("First token can only be of type BuiltIn or Identifier")
                 

def parseLoop(tokens: List[Token], variables: List[str]) -> Tuple[Loop, List[str]]:  
    """
    Parses a loop 
    """
    body = parse(tokens[1:-1], variables)
    if len(tokens[-1]) < 2:
        return Loop(body, None, None), variables
    elif len(tokens[-1]) < 3 and tokens[-1][1].type == "Identifier":
        return Loop(body, Variable(tokens[-1][1].text), 0), variables
    elif tokens[-1][1].type == "Identifier" and tokens[-1][2].type == "Number":
        return Loop(body, Variable(tokens[-1][1].text), Value(int(tokens[-1][2].text))), variables
    else:
        if len(tokens[-1]) < 3:
            raise Exception("Endwhile expects an Identifier, got %s instead." % tokens[-1][1].type)
        else:
            raise Exception("Endwhile expects an Identifier and a Number, got %s and %s instead." % (tokens[-1][1].type, tokens[-1][2].type))

def parseIf(tokens: List[Token], variables: List[str]) -> Tuple[If, List[str]]:
    """
    Parses the if statement
    """
    body = parse(tokens[1:-1], variables) 
    if len(tokens[0]) == 3:
        if tokens[0][1].type == "Identifier":
            if tokens[0][1].text in variables:
                LHS = Variable(tokens[0][1].text)
        elif tokens[0][1].type == "Number":
                LHS = Value(tokens[0][1].text)
        else:
            raise Exception("First type must be identifier or number")
        if tokens[0][2].type == "Identifier":
            if tokens[0][2].text in variables:
                RHS = Variable(tokens[0][2].text)
        elif tokens[0][2].type == "Number":
                RHS = Value(tokens[0][2].text)
        else:
            raise Exception("Second type must be identifier or number")
        return If(body, LHS, RHS), variables
    else:
        raise Exception("If needs two arguments to compare")


def parse(tokens: List[Token], variables: List[str] = None) -> ASTType:
    """
    Parses List of tokens into an AST
    """
    if not tokens:
        return []
    if variables == None:
        variables = []
    if tokens[0][0].text == "while":
        loopLocations = list(map(lambda x: True if x[0].text == "endwhile" else False, tokens))
        try:
            loopEnd = loopLocations.index(True, 1)
        except ValueError as _:
            raise Exception("While loop opened but not closed.")
        temp, variables = parseLoop(tokens[:loopEnd+1], variables)
        return [temp] + parse(tokens[loopEnd+1:], variables)
    if tokens[0][0].text == "if":
        endifs = list(map(lambda x: True if x[0].text == "endif" else False, tokens))
        try:
            end = endifs.index(True, 1)
        except ValueError as _:
            raise Exception("If statement opened but not closed.")
        temp, variables = parseIf(tokens[:end+1], variables)
        return [temp] + parse(tokens[end+1:], variables)
    if len(tokens) < 2:
        temp, _ = parseLine(tokens[0], variables)
        return [temp]
    else:
        temp, variables = parseLine(tokens[0], variables) 
        return [temp] + parse(tokens[1:], variables)


def verbose_parse(f : Callable):
    """
    decorator for the parse function to print the parse output and some extra info
    """
    def inner(lex_output : List[Token]):
        print("start parsing program")
        start_time = time()
        output = f(lex_output)
        print("parsed {} lines of code".format(len(output)))
        print("took: {} seconds to parse program\n".format(round(time()-start_time,4)))
        print("parser output:")
        for i in range(len(output)):
            print("regel {}: {}".format(i+1,output[i]))
        print("\n")
        return output
    return inner
