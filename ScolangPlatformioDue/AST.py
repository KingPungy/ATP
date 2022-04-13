from ast import AST
from collections import namedtuple
from time import time
from dataclasses import dataclass
from unittest import expectedFailure
from lex import lex, Token
from pprint import pprint
from typing import *

# My AST contains Functions, Calls, Ifs, Loops and Expressions, but Function , If and Loop contain an ASTType for body
ASTType = List #[Union[Function, Call, If, Loop, Expression]]

@dataclass
class Variable:
    name: str                       # Name of the Variable

@dataclass
class Value:
    content: Union[str, int]        # Content of the "Value" can be a string or an interger

@dataclass
class Call:
    name: str                       # Name of the Function you're calling
    result: str                     # Name of the variable in which the result will be stored 
    argCount: int                   # Amount of variables or value that are passed with the function call. max 4. doesnt need to be exact
    args: List[Value | Variable]    # List of Variables or Values passed with the function call

@dataclass
class Expression:
    function: str                   # Name of the Function given at definition or one of the BuiltIn functions 
    argCount: int                   # Number of arguments
    args: List[Variable | Value]    # List which can be filled with arguments when called

@dataclass
class Loop:
    body: ASTType                   # Body of the Loop. can contain all other expressions
    LHS: Union[Variable, Value]     # lHS [Variable | Value] of the condition
    RHS: Union[Variable, Value]     # RHS [Variable | Value] of the condition

@dataclass
class If: 
    body: ASTType                   # Body of the IF Statement. can contain all other expressions
    LHS: Union[Variable, Value]     # lHS [Variable | Value] of the condition
    RHS: Union[Variable, Value]     # RHS [Variable | Value] of the condition

@dataclass
class Function:
    name: str                       # Name of the Function given at definition with defunc
    body: ASTType                   # Body of the Function. Can contain all other expressions

# parseMake :: [Token] -> [str] -> (Expression, [str])
def parseMake(tokensLine: List[Token], variables: List[str]) -> Tuple[Expression, List[str]]:
    """Parses the make Expresion to assign a variable or grab arguments in a function
    Takes a list of variables and returns: Expresion and the new list of variables
    """
    if len(tokensLine) == 3:
        if tokensLine[1].type == "Variable":
            if tokensLine[2].type == "Number":
                return Expression("make", len(tokensLine[1:]),[Variable(tokensLine[1].text), Value(int(tokensLine[2].text))]), variables+[tokensLine[1].text]
            elif tokensLine[2].type == "String":
                return Expression("make", len(tokensLine[1:]),[Variable(tokensLine[1].text), Value(tokensLine[2].text)]), variables+[tokensLine[1].text]
            elif tokensLine[2].type == "Variable":
                    if tokensLine[2].text in variables:
                        return Expression("make", len(tokensLine[1:]),[Variable(tokensLine[1].text), Variable(tokensLine[2].text)]), variables+[tokensLine[1].text]   
                    else:
                        raise Exception("Unknown variable name: %s" % tokensLine[2].text)
            else:
                raise Exception("Expected a Number or a String, but got an %s, %s instead." % (tokensLine[2].type, tokensLine[2].text))
        else:
            raise Exception("Expected a Variable, but got an %s, and an %s instead." % (tokensLine[0].type, tokensLine[0].text))
    elif len(tokensLine) == 4: # while in a function a line of 4 tokens can be used to grab one of te arguments that was given in the function call
        if tokensLine[2].text == "args":
            if tokensLine[3].type == "Number":
                return Expression("make", len(tokensLine[1:]), [Variable(tokensLine[1].text), Variable(tokensLine[2].text), Value(int(tokensLine[3].text))]), variables+[tokensLine[1].text]
            else:
                raise Exception("Only tokens of type Number can be used as an index, got %s instead" % tokensLine[3].type)
        else:
            raise Exception("Passing 3 arguments to make is only allowed when indexing an argument list while in a function:{ %s }" % tokensLine[2].text )             
    else:
        raise Exception("Make only takes 2 or arguments. (3 when used to index passed arguments) %s were given." % len(tokensLine[1:]))

