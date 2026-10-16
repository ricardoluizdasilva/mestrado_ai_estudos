#!/usr/bin/python3
#coding: utf-8

# Module STATISTICS

import statistics
import os

os.system("clear")

# Calcular o a média de um grupo de dados
print(statistics.mean([1, 3, 5, 7, 9, 11, 13]))
print(statistics.mean([1, 3, 5, 7, 9, 11]))
print(statistics.mean([-11, 5.5, -3.4, 7.1, -9, 22]))

# Calcula o desvio padrão de uma dada população
print(statistics.pstdev([1, 3, 5, 7, 9, 11]))
print(statistics.pstdev([2, 2.5, 1.25, 3.1, 1.75, 2.8]))
print(statistics.pstdev([-11, 5.5, -3.4, 7.1]))
print(statistics.pstdev([1, 30, 50, 100]))
