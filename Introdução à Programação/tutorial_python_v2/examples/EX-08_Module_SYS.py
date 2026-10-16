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

try:
    age = int(sys.argv[1])
    if age < 18:
        print("You are under 18!")
    else:
        print("Welcome to ANCIBER")
except:
    print("Invalid argument! Provide an integer")
