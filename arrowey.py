#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sys import argv as args, exit
def argument(argument_to_search_for):
    if not argument_to_search_for in args:
        for arg in args:
            if arg[0:len(argument_to_search_for)+1] == argument_to_search_for+":":
                return arg.split("=", 1)[1]
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
parsedcode_1 = list("") # Make an array out of the code so every character can be accessed like `parsedcode_2[line][char]`
for line in arrcode.split("\n"):
    parsedcode_1.append(line.ljust(longest))

newlinestring = '\n'
print(f'parsedcode_1: {newlinestring.join(parsedcode_1)}') # debug

# Loops and conditionals: maybe with if:(condition)→{code}[→{code}] and loops also like that (second part of conditional/loop optional)?

def parsecode(code):
    """
Parser function. Is as function so you can parse code later on.
"""
    ended = False
    parsedcode = ''
    lastdirect = 'right'
    row, char = 0, 0 # Current "playhead" position
    # Move down: row+=1; Move up: row-=1; Move left: char-=1; Move right: char+=1
    def move(pos, direction=...):
        directions = {'right':(0,1), 'down':(1,0), 'left':(0,-1), 'up':(-1,0)} # Relative positions
        if direction.lower() in ('right', 'down', 'left', 'up'):
            row = pos[0] + directions[direction.lower()][0]
            char = pos[1] + directions[direction.lower()][1]
        return (row, char)
    while not ended:
        parsedcode += code[row][char]
        if parsedcode.endswith('end:<>'):
            ended = True
        if parsedcode[-1] == "→":
            lastdirect = 'right'
        elif parsedcode[-1] == "↓":
            lastdirect = 'down'
        elif parsedcode[-1] == "←":
            lastdirect = 'left'
        elif parsedcode[-1] == "↑":
            lastdirect = 'up'
        row, char = move((row, char), lastdirect)
        print(f'({row}, {char}): {parsedcode[-1]} (ended: {ended})') # debug
    return parsedcode

parsedcode_2 = parsecode(parsedcode_1)
print(parsedcode_2) # debug
exit()