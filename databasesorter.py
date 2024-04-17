from linesanalysis import *
from Settings import *
#import fulllist

# ========------=========
# -------- Code ---------
# ========------=========dd2123

#file = open("db2.txt", encoding="utf-8")
file = open("db2.txt")
lines = file.read().split("\n")
lines = list(filter(lambda l: not ignore_lines(l), lines))

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

def sort_irr_verbs(lines, colorifyGroups):
    trs = []
    inf = []
    prt = []
    paz = []

    verbs = list(filter(is_verb, lines))
    for v in verbs:
        forms = process_irrverb(v, colorifyGroups)
        if forms == None:
            continue
        print(forms)
        trs.append(forms[0])
        inf.append(forms[1])
        prt.append(forms[2])
        paz.append(forms[3])

    return trs, inf, prt, paz

def Sort_Irregular_Verbs(colorifyGroups):
    output = ""
    output += render_header(["Translation", "Infinitive", "Praeteritum", "Partizip II"])
    trs, inf, prt, paz = sort_irr_verbs(lines, colorifyGroups)
    for i in range(len(inf)):
        output += f"| {trs[i]} | {inf[i]} | {prt[i]} | {paz[i]} |\n"
    return output

def sort_reg_verbs(lines, order):
    result = []

    verbs = list(filter(is_verb, lines[::order]))
    for v in verbs:
        process_regverb(v, REGVERBS_COLORIFY)
    
    return result

def Sort_Regular_Verbs(order):
    output = render_header(["En/Ru", "Deutsch"])
    verbs = sort_reg_verbs(lines, order)
    for i in range(len(verbs)):
        output += f"|{verbs[i][0]}|{verbs[i][1]}|\n"
    return output


#write_result(Sort_Regular_Verbs(REGVERBS_ORDER), "regverbs.md")
write_result(Sort_Nouns_Gender(NOUNS_GENDER_COLORIFY and COLORIFY, NOUNS_GENDER_SHOW_ARTICLE, NOUNS_GENDER_ORDER), "nouns.md")
#write_result(Sort_Irregular_Verbs(IRRVERBS_COLORIFY and COLORIFY), "irverbs.md")