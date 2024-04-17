from databasesorter import *
from random import shuffle, randint
import asyncio

OUTPUT_FILE = "exercise.md"
INPUT_FILE = "db2.txt"

QUESTION_DURATION_SECONDS = 15
QUESTION_NUMBER_PER_SESSION = 10

HIDE_HALF = True  # whether the entire half of line should be hidden

# -1 : random half is chosen
# 0  : left half  (German)
# 1  : right half (English)
HIDE_HALF_INDEX = 0

# duration of breaks between questions
break_duration_seconds = 0.75

hidden_symbol = "____"

# cache
written = "## Exercises\n"

def write(value, mode="a"):
    outputfile = open(OUTPUT_FILE, mode)
    outputfile.write(value)
    outputfile.close()

async def loop(list, i):
    global written
    write(f"{i+1}. " + hide(list[i]) + "<br>\n")
    await asyncio.sleep(QUESTION_DURATION_SECONDS)
    write(written, "w")
    write(f"{i+1}. " + list[i] + "<br>\n")

    written += f"{i+1}. " + list[i] + "<br>\n"
    await asyncio.sleep(break_duration_seconds)


def hide(line):
    if (HIDE_HALF):
        half_index = HIDE_HALF_INDEX
        if (HIDE_HALF_INDEX == -1):
            half_index = randint(0, 1)
        return line.replace(line.split(" - ")[half_index], hidden_symbol)
    parts = line.replace(',', '').replace(' - ', ' ').replace("to ", "").split(" ")
    hidden = parts[randint(0, len(parts)-1)]
    return line.replace(hidden, hidden_symbol)


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


outputfile = open(OUTPUT_FILE, "w")
outputfile.write(written)
outputfile.close()
databasefile = open(INPUT_FILE, "r")

list = generate(QUESTION_NUMBER_PER_SESSION, False, False)
for i in range(QUESTION_NUMBER_PER_SESSION):
    asyncio.run(loop(list, i))
