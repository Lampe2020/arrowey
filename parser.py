#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import lark
arr_version = '0.1.0'
with open('arrowey.lark','r') as larkfile:
    parser = lark.Lark(larkfile.read())

def printlog(mood:int=0,msg:str|tuple[str,...]|list[str]='')->None:
    """
    Print one or more log message(s) with associated status.
    """
    if type(msg)==str:
        msg = (msg,)
    elif type(msg) not in (tuple,list):
        printlog(-1, (f'printlog(): message list has wrong type: {repr(type(msg).__name__)}',))
    match mood:
        # msym: Mood SYMbol
        case -1:
            msym:str = '-'
        case 0:
            msym:str = 'i'
        case 1:
            msym:str = '+'
        case _:
            msym:str = '?'
    for message in msg:
        print(f'[{msym}] {message}')

printlog(0, (
        f'arrowey v{arr_version}',
        'Type "end:0" (without the double quotes) or press [Ctrl]+[D] to exit.'
    ))
while True:
    try:
        inp = input('arrowey>>> ')
    except EOFError:
        inp = 'end:0'
    if inp == 'end:0':
        printlog(0,'arrowey stopped')
        break
    if inp:
        try:
            AST = parser.parse(inp)
        except Exception as err:
            AST = None
            printlog(-1,f'Parser error!\n→ {type(err).__name__}: {err}')
            continue
        printlog(1,f'AST successfully generated:\n{AST.pretty()}')
