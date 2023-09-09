from linesanalysis import *

file = open("database.txt")
lines = file.read().split("\n")
lines = list(filter(lambda l: not ignore_lines(l), lines))

result = []

space = "⠀"
dash = "—"

PLAIN = False

index = 1
def add(line):
    global index, result
    if PLAIN:
        result.append(line)
    else:
        result.append(colorify(f"{index} ".ljust(5, "⠀"), "#999AAB") + line)
    index += 1

def parse(line):
    irrverb = process_irrverb(l, IRRVERBS_COLORIFY and not PLAIN)
    if irrverb is not None:
        for i in irrverb:
            deutsch = i[1] + space + i[2] + space + i[3] + f"{space}{dash}{space}"
            english = i[0]
            add(deutsch + english)
        return
    
    regverb = process_regverb(l, REGVERBS_COLORIFY and not PLAIN)
    if regverb is not None:
        for i in regverb:
            add(f"{space}{dash}{space}".join(i))
        return

    add(line)

for l in lines:
    parse(l)

write_result("<br>".join(result), "fulllist.md")
write_result("\n".join(result), "fulllist.txt")
