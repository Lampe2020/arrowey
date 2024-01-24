#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Implement compiler using https://github.com/numba/llvmlite later on?
import lark, sys, os
arr_version = '0.1.1-pre-alpha+py3.10-plus'
NaN:float = float('NaN')
Infinity:float = float('Infinity')
with open((os.path.sep if os.path.sep=='/' else '')+os.path.join(*(__file__.split(os.path.sep)[:-1]), 'arrowey.lark'),'r') as larkfile:
    parser = lark.Lark(larkfile.read())

def argument(argument_to_search_for):
    if not argument_to_search_for in sys.argv:
        for arg in sys.argv:
            if arg[0:len(argument_to_search_for)+1] == argument_to_search_for+":":
                return arg.split(":", 1)[1]
        return False
    else:
        return True

def logmsg(mood:int=0,msg:str|tuple[str,...]|list[str]|set[str]='')->None:
    """
    Print one or more log message(s) with associated status.
    """
    if type(msg)==str:
        msg = (msg,)
    elif type(msg) not in (tuple,list,set):
        logmsg(-1, (f'logmsg(): message list has wrong type: {repr(type(msg).__name__)}',))
        msg = (repr(msg),)
    match mood:
        # msym: Mood SYMbol
        case -3:
            msym:str = '!' # fatal error
        case -2:
            msym:str = '-' # error
        case -1:
            msym:str = 'w' # warning
        case 0:
            msym:str = 'i' # info
        case 1:
            msym:str = '+' # success
        case _:
            msym:str = '?' # unknown
    for message in msg:
        print(f'[{msym}] {message}')

def codegrid(code:str) -> tuple[str, ...]:
    """
    Returns the given code as a list of strings of equal length, one string=one line
    """
    rawcodegrid:tuple[str, ...] = code.split('\n')
    if rawcodegrid[0].startswith('#!'):
        rawcodegrid = rawcodegrid[1:] # Remove shebang line
    if rawcodegrid[0].startswith('# -*- ') and rawcodegrid[0].endswith('-*-'):
        rawcodegrid = rawcodegrid[1:] # Remove encoding line
    # Measure for the longest line
    longest:int = 0
    for line in rawcodegrid:
        if len(line) > longest:
            longest = len(line)
    return tuple(line.ljust(longest) for line in rawcodegrid) # Return the code grid for access like `grid[row][col]`

def linearize(code:tuple[str, ...]) -> str:
    """
    Kind-of a preparser,
    converts a code grid into parseable code
    """
    playhead_pos:tuple[int,int] = (0,0)
    codeline:str = ''
    lastdir:str = '→'
    def move(pos:tuple[int,int], direction:str|Ellipsis=...):
        directions = {'←':(0,-1), '↓':(1,0), '↑':(-1,0), '→':(0,1)} # Relative positions
        if direction in directions.keys():
            return (
                pos[0] + directions[direction][0],
                pos[1] + directions[direction][1]
            )
        else:
            logmsg(-1, f'arrowey.linearize.<move>(): called at position {repr(pos)} with invalid direction {repr(direction)}!')
            return pos
    while True: # Gets stopped by `return` statement
        try:
            codeline += code[pos[0]][pos[1]]
            move(playhead_pos, (
                codeline[-1] if (code[pos[0]][pos[1]] in ('←', '↓', '↑', '→'))
                else lastdir
            ))
        except IndexError:
            return codeline # We his a border, meaning we must have hit the end.

#TODO: Maybe implement parsers as classes, not as functions?

def recursive_parse(code:str)->any:
    """
    Same as parse(), just using Python's stack to make our lives easier.
    """
    sys.setrecursionlimit(3_333) # Some high number to prevent arrowey from crashing too easily with recursion errors

def iterative_parse(code:str)->any:
    """
    Parse the given line of code and return its return value

    Follow the parse tree:
    Stack: uppermost node has highest list index
    create a stack, when encountering a node push it onto there and call the stack visit function.
    If stack visitor tells us the uppermost node can have children, go into the uppermost node and put its first child onto the stack,
    if the stack visitor returns nothing, pop the uppermost node off the stack and call its visitor method, then push its next sibling onto the stack if it has such.
    Rinse and repeat.

    ↑ Acceptable?

    To visit node: add to to-parse list with its parent node ID as an attribute to tell the visitor what element to tell that its child has been visited.
    If the node that gets updated then has no unvisited TERMINAL nodes left it is added to a runnable list (?) and if it has non-TERMINAL child nodes left it waits until they are marked runnable.

    When we encounter a node we give it an ID and store it in the flat node buffer. We then iterate over that buffer and extract all child nodes and give them IDs as well as a property telling which node is their parent and adding the child's ID to a children property on the parent.
    When all nodes have no nested children and every node except the `start` node (ID 0) has a parent ID associated with it we iterate over the buffer again and resolve all TERMINALs and store them into their parents.
    When all TERMINALs are resolved we iterate over the buffer from the node 0 (`start`) and through its children etc. to implement the behaviour.
    """

    stack:list[lark.any] = []

    #TODO: Implement stack handling!

def parse(code:str, iterative:bool=False)->any:
    """
    Parse the code with the selected parsing function, defaulting to recursive.
    """
    if iterative:
        return iterative_parse(code)
    else:
        return recursive_parse(code)

if __name__ == '__main__':
    # Do the interactive shells with the help of `readline` module? https://docs.python.org/3.10/library/readline.html#module-readline
    if argument('--help') or argument('-h'):
        logmsg(0, f'''arrowey v{arr_version}
            
            Usage:
            <no args>            
            --help|-h           Display this help and exit.
            
            '''.replace('           ', '')) # Remove unecessary padding.
        sys.exit(0)
    elif ((not (argument('--parse-only') or argument('-p'))) and len(sys.argv)==2) or len(sys.argv)==1:
        file_is_script:bool = bool(argument('--script') or argument('-s'))
        #TODO: Implement parser above and invoke it here
    else:
        logmsg(0, (
            f'arrowey v{arr_version}',
            'Type "end:0" (without the double quotes) or press [Ctrl]+[D] to exit.'
        ))
        codebuf:str = ''
        nl:str='\n'
        while True:
            try:
                inp:str = input(f'arrowey {"..." if codebuf else ">>>"} ')
            except (EOFError, KeyboardInterrupt):
                inp:str = 'end:0'
            except Exception as err:
                from traceback import format_exception
                logmsg(-3, f'Error while reading stdin!\n{nl.join(format_exception(err))}')
                inp:str = 'end:0'
            if inp == 'end:0' and not codebuf:
                logmsg(0, 'arrowey stopped')
                sys.exit(0)
            if inp or codebuf:
                try:
                    AST = parser.parse(codebuf or inp)
                except lark.UnexpectedEOF as err:
                    codebuf = '\n'.join((codebuf, inp))
                    continue
                except Exception as err:
                    AST = None
                    codebuf = ''
                    logmsg(-2, f'Parser error!\n→ {type(err).__name__}: {err}')
                    continue
                if any((argument(arg) for arg in ('-p','--parse-only'))):
                    logmsg(1, f'AST successfully generated:\n{AST.pretty()}')
                else:
                    logmsg(1, f'Result:\n{run_from_AST(AST)}')
                codebuf = ''

