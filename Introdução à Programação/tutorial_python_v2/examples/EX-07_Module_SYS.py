#!/usr/bin/python3
#coding: utf-8

# Module SYS - sys.argv

# Import module
import os, sys

# Clean the screen
os.system('clear')

# Main program
n = len(sys.argv)
if n == 1:
    sys.exit("Please, provide at least 1 argument")

print("Total numbers of arguments passed to the script: ", n)
print("Name of Python script is the argument 0:", sys.argv[0])
print("Arguments passed: ", end = " ")
for i in range(1, n):
    print("\nArgumento: %i " %(i), sys.argv[i], "type: ", type(sys.argv[i]), end = " " )
print("\n")
