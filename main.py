import os
from Creator import *
textoA="C:/Users/lcest/Desktop/Proyecto2Final/Aritmetica.atg"
texto = open(textoA, "r")
antes, character, keywords, tokens = load(textoA)
npgm(antes, character, keywords, tokens)
nombre = antes[0].split(" ")
print(nombre)
os.system('python '+nombre[1]+'.py')