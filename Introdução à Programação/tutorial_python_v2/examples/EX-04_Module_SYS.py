#!/usr/bin/python3
#coding: utf-8

# Module SYS - stdin function

# Import module
import os, sys

# Clean the screen
os.system('clear')

# Main program
for line in sys.stdin:
    if 'q' == line.rstrip() or 'Q' == line.rstrip():
        break
    print(f'Input: {line}')
print("Exit")
