#!/usr/bin/python3
#coding: utf-8

# Module Pandas - read csv

import os, pandas as pd

os.system('clear')

df = pd.read_csv('samples.csv', index_col=0)
print(df)
