outputpath = "exercise.md"
databasepath = "database.txt"
from databasesorter import *
from random import shuffle, randint
import asyncio

delay = 1
count = 10

written = "## Exercises\n"

def write(value, mode="a"):
    outputfile = open(outputpath, mode)
    outputfile.write(value)
    outputfile.close()

async def loop(list, i):
    global written
    write(f"{i+1}. " + hide(list[i]) + "<br>\n")
    await asyncio.sleep(5)
    write(written, "w")
    write(f"{i+1}. " + list[i] + "<br>\n")

    written += f"{i+1}. " + list[i] + "<br>\n"
    await asyncio.sleep(0.4)


def hide(line):
    parts = line.replace(',', '').replace(' - ', ' ').split(" ")
    hidden = parts[randint(0, len(parts)-1)]
    return line.replace(hidden, "____")


def generate(n, onlynouns=False, onlyverbs=False):
    lines = databasefile.read().split('\n')
    if onlynouns:
        nouns = sort_nouns(lines)
        shuffle(nouns)
        return nouns[:n:]
    elif onlyverbs:
        verbs = sort_verbs(lines)
        shuffle(verbs)
        return verbs[:n:]
    words = lines
    shuffle(words)
    return words[:n:]


outputfile = open(outputpath, "w")
outputfile.write(written)
outputfile.close()
databasefile = open(databasepath, "r")

list = generate(count, False, False)
for i in range(count):
    asyncio.run(loop(list, i))
