from Settings import *

irr_colorid = 0
reg_colorid = 0

def ignore_lines(line):
    if line in ["", "\n", "\n\r", "\r\n", "\r", " "]:
        return True
    for c in COMMENTS:
        if line.startswith(c):
            return True
    return False

def write_result(result, file):
    f = open(file, "w")
    f.write(result)

def write_result(result, file):
    f = open(file, "w")
    f.write(result)

def clamp(a, minv, maxv):
    if a < minv:
        return minv
    if a > maxv:
        return maxv
    return a

def repeat(a, minv, maxv):
    if a < minv:
        return maxv
    if a > maxv:
        return minv
    return a

def colorify(string, color):
    return f"<span style=\"color:{color}\">{string}</span>"

def render_header(colomns):
    header = ""
    for c in colomns:
        header += "| " + c
    header += "|\n"

    for c in colomns:
        header += "| - "
    header += "|\n"

    return header