# parseMathStatement :: [Token] -> [str] -> (Expression, [str])
def parseMathStatement(tokensLine: List[Token], variables: List[str]) -> Tuple[Expression, List[str]]:
    """
    Parses a math statement into one of the Built in functions
    Takes a list of variables and returns: Expression and the new variables
    """
    if len(tokensLine) == 3:
        if tokensLine[1].type == "Variable":
            if tokensLine[1].text in variables:
                if tokensLine[2].type == "Number":
                    return Expression(tokensLine[0].text, len(tokensLine[1:]),[Variable(tokensLine[1].text), Value(int(tokensLine[2].text))]), variables
                elif tokensLine[2].type == "Variable":
                    if tokensLine[2].text in variables:
                        return Expression(tokensLine[0].text, len(tokensLine[1:]),[Variable(tokensLine[1].text), Variable(tokensLine[2].text)]), variables
                    else:
                        raise Exception("Unknown variable name: %s" % tokensLine[2].text)   
                else:
                    raise Exception("Expected a Number or a Variable, but got an %s, %s instead." % (tokensLine[2].type, tokensLine[2].text))    
            else:
                raise Exception("Unknown variable name: %s" % tokensLine[1].text) 
        else:
            raise Exception("Expected a Variable, but got an %s, %s instead." % (tokensLine[1].type, tokensLine[1].text))
    else:
        raise Exception("A Math statement only takes 2 arguments. %s was given %s arguments." % (tokensLine[0].text, len(tokensLine[1:])))

# parseDefinition :: [Token] -> [str] -> (Function, [str])
def parseDefinition(tokensLine: List[Token], variables: List[str]) -> Tuple[Function, List[str]]:
    """
    Parses function definition and parses & Lex the file with the function name
    Takes a list of known variables

    lex and parses the defined function before continuing and returning: a Function and the new variables
    """
    if len(tokensLine) == 3:
        if all(map(lambda x: x.type == "Variable", tokensLine[1:])):
            tmp = list(filter(lambda x: x[-1] == '~', variables))
            return Function(tokensLine[1].text, parse(lex(tokensLine[2].text + ".sco"), tmp)), variables+[tokensLine[1].text + '~'] #lex and parse the function before continuing 
        else:
            raise Exception("Defunc expects two Identifiers. Got %s instead" % list(map(lambda x: x.type, tokensLine[1:])))
    else:
        raise Exception("Defunc expects two arguments, a function name and a file name without .sco. Got %s instead" % list(map(lambda x: x.text, tokensLine[1:])))

# parseFunctionCall :: [Token] -> [str] -> (Call, [str])
def parseFunctionCall(tokensLine: List[Token], variables: List[str]) -> Tuple[Call, List[str]]:
    """
    Parses a function call with all given arguments
    takes a list of variables and returns: A Call with new variables
    """
    if all(map(lambda x: True if x.type == "String" or x.type == "Number" else (True if x.text in variables else False), tokensLine[2:])):
        if tokensLine[1].type == "Variable" and tokensLine[1].text == "void":
            return Call(tokensLine[0].text, None, len(tokensLine[2:]), list(map(lambda x: Value(x.text) if x.type == "String" or x.type == "Number" else Variable(x.text), tokensLine[2:]))), variables
        elif tokensLine[1].type == "Variable" and tokensLine[1].text not in variables:
            return Call(tokensLine[0].text, tokensLine[1].text, len(tokensLine[2:]), list(map(lambda x: Value(x.text) if x.type == "String" or x.type == "Number" else Variable(x.text), tokensLine[2:]))), variables+[tokensLine[1].text]
        else:
            raise Exception("A Function Call expects an unused variable name or 'void'\nOr you misspelled a BuiltIn Function: {%s}" % tokensLine[0].text)

    else:
        raise Exception("Only strings, numbers or known variable names are allowed as an Argument")


# parseShow :: [Token] -> [str] -> (Expression, [str])
def parseShow(tokensLine: List[Token], variables: List[str]) -> Tuple[Expression, List[str]]:
    """
    Parses the Built in show function
    Takes a list of vaiables and returns: the Show Expression and a new list of variables
    """
    return Expression(("show"), len(tokensLine[1:]), [Variable(x.text) if x.type == "Variable" else Value(x.text) for x in tokensLine[1:]]), variables

