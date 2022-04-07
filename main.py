from lex import lex, verbose_lex
from AST import parse, verbose_parse
import AST as a
import interpreter as i
import compiler as c

from time import time
import sys
from os import path
import threading
import platform
import argparse



def set_stack_recursion():
    """
    Function that sets recusion limit to 0x1000000 and increases stacksize based on OS
    """
    sys.setrecursionlimit(0x1000000)
    if platform.system() == "Linux":
        print("running on linux stack size: 2gb\n")
        threading.stack_size(2147483648) #set stack to 2gb
    else:
        print("running on windows stack size: 256mb\n")
        threading.stack_size(256000000)


def main():
    """
    Main function called if script starts, procceses arguments and starts interpreter/compiler
    """
    global parse
    global lex
    parser = argparse.ArgumentParser(description="Interpreter & Compiler for scolang-- programming language")
    parser.add_argument("file_name", type=str, metavar='File name', help="the file name that needs to be interpreted or compiled")
    parser.add_argument('-c','--compile',  dest='compile',       action='store_true',default=False, help="Run and Compile into Assembly files")
    parser.add_argument('-l','--lex',      dest='verbose-lex',   action='store_true',default=False, help="Run with verbose lexing")
    parser.add_argument('-p','--parse',    dest='verbose-parse', action='store_true',default=False, help="Run with verbose parsing")
    parser.add_argument('-v','--verbose',  dest='verbose-all',   action='store_true',default=False, help="Run with verbose lexing and parsing")
    parser.add_argument('-s','--stats',    dest='statistic',     action='store_true',default=False, help="Shows time statistics")
    arguments = vars(parser.parse_args())

    set_stack_recursion()
    #check if file exists
    if (not path.exists(arguments['file_name'])):
        raise Exception("no file named { %s } at specified path " % arguments["file_name"])
    
    #use decorated functions based on verbose flags
    if (arguments['verbose-all'] == True or arguments['verbose-parse'] == True):
        parse = verbose_parse(parse)   # add new func
    if (arguments['verbose-all'] == True or arguments['verbose-lex'] == True):
        lex = verbose_lex(lex) # new func
    if (arguments['statistic'] == True):
        start_time = time()
    


    lex_out = lex(arguments['file_name'])
    ast = parse(lex_out)
    i.interpret(ast)
    
    if(arguments['statistic']==True):
        print("time to run program: {} seconds".format(round(time()-start_time,4)))


    if (arguments['compile'] == True):
        c.mainCompiler(arguments['file_name'].strip(".sco"),ast)


if __name__ == "__main__":
    main()