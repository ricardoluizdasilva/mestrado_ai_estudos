#!/usr/bin/python3
#coding: utf-8

# Module Pandas - data frames

import os, pandas as pd
import pdb

os.system('clear')

mydataset = {
    'linux': ["Kali", "Xubuntu", "Fedora", "RedHat", "Suse", "Ubuntu"],
    'score': [1, 2, 3, 4, 5, 6]
}

myvar = pd.DataFrame(mydataset)

print("Panda Version is", pd.__version__)
print(myvar)
