file = open("database.txt")
lines = file.read().split("\n")

colors = ['#BBCCFF', '#FFAABB', '#BBFFCC', "#AAAAFF", "#FFAAAA", "#FFAAFF"]

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

def sort_nouns(lines):
    nouns = []
    for l in lines:
        if l.startswith("der ") or l.startswith("die ") or l.startswith("das "):
            nouns.append(l)
    return nouns

def sort_nouns_gender(lines, order):
    masc = []
    femi = []
    neut = []

    for l in lines[::order]:
        if l.startswith("der "):
            masc.append(l)
        if l.startswith("die "):
            femi.append(l)
        if l.startswith("das "):
            neut.append(l)
    
    return masc, femi, neut

def Sort_Nouns_Gender(colorifyText, showArticle, order):
    output = ""
    output += render_header(["Masculine", "Feminine", "Neutral"])
    mlist, flist, nlist = sort_nouns_gender(lines, order)
    for i in range(max(len(mlist), len(flist), len(nlist))):
        m = mlist[i] if i < len(mlist) else " "
        f = flist[i] if i < len(flist) else " "
        n = nlist[i] if i < len(nlist) else " "
        m = m if showArticle else m[4::]
        f = f if showArticle else f[4::]
        n = n if showArticle else n[4::]
        if (colorifyText):
            output += f"| {colorify(m, colors[0])} | {colorify(f, colors[1])} | {colorify(n, colors[2])} |\n"
        else:
            output += f"| {m} | {f} | {n} |\n"
    return output

def sort_verbs(lines):
    verbs = []
    for l in lines:
        de_en = l.split(" - ")
        comps = l.split(" ")
        if ("to " in de_en[1]):
            verbs.append(l)
        elif (comps[0].endswith("en")):
            verbs.append(l)
        elif (comps[0] == "sich"):
            verbs.append(l)
        elif (comps[0][0] == "("):
            verbs.append(l)
    return verbs

colorid = 0
def sort_irr_verbs(lines, colorifyGroups):
    trs = []
    inf = []
    prt = []
    paz = []

    def need2AddGe(infinitive):
        for prefix in ["be", "emp", "ent", "er", "ge", "miss", "ver", "zer"]:
            if infinitive.startswith(prefix):
                return False
        if infinitive.endswith("ieren"):
            return False
        return True

    def parse_verb(line):
        global colorid
        prefixes = ['']
        reflexives = ['']
        cases = ['']
        if line[0] == "(":
            p = line.split(")")
            prefstring = p[0][1::]
            prefixes += prefstring.split(", ")
            rest = line.split(")")[1]
        else:
            rest = line
        
        reflexive = False
        if (rest.startswith("sich")):
            reflexive = True
            forms3 = rest.split(" - ")[0].split(" ")[1::]
        else:
            forms3 = rest.split(" - ")[0].split(" ")
        
        _forms3 = []
        for i in range(len(forms3)):
            if forms3[i].isalpha() and forms3[i].islower():
                _forms3.append(forms3[i])
        forms3 = _forms3

        trans = rest.split(" - ")[1]

        if len(forms3) != 3:
            return
        
        transvars = trans.split("; ")

        def _colorify(text):
            if colorifyGroups:
                return colorify(text, colors[colorid])
            return text

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
            trs.append(transvars[0])
            inf.append(("sich " if reflexive else "") + forms3[0])
            prt.append(forms3[1])
            paz.append(forms3[2])
        
        else:
            for i in range(0, len(prefixes)):
                trs.append(_colorify(transvars[i]))
                inf.append(_colorify(("sich " if reflexive else "") + prefixes[i] + forms3[0]))
                prt.append(_colorify(make2form(prefixes[i] + forms3[0], forms3[1], prefixes[i])))
                paz.append(_colorify(make3form(prefixes[i] + forms3[0], forms3[2], prefixes[i])))
            colorid = repeat(colorid+1, 3, len(colors)-1)

    verbs = sort_verbs(lines)
    for v in verbs:
        parse_verb(v)
    
    return trs, inf, prt, paz

def Sort_Irregular_Verbs(colorifyGroups):
    output = ""
    output += render_header(["Translation", "Infinitive", "Präteritum", "Partizip II"])
    trs, inf, prt, paz = sort_irr_verbs(lines, colorifyGroups)
    for i in range(len(inf)):
        output += f"| {trs[i]} | {inf[i]} | {prt[i]} | {paz[i]} |\n"
    return output

def Sort_Nouns_Plurals():
    nouns = []
    for l in lines:
        if l.startswith("der ") or l.startswith("die ") or l.startswith("das "):
            nouns.append(l)

def write_result(result, file):
    f = open(file, "w")
    f.write(result)

COLORIFY = True
STRAIGHT = 1
REVERSED = -1

write_result(Sort_Nouns_Gender(COLORIFY, False, order=REVERSED), "nouns.md")
write_result(Sort_Irregular_Verbs(COLORIFY), "irverbs.md")
