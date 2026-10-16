#!/usr/bin/python3
#coding: utf-8

#!/usr/bin/python3
#coding: utf-8

# Module MATH

# 1 - Entrada de dados inteiro
# 2 - Calcular o fatorial do número digitado
# 3 - Calcular os logaritmos natural e de base 10 do número digitado

import math as m
import os

os.system("clear")

numero = int(input("Digite um número: "))
numero_fat = m.factorial(numero)
natural_log = m.log(numero)
log_base_10 = m.log10(numero)

print(numero, "! é ", numero_fat)
print("O logaritmo natural de", numero, "é", natural_log)
print("O logaritmo na base 10 do", numero, "é", log_base_10)
