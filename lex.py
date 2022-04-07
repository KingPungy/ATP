from functools import reduce
import re
from typing import *

class Token:
    def __init__(self, type_: str, text_: str):
        self.type = type_
        self.text = text_
    def __repr__(self):
        return "[" + self.type + ", " + self.text + "]"


def compose(f, g):
    """Nests given functions into eachother

    Args:
        f (Func): 
        g (func): 

    Returns:
        Func: nested function f(g(x))
    """    
    return lambda x: f(g(x))


def composite_function(*func):
    """Nests given list of functions

    Returns:
        Func: singular function made of nested function for readability
    """    
    return reduce(compose, func, lambda x: x)


def genToken(w: str) -> Token:
    """
    Gets token out of a string
    """
    builtins = ["show", "make", "plus", "minus", "defunc", "times", "divide"]
    operators = ["in"]
    if w in builtins:
        return Token("BuiltIn", w)
    if w in operators:
        return Token("Operator", w)
    if w[0] == '"' and w[-1] == '"':
        return Token("String", w)
    if all(map(str.isdigit,w)) or (w[0] == '-' and all(map(str.isdigit,w[1:]))): # Positive and negative numbers
        return Token("Number", w)
    if re.fullmatch("^[a-zA-Z_][a-zA-Z_0-9]*", w) is not None:
        return Token("Identifier", w)
    if w == "while":
        return Token("LoopStart", w)
    if w == "endwhile":
        return Token("LoopEnd", w)
    if w == "if":
        return Token("If", w)
    if w == "endif":
        return Token("Endif", w)
    raise Exception("Invalid Syntax: %s" % w)

def ifNotDecorator(func):
    def inner(toLex):
        if not toLex:
            return ("","")
        return func(toLex)
    return inner

@ifNotDecorator
def lexString(toLex: str) -> Tuple[str, str]:
    head, *tail = toLex
    if head != '"':
        string, rest = lexString(tail)
        return (head+string, rest)
    else:
        return (head, tail)

@ifNotDecorator
def lexToken(toLex: str) -> Tuple[str, str]:
    head, *tail = toLex
    if head != " ":
        string, rest = lexToken(tail)
        return (head+string, rest)
    else:
        return ("", tail)

def lexLine(toLex: str) -> Tuple[List[Union[Token, str]], str]:
    if not toLex:
        return ([],"")
    head, *tail = toLex
    if head.isalnum() or (head[0] == '-' and all(map(str.isdigit,head[1:]))): # checks for number 
        token, rest = lexToken(toLex)
        string, rest2 = lexLine(rest)
        return ([token,string], rest2)
    elif head == " ":
        string, rest = lexLine("".join(tail))
        return (string, rest)
    elif head == '"':
        string, rest = lexString("".join(tail))
        string2, rest2 = lexLine(rest)
        return ([head+string,string2], rest2)
    return ([], toLex) 


def flatten(t): # [A, [A, [A, []]]] -> [A]
    """
    Converts recursive list into regular list
    """    
    if not t:
        return []
    if len(t) == 1:
        return t[0]
    return [t[0]] + flatten(t[1])

def removeCommentAndBlank(toLex: str) -> str:
    """
    Removes:
        comments between # {Text} # and stitches the rest together,
        removes leading and trailing whitespaces
    """

    return re.sub(r"\#.*\#", "", toLex).strip()

def myHead(a: tuple):
    return a[0]

def genTokens(a: List[str]) -> List[Token]:
    """
    Generates list of tokens from a list of strings
    """
    return list(map(lambda x: genToken(x), a))

def emptyLineFilter(a: list) -> List[Token]:
    """
    Removes empty instances of the list
    """
    return filter(None, a)

linesToTokens = composite_function(genTokens, flatten, myHead, lexLine, removeCommentAndBlank)


def lex(filename: str) -> List[Token]:
    """
    Lexes the given string into a list of tokens
    """
    with open(filename) as file: 
        lines = file.read().replace(";", "\n").split("\n")
    return list(filter(None, map(linesToTokens, lines)))


def verbose_lex(f: Callable):
    """
    Decorator for the lex function to print the lex output and some extra info
    """
    def inner(file_name : str):
        print("start lexing of program located in {}".format(file_name))
        print("lexer output:")

        tokens = f(file_name)

        print("Regels: ",*tokens,sep="\nRegel: ")
        return tokens
    return inner
