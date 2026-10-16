#!/usr/bin/python3
#coding: utf-8

# Module Pandas - read json

import os, pandas as pd

os.system('clear')

df = pd.read_json('grades.json')
print(df.to_string())
