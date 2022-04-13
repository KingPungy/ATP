from functools import reduce
import re
from typing import *

A = NewType('A', int) # Generic type [A]

# Generic token made of two strings
class Token:
    """Generic Token class made of 2 strings"""    
    def __init__(self, type_: str, text_: str):
        self.type = type_
        self.text = text_
    def __str__(self):
        return f"Token: {self.type}, content: {self.text}"
    def __repr__(self):
        return self.__str__() #"[" + self.type + ", " + self.text + "]"


# https://www.geeksforgeeks.org/function-composition-in-python/#:~:text=Function%20composition%20is%20the%20way,second%20function%20and%20so%20on.



def composite_function(*func):
    """Nests given list of functions
    Returns: singular function made of nested function for readability 
    and cleaner functional programming
    """    
    def compose(f, g):
        """Nests given functions into eachother
        Returns: Func: nested function f(g(x))
        """    
        return lambda x: f(g(x))

    return reduce(compose, func, lambda x: x)

# genToken :: str -> Token
def genToken(word: str) -> Token:
    """
    Gets token out of a word. 
    Takes a string "word" and returns a token 
    """
    builtins = ["show", "make", "plus", "minus", "defunc", "times", "divide"]
    if word in builtins:
        return Token("BuiltIn", word)
    if word[0] == '"' and word[-1] == '"':
        return Token("String", word)
    if (all(map(str.isdigit, word)) or # Positive 
       (word[0] == '-' and all(map(str.isdigit,word[1:])))): # and negative numbers
        return Token("Number", word)
    if re.fullmatch("^[a-zA-Z_][a-zA-Z_0-9]*", word) is not None:
        return Token("Variable", word)
    if word == "while":
        return Token("LoopStart", word)
    if word == "endwhile":
        return Token("LoopEnd", word)
    if word == "if":
        return Token("If", word)
    if word == "endif":
        return Token("Endif", word)
    raise Exception("Invalid Syntax: %s" % word)

# removeEmptyLine :: (A -> A) -> (str, str)
def removeEmptyLine(func: Callable[[A], A]) -> Tuple[str, str]:
    """Decorator that checks input is not empty and returns a tuple of two empty strings to fill the empty tuple"""
    def inner(toLex):
        if not toLex:
            return ("","")
        return func(toLex)
    return inner

@removeEmptyLine
# lexString :: str -> (str, str)
def lexString(toLex: str) -> Tuple[str, str]:
    """-
    Lex a string between "__" quotation marks
    """
    head, *tail = toLex
    if head != '"':
        string, rest = lexString(tail)
        return (head+string, rest)
    else:
        return (head, tail)

@removeEmptyLine
# lexToken :: str -> (str, str)
def lexToken(toLex: str) -> Tuple[str, str]:
    """
    Lex a line  that are used for tokens
    """
    head, *tail = toLex
    if head != " ":
        string, rest = lexToken(tail)
        return (head+string, rest)
    else:
        return ("", tail)

# lexLine :: str -> ([Token | Str], str)
def lexLine(toLex: str) -> Tuple[List[Union[Token, str]], str]:
    """Lex a line of scolang code
    Returns: a list of tokens and the rest of the string
    """
    if not toLex:
        return ([],"")
    head, *tail = toLex
    if head.isalnum() or (head[0] == '-' and all(map(str.isdigit,head[1:]))): # checks for positive and negative number
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

# flatten :: [A, [A, [A, []]]] -> [A]
def flatten(t): # [A, [A, [A, []]]] -> [A]
    """
    Converts recursive list into regular list
    """    
    if not t:
        return []
    if len(t) == 1:
        return t[0]
    return [t[0]] + flatten(t[1])

# removeCommentAndBlank :: str -> str
def removeCommentAndBlank(toLex: str) -> str:
    """
    Removes:
        comments after # {Text}  and stitches the rest together,
        removes leading and trailing whitespaces
    """
    return re.sub(r"\#.*", "", toLex).strip()

# myHead :: (A, A) -> A
def myHead(a: tuple) -> A:
    """Returns the first item of a tuple"""
    return a[0]

# genTokens :: [str] -> [Token]
def genTokens(a: List[str]) -> List[Token]:
    """Loop for genToken functie"""
    return list(map(lambda x: genToken(x), a))


linesToTokens = composite_function(genTokens, flatten, myHead, lexLine, removeCommentAndBlank)

# lex :: str -> [Token]
def lex(filename: str) -> List[Token]:
    """
    Lexes the given string into a list of tokens for the parser
    """
    with open(f"ScolangSrc/{filename}") as file: 
        lines = file.read().replace(";", "\n").split("\n")
    return list(filter(None, map(linesToTokens, lines)))

# verbose_lex :: Callable -> Callable
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
