#!/usr/bin/python3
#coding: utf-8

# Module RANDOM

import random
import os

os.system("clear")

# Imprime um valor aleatório de uma lista
lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(random.choice(lista))

# Baralha a lista
random.suffle(lista)
print(lista)

# Criar uma lista a partir de uma string
# Baralha a lista
# Imprimi o novo contéudo
texto = "I am your father"
lista = list(texto)
print(lista)
random.shuffle(lista)
print("".join(lista))
