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
    masc = []
    femi = []
    neut = []

    for l in lines:
        if l.startswith("der "):
            masc.append(l)
        if l.startswith("die "):
            femi.append(l)
        if l.startswith("das "):
            neut.append(l)
    
    return masc, femi, neut

def Sort_Nouns_Gender(colorifyText, showArticle):
    output = ""
    output += render_header(["Masculine", "Feminine", "Neutral"])
    mlist, flist, nlist = sort_nouns(lines)
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

colorid = 0
def sort_verbs(lines, colorifyGroups):
    trs = []
    inf = []
    prt = []
    paz = []

    def parse_verb(line):
        global colorid
        prefixes = ['']
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
        
        if len(prefixes) == 1:
            trs.append(transvars[0])
            inf.append(("sich " if reflexive else "") + forms3[0])
            prt.append(forms3[1])
            paz.append(forms3[2])
        
        else:
            for i in range(0, len(prefixes)):
                trs.append(_colorify(transvars[i]))
                inf.append(_colorify(("sich " if reflexive else "") + prefixes[i] + forms3[0]))
                prt.append(_colorify(prefixes[i] + forms3[1]))
                paz.append(_colorify(prefixes[i] + forms3[2]))
            colorid = repeat(colorid+1, 3, len(colors)-1)

    for l in lines:
        de_en = l.split(" - ")
        comps = l.split(" ")
        if ("to " in de_en[1]):
            parse_verb(l)
        elif (comps[0].endswith("en")):
            parse_verb(l)
        elif (comps[0] == "sich"):
            parse_verb(l)
        elif (comps[0][0] == "("):
            parse_verb(l)
    
    return trs, inf, prt, paz

def Sort_Irregular_Verbs(colorifyGroups):
    output = ""
    output += render_header(["Translation", "Infinitive", "Präteritum", "Partizip II"])
    trs, inf, prt, paz = sort_verbs(lines, colorifyGroups)
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

write_result(Sort_Nouns_Gender(COLORIFY, False), "nouns.md")
write_result(Sort_Irregular_Verbs(COLORIFY), "irverbs.md")
