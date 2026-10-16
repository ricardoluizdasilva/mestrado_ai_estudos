#!/usr/bin/python3
#coding: utf-8

# Module DATETIME

import calendar
import os

os.system("clear")

# Imprime o dia da semana
# 0 = Monday, 1 = Tuesday, 2 = Wednesday, 3 = Thursday, 4 = Friday, 5 = Saturday, 6 = Sunday
print(calendar.weekday(2022, 12, 26))

# Com a ajuda da calendar.day_name retorna o dia da semana literal
print(calendar.day_name[calendar.weekday(2022, 12, 26)])

# Imprime o calendário de 1 mês específico
calendar.prmonth(2022, 5)

# Imprime o calendário de 1 ano específico
calendar.prcal(2022)

# Verifica se o ano é bissexto
# Entrada de dados
import calendar
n_year = int(input("Qual é o ano que você pretende verificar se é bissexto? "))

# Estas linhas demonstram a lógica passo a passo antes de ter o print feito em uma única "linha" 
"""
day_29 = calendar.day_name[calendar.weekday(n_year, 2, 29)] if (x := calendar.isleap(n_year)) else ""
print(day_29)
check_year = calendar.isleap(n_year)
print(f"The year {n_year}" , "isn't a leap year!" if not check_year 
      else "is a leap year and 29.Feb will be / was on a "+day_29+"!")
"""
print(f"The year {n_year}" , "isn't a leap year!" if not calendar.isleap(n_year) 
      else "is leap year! And 29.Feb will be / was on a " + 
      calendar.day_name[calendar.weekday(n_year, 2, 29)]+"!")