# parseLine :: [Token] -> [str] -> (Expression | Call | Function, [str])
def parseLine(tokensLine: List[Token], variables: List[str]) -> Tuple[Union[Expression, Call, Function], List[str]]:
    """
    Parses a line of tokens based on the first token in the line
    Takes a list of Variables and returns: a tuple of either the [ Expression | Call | function ] and a list of new variables
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
    elif tokensLine[0].type == "Variable":
        return parseFunctionCall(tokensLine, variables)
    else:# this exeption will probable never occur because of the lexer
        raise Exception("First token can only be of type BuiltIn or Variable")
                 
# parseLoop :: [Token] -> [str] -> (Loop, [str])
def parseLoop(tokens: List[Token], variables: List[str]) -> Tuple[Loop, List[str]]:  
    """
    Parses a loop 
    Takes a list of variables and returns: a tuple of a [Loop Expression and a list of new variables]
    """
    body = parse(tokens[1:-1], variables)
    if len(tokens[-1]) < 2:
        return Loop(body, None, None), variables
    elif len(tokens[-1]) < 3 and tokens[-1][1].type == "Variable":
        return Loop(body, Variable(tokens[-1][1].text), Value(0)), variables
    elif tokens[-1][1].type == "Variable" and tokens[-1][2].type == "Number":
        return Loop(body, Variable(tokens[-1][1].text), Value(int(tokens[-1][2].text))), variables
    elif tokens[-1][1].type == "Variable" and tokens[-1][2].type == "Variable":
        return Loop(body, Variable(tokens[-1][1].text), Variable(tokens[-1][2].text)), variables
    else:
        if len(tokens[-1]) < 3:
            raise Exception("Endwhile expects a Variable, got %s instead." % tokens[-1][1].type)
        else:
            raise Exception("Endwhile expects a Variable and a Number, got %s and %s instead." % (tokens[-1][1].type, tokens[-1][2].type))

# parseIf :: [Token] -> [str] -> (If, [str])
def parseIf(tokens: List[Token], variables: List[str]) -> Tuple[If, List[str]]:
    """
    Parses the if statement
    Takes a list of variables
    """
    body = parse(tokens[1:-1], variables) 
    if len(tokens[0]) == 3:
        if tokens[0][1].type == "Variable":
            if tokens[0][1].text in variables:
                LHS = Variable(tokens[0][1].text)
        elif tokens[0][1].type == "Number":
                LHS = Value(tokens[0][1].text)
        else:
            raise Exception("First type must be Variable or number")
        if tokens[0][2].type == "Variable":
            if tokens[0][2].text in variables:
                RHS = Variable(tokens[0][2].text)
        elif tokens[0][2].type == "Number":
                RHS = Value(tokens[0][2].text)
        else:
            raise Exception("Second type must be Variable or number")
        return If(body, LHS, RHS), variables
    else:
        raise Exception("If needs two arguments to compare")

# scopeEndFind :: [Token] -> str -> int -> int
def scopeEndFind(tokens: List[Token], keyWord: str, scopeCounter = 1):
    """
    Finds the end token for the given if or while expression
    """
    if not tokens:
        return -1
    match keyWord:
        case "while":
            endword = "endwhile"
        case "if":
            endword = "endif"

    if tokens[0][0].text == endword:
        scopeCounter -= 1
    elif tokens[0][0].text == keyWord:
        scopeCounter += 1

    if not scopeCounter:
        return 1
    else:
        tmp = scopeEndFind(tokens[1:], keyWord, scopeCounter)
        if tmp == -1:
            return -1
        return 1 + tmp
    
    


# parse :: [Token] -> [str] -> ASTType
def parse(tokens: List[Token], variables: List[str] = None) -> ASTType:
    """
    Parses List of tokens into an AST
    Takes a list of variables to use in the parsing functions and returns: a ASTType Abstract Syntax Tree
    """
    if not tokens:
        return []
    if not variables:
        variables = []
    if tokens[0][0].text == "while":
        loopEnd = scopeEndFind(tokens[1:], "while")
        temp, variables = parseLoop(tokens[:loopEnd+1], variables)
        return [temp] + parse(tokens[loopEnd+1:], variables)
    if tokens[0][0].text == "if":
        end = scopeEndFind(tokens[1:], "if")
        temp, variables = parseIf(tokens[:end+1], variables)
        return [temp] + parse(tokens[end+1:], variables)
    if len(tokens) < 2:
        temp, _ = parseLine(tokens[0], variables)
        return [temp]
    else:
        temp, variables = parseLine(tokens[0], variables) 
        return [temp] + parse(tokens[1:], variables)

# verbose_parse :: Callable -> Callable
def verbose_parse(f : Callable):
    """
    decorator for the parse function to print the parse output and some extra info
    """
    def inner(lex_output : List[Token]):
        print("Start parsing program")
        start_time = time()
        output = f(lex_output)
        print("Parsed {} lines of code".format(len(output)))
        print("Took: {} seconds to parse program\n".format(round(time()-start_time,4)))
        print("Parser output:")

        print("Regels: ",*output,sep=f"\nRegel: ")
        
        return output
    return inner
