#!/usr/bin/env python

from random import randint

file = open(r"/media/jam/win11/Archive/School/Deutsch/LanguageWorkspace/database.txt")
lines = file.read().split("\n")

line = lines[randint(0, len(lines)-1)]

def colorify(string, color):
    colors = {"red" : "31", "green" : "32", "yellow" : "33", "pink" : "35", "cyan" : "36"}
    return f"\x1b[1;{colors[color]};41m{string}\x1b[0m\n"

if (line.startswith("der ")):
    print(colorify(line, "cyan"))
if (line.startswith("die ")):
    print(colorify(line, "pink"))
if (line.startswith("das ")):
    print(colorify(line, "green"))
else:
    print(line)