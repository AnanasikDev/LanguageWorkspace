from linesanalysis import *

file = open("database.txt")
lines = file.read().split("\n")
lines = list(filter(lambda l: not ignore_lines(l), lines))

write_result(str(process_regverb(lines[3], False)), "debug")