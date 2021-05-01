# from funciones import * 
from operator import itemgetter
import os
"""
Function that clean the "()" for concatenation and compact in "[]"
"""
def clean(y, c):
    temp = []
    for i in y:
        if isinstance(i, list):
            clean(i, c)
        else:
            c.append(i)
    
    for i in range(0,len(c),3):
        if i != len(c):
            temp.append([c[i],c[i+1],c[i+2]])
    
    return temp
"""
Function that make the thomson construction with the postfix
"""
def AFN(posF):
    n=2
    i = 0
    infin = []
    temp = []
    while i < len(posF):
        #Make Klee
        if posF[i] == "*":
            fst = infin[-1][0]
            lst = infin[-1][1]
            x1 = [n, "e", fst]
            y1 = [lst, "e", fst]
            fst = n
            n +=1
            x2 = [lst, "e", n]
            y2 = [fst, "e", n]
            lst = n
            x3 = temp[-1]
            temp.pop()
            temp.append([x3,x1,y1,x2,y2])
            infin.pop()
            infin.append([fst, lst])
            n += 1
        #Make the OR
        elif posF[i] == "|":
            x = temp[-1]
            temp.pop()
            y = temp[-1]
            temp.pop()
            temp.append([x,y, [n,"e", infin[-2][0]],[n,"e",infin[-1][0]],[infin[-2][1],"e",n+1],[infin[-1][1],"e",n+1]])
            fst = n
            lst = n +1
            n +=2
            infin.pop()
            infin.pop()
            infin.append([fst,lst])
        #Make Concatenation
        elif posF[i] == " ":
            x = temp[-1]
            temp.pop()
            y = temp[-1]
            temp.pop()
            temp3 = infin[-1]
            infin.pop()
            temp2 = infin[-1]
            infin.pop()
            try:
                 y = clean(y, [])
                 for a in range(len(y)):
                     for n in range(0,3):
                         if y[a][n] == temp2[1]:
                             y[a][n] = temp3[0]                
            except:
                for a in range(len(y)):
                    if y[a] == temp2[1]:
                        y[a] = temp3[0]
            infin.append([temp2[0], temp3[1]])
            temp.append([y, x])
        elif posF[i] != " " and posF[i] != "|" and posF[i] != "*" :
            temp.append([n, posF[i], n+1])
            infin.append([n, n +1])
            n +=2
        i+=1
    thsm = sorted(clean(temp,[]), key= itemgetter(0))
    return thsm, infin
"""
Function that says the moves with epsilon
"""
def eclosure(x, sub):
    if isinstance(x, int):
        nodes = []
        nodes.append(x)
    else: 
        nodes = list(x)
    if isinstance(nodes, list):
        for n in nodes:
            move = movesP(n, "e", sub)
            for x in move:
                if x[2] not in nodes:
                    nodes.append(x[2])
    it = set()
    for item in nodes:
        it.add(item)
    return it
"""
Function that calc the moves of the chain
"""
def movesP(nodes,chn, sub):
    moves = []
    for n in sub:
        if n[0] == nodes and n[1] == str(chn):
            moves.append(n) 
    return moves
"""
Function that move the part of the chain for a expression
"""
def move(nodes, chn, sub):
    nodes = list(nodes)
    moves = []
    if isinstance(nodes, list):
        for i in range(len(nodes)):
            move = movesP(nodes[i], chn, sub)
            for j in move:
                if j[2] not in moves:
                    moves.append(j[2])
        it = set()
        for item in moves:
            it.add(item)
        return it
    else:
        move = movesP(nodes, chn, sub)
        for x in move:
            if x[2] not in moves:
                moves.append(x[2])      
        it = set()
        for item in moves:
            it.add(item)
        return it
"""
Function to convert list to string or string to list
"""
def read_AFD(chn, sub,infin):
    i = 0
    frt = infin[0][0]
    for n in chn:
        x = move2(frt, n, sub)
        if len(x)==0:
            return False
        x = list(x)
        frt = x[0]
    i = 0 
    for n in range(len(infin)):
        if frt == infin[n][1]:
            i += 1
    if i !=0:
        return True
    else:
        return False
"""
Function that move the part of the chain for a expression
"""
def move2(nodes, chn, sub):
    if isinstance(nodes, list):
        nodes = list(nodes)
    else:
        nodes = [nodes]
    moves = []
    if isinstance(nodes, list):
        for i in range(len(nodes)):
            move = movesP(nodes[i], chn, sub)
            for j in move:
                if j[2] not in moves:
                    moves.append(j[2])
        it = set()
        for item in moves:
            it.add(item)
        return it
    else:
        move = movesP(nodes, chn, sub)
        for x in move:
            if x[2] not in moves:
                moves.append(x[2])      
        it = set()
        for item in moves:
            it.add(item)
        return it
     
