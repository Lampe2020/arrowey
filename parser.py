#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import lark
arr_version = '0.1.1-prerelease+py3'
with open('arrowey.lark','r') as larkfile:
    parser = lark.Lark(larkfile.read())

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

if __name__ == '__main__':
    logmsg(0, (
        f'arrowey v{arr_version}',
        'Type "end:0" (without the double quotes) or press [Ctrl]+[D] to exit.'
    ))
    while True:
        try:
            inp = input('arrowey>>> ')
        except EOFError:
            inp = 'end:0'
        except Exception as err:
            from traceback import format_exception
            nl:str='\n'
            logmsg(-3, f'Error while reading stdin!\n{nl.join(format_exception(err))}')
            inp = 'end:0'
        if inp == 'end:0':
            logmsg(0, 'arrowey stopped')
            break
        if inp:
            try:
                AST = parser.parse(inp)
            except Exception as err:
                AST = None
                logmsg(-2, f'Parser error!\n→ {type(err).__name__}: {err}')
                continue
            logmsg(1, f'AST successfully generated:\n{AST.pretty()}')
