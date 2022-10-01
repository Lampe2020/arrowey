#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re # Needed for syntax reading (escaping escape sequences, finding variables, ...)
from sys import argv as args, exit
def argument(argument_to_search_for):
    if not argument_to_search_for in args:
        for arg in args:
            if arg[0:len(argument_to_search_for)+1] == argument_to_search_for+":":
                return arg.split(":", 1)[1]
        return False
    else:
        return True

# Read the file with encoding utf-8. This is required for arrowey as the arrow characters are multi-byte characters and far off the standard charset.
with open(argument('--file') or '__main__.arr', "r", encoding="utf-8") as arrfile:
    arrcode = arrfile.read()

# Measure for the longest line
longest = 0
for line in arrcode.split("\n"):
    if len(line) > longest:
        longest = len(line)

# Pad all lines to the longest line's length, thereby making the code rectangular
parsedcode_1 = list("") # Make a list out of the code so every character can be accessed like `parsedcode_1[row][col]`
for line in arrcode.split("\n"):
    parsedcode_1.append(line.ljust(longest))

newlinestring = '\n'
print(f'parsedcode_1: {newlinestring.join(parsedcode_1)}') # debug

# Loops and conditionals: maybe with if:(condition)→{code}[→{else-code}] and loops also like that (second part of conditional/loop optional)?

def parsecode(code):
    """
Parser function. Is as function so you can parse code later on.
"""
    ended = False
    parsedcode = ''
    lastdirect = 'right'
    row, col = 0, 0 # Current "playhead" position
    # Move down: row+=1; Move up: row-=1; Move left: col-=1; Move right: col+=1
    def move(pos, direction=...):
        directions = {'right':(0,1), 'down':(1,0), 'left':(0,-1), 'up':(-1,0)} # Relative positions
        if direction.lower() in ('right', 'down', 'left', 'up'):
            row = pos[0] + directions[direction.lower()][0]
            col = pos[1] + directions[direction.lower()][1]
            if row < 0:
                print(parsedcode.strip()) # debug
                raise SyntaxError(f'Hit the border at {(row, col)} without an end statement!')
            if col < 0:
                print(parsedcode.strip()) # debug
                raise SyntaxError(f'Hit the border at {(row, col)} without an end statement!')
        return (row, col)
    while not ended:
        try:
            parsedcode += code[row][col]
        except IndexError:
            if parsedcode.strip().endswith('end:<>'):
                ended = True
            else:
                print(parsedcode.strip()) # debug
                raise SyntaxError(f'Hit the border at {(row, col)} without an end statement!')
        if parsedcode[-1] == "→":
            lastdirect = 'right'
        elif parsedcode[-1] == "↓":
            lastdirect = 'down'
        elif parsedcode[-1] == "←":
            lastdirect = 'left'
        elif parsedcode[-1] == "↑":
            lastdirect = 'up'
        row, col = move((row, col), lastdirect)
        print(f'({row}, {col}): {parsedcode[-1]} (ended: {ended})') # debug
    return parsedcode

parsedcode_2 = parsecode(parsedcode_1)
print(parsedcode_2) # debug
parsedcode_3 = parsedcode_2.replace("←", ";\n").replace("↑", ";\n").replace("↓", ";\n").replace("→", ";\n").split(";\n") # debug
for line in parsedcode_3: # debug
    print(line.strip(), end=";") # debug
print() # debug
exit()
