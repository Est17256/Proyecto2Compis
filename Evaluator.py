from Creator import *
from AFD import *
outK = []
out = []
key = []
"""
Function that scann the results of the ATG
"""
def scanner(keywords, token , kt, chars):
    print("scanning")
    key.append(keywords)
    try: 
        if len(kt)!= 0:
            try:
                for i in range(len(kt)):
                    print("entro")
                    infn, ress = AFD(kt[i])
                    outK.append([ress, infn])
                    print("paso")
            except:
                pass
    except:
        pass
    if len(token)!= 0:
        for i in range(len(token)):
            infn, ress = AFD(token[i])
            out.append([ress, infn])
    textoA="C:/Users/lcest/Desktop/Proyecto2Final/ari.txt"
    print("paso")
    doc = reads(textoA)
    eval(doc)
"""
Function that open the file to comprobate
"""
def reads(ts):
    print("reads")
    fls = open(ts, "r")
    flsL = []
    for i in fls:
        flsL.append(i)
    fls.close()
    return flsL
"""
Function that evaluate the instructions of the ATG
"""
def eval(vals):
    for i in range(len(vals)):
        lns = vals[i].split(" ")
        for j in range(len(lns)):
            temp1 = 0
            temp2 = 0
            try:
                if len(lns)-1 == j and lns[j][-1] == "\n":
                    temp3 = 0
                    kys = 0
                    tkss = 0
                    temp4 = lns[j].replace("\n", "") 
                    if temp4 in key[0]:
                        print("Key: "+temp4)
                        kys+=1
                    else:
                        for k in range(len(outK)):
                            sols = read_AFD(temp4, outK[k][0],outK[k][1])
                            if sols == True:
                                tkss +=1
                            sols2 = read_AFD("\n", outK[k][0],outK[k][1])
                            if sols2 == True:
                                temp3 +=1
                    for r in range(len(out)):  
                        temp4 = lns[j].replace("\n", "")
                        sols = read_AFD(temp4, out[r][0],out[r][1])
                        if sols == True:
                            tkss +=1
                        sols2 = read_AFD("\n", out[r][0],out[r][1])
                        if sols2 == True:
                            temp3 +=1
                    if tkss == 0 and kys == 0:
                        print("BAD: "+temp4)
                    elif kys == 0 and tkss >=1:
                        print("Token: "+temp4)
                    if sols2 == False:
                        print("BAD.")
                    elif sols2 == True:
                            print("Token: New Line")
                else:
                    try:
                        if lns[j] in key[0]:
                            print("Key: "+lns[j])
                            temp2+=1
                        else:  
                            for s in range(len(outK)):
                                sols = read_AFD(lns[j], outK[s][0],outK[s][1])
                                if sols == True:
                                    temp1 +=1
                    except:
                        pass
                    for u in range(len(out)):
                            sols = read_AFD(lns[j], out[u][0],out[u][1])
                            if sols == True:
                                temp1 +=1
                    if temp1 >=1:
                        print("Token: "+lns[j])
                    elif temp2 >=1:
                        pass
                    else:
                        print("BAD: "+lns[j])
            except:
                pass