"""
Function that convert the thomson results to subsets for AFD
"""
def dfa_nfa(thsm, infin):
    infin2 =[]
    infin3 = []
    states =[]
    subs = []
    states.append(eclosure(infin[0][0], thsm))
    infin2.append(eclosure(infin[0][0], thsm))
    vals = []
    ltss = ["A","B","C","D","E","F","G","H","I","J","k","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
            "AA","BB","CC","DD","EE","FF","GG","HH","II","JJ","KK", "LL", "MM", "NN", "OO", "PP", "QQ", "RR", "SS",
            "TT", "QQ", "RR", "SS", "TT", "UU", "VV", "WW", "XX", "YY", "ZZ"]
    vns = [1,2,3,4,5,6,7,8,9]
    nodeV = []
    for i in range(len(vns)):
        for j in range(len(ltss)):
            temp2 = str(ltss[j]) + str(vns[i])
            nodeV.append(temp2)
    for i in range(len(thsm)):
        if thsm[i][1] != "e":
            if thsm[i][1] not in vals:
                vals.append(thsm[i][1])
    i = 0
    while i < len(states):
        for n in vals:
            temp1 = eclosure(move(states[i],n,thsm),thsm)
            subs.append([states[i],n,temp1])
            for j in infin:
                if j[1] in temp1:
                    infin2.append(temp1)
            if temp1 not in states and temp1 is not None:
                states.append(temp1)         
        i+=1
    i = 0
    while i < len(subs):
        if subs[i][0] == set() or subs[i][2] == set():
            subs.pop(i)
            i-=1
        i +=1
    i = 0 
    while i < len(subs):
        temp = states.index(subs[i][0])
        subs[i][0] = nodeV[temp]
        temp = states.index(subs[i][2])
        subs[i][2] = nodeV[temp]
        i +=1
    i = 0
    while i < len(infin2):
        temp = states.index(infin2[i])
        infin2[i]= nodeV[temp]
        i+=1
    for i in range(1,len(infin2)):
        infin3.append([infin2[0],infin2[i]])
    return subs, infin3
"""
Function to convert list to string or string to list
"""
def lst_str(val,opc):
    if opc==0:
        temp = ''
        for i in range(0, len(val)):
            temp = temp + str(val[i])
        return temp
    elif opc==1:
        i = 0
        temp = []
        while i< len(val):
            temp.append(val[i])
            i+= 1
        return temp   
"""
Function that combines the nodes with transitions
""" 
def strL(val):
    temp = []
    temp.append("[")
    for i in range(len(val)):
        temp.append(val[i])
        if i != len(val)-1:
            temp.append(",")
    temp.append("]")
    
    return lst_str(temp,0)
"""
Function to append values in characters
"""
def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result
"""
Function that transforms words in charactes
"""
def character(vals):
    vals = lst_str(vals,1)
    flag = False
    temp = []
    for i in vals:
        if i == "(":
            flag = True
    if flag == False:
        vals = lst_str(vals,1)
        vals = intersperse(vals, '|')
        vals =  lst_str(vals,1)
        vals.append(")")
        vals.insert(0,"(")
        return lst_str(vals,0)
    flag2 = False
    if flag == True:
        temp = []
        for i in vals:
            if i == "(":
                flag2 = True
            if i == ")":
                flag2 = False
                
            if flag2 == True:
                if i == "(" or i == ")":
                    pass
                else:
                    temp.append(i)
            if flag2 == False:
                if i == ")":
                    pass
                else:
                    temp.append(i)
                temp.append("|")
        if temp[len(temp)-1] == "|":
            temp.pop()
        if temp[len(temp)-1] == " ":
            temp.pop()
            temp.pop()
        # print(temp)
        temp.append(")")
        temp.insert(0,"(")
        return lst_str(temp,0)
"""
Function to measure the value of precedence
"""
def precedence(opr):
    if opr == "(":
        return 3
    elif opr == '*':
        return 3
    elif opr == '|':
        return 2
    elif opr == " ":
        return 1
    else:
        return 0
"""
Function that convert the ready expression to postfix
Search through the () ​​to find the operators and values
"""
def postfix(expression):
    temp = []
    oprs = []
    temp2 = []
    i = 0
    #Search in the expression ( to add the operators
    while i < len(expression):
        if expression[i] == "(":
            temp.append(expression[i])
        elif expression[i] == ")":
            x = len(temp) - 1
            while temp[x] != "(":
                if len(temp2) != 0:
                    oprs.append(lst_str(temp2,0))
                    temp2 = []
                oprs.append(temp[x])
                temp.pop()
                x -= 1
            temp.pop()
        elif expression[i] =="|" or expression[i] =="*" or expression[i] ==" ":
            if len(temp) == 0:
                temp.append(expression[i])
                if len(temp2) != 0:
                    oprs.append(lst_str(temp2,0))
                    temp2 = []
            else:
                if temp[-1] != '(':
                    if precedence(expression[i]) < precedence(temp[-1]):
                        x = len(temp) - 1
                        if x != 0:
                            while temp[x] != '(':
                                if len(temp2) != 0:
                                    oprs.append(lst_str(temp2,0))
                                    temp2 = []
                                oprs.append(temp[-1])
                                temp.pop()
                                x -= 1
                            temp.append(expression[i])
                        else:
                            if len(temp2) != 0:
                                oprs.append(lst_str(temp2,0))
                                temp2 = []
                            oprs.append(temp[-1])
                            temp.pop()
                            temp.append(expression[i])
                    elif precedence(expression[i]) >= precedence(temp[-1]):
                        if len(temp2) != 0:
                            oprs.append(lst_str(temp2,0))
                            temp2 = []
                        temp.append(expression[i])
                else:
                    if len(temp2) != 0:
                        oprs.append(lst_str(temp2,0))
                        temp2 = []
                    temp.append(expression[i])
        else:
            temp2.append(expression[i])
        i += 1
    if len(temp2) != 0:
        oprs.append(lst_str(temp2,0))
    if len(temp) != 0:
        for i in range(len(temp)):
            oprs.append(temp[-1])
            temp.pop()
    return oprs
"""
Function that combine the results of AFN to AFD
"""
def AFD(nws):
    temp = postfix(nws)
    res, infin = AFN(temp)
    res2, infin2 = dfa_nfa(res, infin)
    return infin2, res2
    