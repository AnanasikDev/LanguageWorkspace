from utils import *

def is_verb(line):
    de_en = line.split(" - ")
    comps = line.split(" ")
    if ("to " in de_en[1]):
        return True
    elif ((comps[0].endswith("en") or comps[0].endswith("ln") or comps[0].endswith("rn")) and ("ться " in comps[1] or "ть " in comps[1])):
        return True
    elif (comps[0] == "sich"):
        return True
    elif (comps[0][0] == "("):
        return True
    return False

def parse_verb(line):
    global irr_colorid
    prefixes = ['']
    cases = ['']
    if line[0] == "(":
        p = line.split(")")
        prefstring = p[0][1::]
        prefixes += prefstring.split(", ")
        rest = line.split(")")[1]
    else:
        rest = line
    
    isreflexive = False
    if (rest.startswith("sich")):
        isreflexive = True
        forms3 = rest.split(" - ")[0].split(" ")[1::]
    else:
        forms3 = rest.split(" - ")[0].split(" ")
    
    _forms3 = []
    for i in range(len(forms3)):
        if forms3[i].isalpha() and forms3[i].islower():
            _forms3.append(forms3[i])
    forms3 = _forms3

    translation = rest.split(" - ")[1]
    allde = rest.split(" - ")[0]

    isreg = len(forms3) != 3

    return isreg, translation, forms3, allde, isreflexive, prefixes, cases

def process_irrverb(line, colorifyGroups):
    global irr_colorid
    isreg, trans, forms3, allde, reflexive, prefixes, cases = parse_verb(line)

    def need2AddGe(infinitive):
        for prefix in ["be", "emp", "ent", "er", "ge", "miss", "ver", "zer"]:
            if infinitive.startswith(prefix):
                return False
        if infinitive.endswith("ieren"):
            return False
        return True

    transvars = trans.split("; ")
    if isreg or len(transvars) != len(prefixes):
        return
    
    forms = []

    def _colorify(text):
        return ifcolorify(text, colors[irr_colorid], colorifyGroups)

    def make3form(inf, f3, pref):
        if need2AddGe(inf):
            return pref + f3
        if f3.startswith("ge"):
            return pref + f3[2::]
        return pref + f3

    def make2form(inf, f2, pref):
        if need2AddGe(inf):
            return f2 + " " + pref
        return pref + f2
    
    if len(prefixes) == 1:
        forms.append([])
        forms[-1].append(transvars[0])
        forms[-1].append(("sich " if reflexive else "") + forms3[0])
        forms[-1].append(forms3[1])
        forms[-1].append(forms3[2])
    
    else:
        for i in range(0, len(prefixes)):
            forms.append([])
            forms[-1].append(_colorify(transvars[i]))
            forms[-1].append(_colorify(("sich " if reflexive else "") + prefixes[i] + forms3[0]))
            forms[-1].append(_colorify(make2form(prefixes[i] + forms3[0], forms3[1], prefixes[i])))
            forms[-1].append(_colorify(make3form(prefixes[i] + forms3[0], forms3[2], prefixes[i])))
        irr_colorid = repeat(irr_colorid+1, 3, len(colors)-1)
    
    return [[word.strip() for word in line] for line in forms]

def process_regverb(line, colorifyGroups):
    global reg_colorid
    isreg, trans, forms3, allde, reflexive, prefixes, cases = parse_verb(line)

    result = []

    transvars = trans.split("; ")

    if not isreg or len(forms3) == 0 or len(transvars) != len(prefixes):
        return
    
    col = colorifyGroups
    if len(prefixes) <= 1:
        col = False

    def _colorify(text):
        if col:
            return colorify(text, colors[reg_colorid])
        return text
    
    f = str(allde)
    for p in range(len(prefixes)):
        result.append([_colorify(str(prefixes[p]) + str(f)), _colorify(transvars[p])])
    
    reg_colorid = repeat(reg_colorid+1, 3, len(colors)-1)
    return result