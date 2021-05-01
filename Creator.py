from AFD import *
"""
Function that load the ATG file and distributed
"""
def load(url):
    chrs = []
    keys = []
    toks = []
    temp = []
    wht = 0
    fls = []
    fls2 = open(url, "r")
    for i in fls2.readlines():
        if i[-1:] == "\n":
            fls.append((i[:-1]))
        else:
            fls.append(i)
    fls2.close() 
    for i in fls:
        if i.strip() == "TOKENS":
            wht = 1
        if i.strip() == "CHARACTERS":
            wht = 2
        if i.strip() == "KEYWORDS":
            wht = 3
        if wht == 1:
            toks.append(i)
        if wht == 0:
            temp.append(i)
        if wht == 2:
            chrs.append(i)
        if wht == 3:
            keys.append(i)
    return temp, chrs, keys, toks
"""
Function that make the new python program
"""
def npgm(temp, chrs, keys, toks):
    holis=[]
    keys2=[]
    toks2=[]
    chara=[]
    aut = []
    chars = []
    autk = []
    if temp[0] != "":
        nombre = temp[0].split(" ")
        if nombre[0] == "COMPILER":
            file = open(nombre[1]+".py",'w')
    file.write("from AFD import * ")
    file.write("\n")
    file.write("from Evaluator import *")
    file.write("\n")
    keywordss = []
    for i in range(len(keys)):
        if keys[i].strip() == "KEYWORDS":
            pass
        else:
            if keys[i] != "":
                x = keys[i].split("=")
                y = x[1].replace(chr(34), "")
                y = y.replace(chr(39), "")
                y = y.replace(".", "")
                keywordss.append(y.strip())
    file.write("keywords ="+str(keywordss)+"\n")
    holis.append(["keywords",str(keywordss)])
    keys2.append(["keywords",str(keywordss)])
    for i in range(len(chrs)):
        if chrs[i].strip() == "CHARACTERS":
            pass
        else:
            lst = chrs[i].rfind(".")
            nstr = chrs[i][:lst] + "" + chrs[i][lst+1:]
            if nstr != "":
                # file.write("\n")
                y = nstr.split("=")
                if "chr(" in y[1] or "CHR(" in y[1] :
                    chars.append(y[1].lower())
                    file.write(nstr.lower())
                    chara.append([y[0],nstr.lower()])
                    file.write("\n")
                    file.write(y[0]+"= character("+y[0].strip().lower()+")")
                    file.write("\n")
                elif y[1].strip() == "'A' . 'Z'" or y[1].strip() == "'A' . 'Z'." or y[1].strip()== chr(34)+"A"+chr(34)+ ".." +chr(34)+"Z"+chr(34):
                    y[1]=chr(34)+"ABCDEFGHIJKLMNOPQRSTUVWXYZ"+chr(34)
                    file.write(y[0]+'='+y[1])
                    file.write("\n")
                    file.write(y[0]+"= character("+y[0].strip()+")")
                    chara.append([y[0],y[1]])
                    file.write("\n")
                elif y[1].strip()== "'a' . 'z'" or y[1].strip()== "'a' . 'z'." or y[1].strip()== chr(34)+"a"+chr(34)+ ".." +chr(34)+"z"+chr(34):
                    y[1] =chr(34)+"abcdefghijklmnopqrstuvwxyz"+chr(34)
                    file.write(y[0]+'='+y[1])
                    file.write("\n")
                    file.write(y[0]+"= character("+y[0].strip()+")")
                    chara.append([y[0],y[1]])
                    file.write("\n")
                else:
                    file.write(nstr)
                    file.write("\n")
                    file.write(y[0]+"= character("+y[0].strip()+")")
                    chara.append([y[0],y[1]])
                    file.write("\n")
    if toks[-1][0:3] == "END":
        toks.pop()
    for i in range(len(toks)):
        if toks[i].strip() == "TOKENS":
            pass
        else:
            if len(toks[i]) != 0:
                nstr = lst_str(toks[i],1)
                if nstr[len(nstr)-1] == ".":
                    nstr.pop()
                nstr = lst_str(nstr,0)
                nstr = nstr.strip()
                nstr = nstr.replace(chr(34), "+")
                nstr = nstr.replace("(H)", chr(34)+"H"+chr(34))
                nstr = nstr.replace("(","+"+chr(34)+" ("+chr(34)+"+")
                nstr = nstr.replace(")","+"+chr(34)+")"+chr(34))
                nstr = nstr.replace("|","+"+chr(34)+"|"+chr(34)+"+")
                nstr = nstr.replace(".", chr(34)+". "+chr(34))
                nstr = nstr.replace("{", "+"+chr(34)+" (("+chr(34)+"+")
                nstr = nstr.replace("[", "+"+chr(34)+" (("+chr(34)+"+")
                nstr = nstr.replace("}", "+"+chr(34)+")*) "+chr(34)+"+")
                nstr = nstr.replace("]", "+"+chr(34)+")*) "+chr(34)+"+")
                nstr2 = nstr.split()
                if len(nstr2)>2 and nstr2[len(nstr2)-1] == "KEYWORDS" and nstr2[len(nstr2)-2] == "EXCEPT" :
                     nstr2.pop()
                     nstr2.pop()
                     autk.append(nstr2[0])
                else:
                    aut.append(nstr2[0])
                nstr2 = lst_str(nstr2,0)
                nstr2 = nstr2.split("=")
                nstr2[1]= nstr2[1].replace(")*)", ")*) ")
                if nstr2[1][0]== "+":
                    nstr2[1] = nstr2[1].replace("+","",1)
                if nstr2[1][-1] == "+":
                    nstr2[1] = nstr2[1][:-1]
                temp = lst_str(nstr2[1],1)
                if temp[-2] == " ":
                    temp.pop(len(temp)-2)
                for i in range(len(temp)):
                    if temp[i] == "." or temp[i] == ",":
                        temp.insert(i+1, " ")
                nstr2[1] = lst_str(temp,0)
                rsts = nstr2[0]+"="+lst_str(nstr2[1],0)
                rsts = rsts.replace("((", " ((")
                rsts = rsts.replace("+++", " +")
                rsts = rsts.replace("++", " +")
                rsts = rsts.replace(chr(34)+"("+chr(34), chr(34)+" ("+chr(34))
                temp2 = rsts.split("=")
                if lst_str(temp2[1],1)[1] == " ":
                    x = lst_str(temp2[1],1)
                    x.pop(1)
                    temp2[1] = lst_str(x,0)
                rsts = temp2[0]+"="+lst_str(temp2[1],0)
                rsts2 = temp2[0],lst_str(temp2[1],0)
                file.write(rsts)
                toks2.append([rsts2])
                file.write("\n")
    file.write("autk=" +strL(autk))
    holis.append([strL(autk)])
    file.write("\n")
    file.write("aut ="+strL(aut))
    holis.append([strL(aut)])
    file.write("\n")
    file.write("charss ="+strL(chars))
    holis.append([strL(chars)])
    file.write("\n")
    file.write("scanner(keywords, aut , autk, charss)")
    return keys2,chara,toks2
