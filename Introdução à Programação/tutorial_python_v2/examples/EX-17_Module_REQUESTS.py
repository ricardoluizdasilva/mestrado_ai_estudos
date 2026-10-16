#!/usr/bin/python3
#coding: utf-8

# Module REQUETS

import os, requests

os.system(clear)

r = requests.get("https://en.wikipedia.org/wiki/Python_(programming_language)")
print(
    f"The word 'Python' is used {r.text.count('Python')} times in its Wikipedia entry!"
)