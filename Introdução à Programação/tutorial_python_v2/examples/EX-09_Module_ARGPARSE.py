#!/usr/bin/python3
#coding: utf-8

# Module ARGPARSE

# Import module
import os, sys, argparse

# Clean the screen
os.system('clear')

# Setting the args
parser = argparse.ArgumentParser()
parser.add_argument('-n',type=str, help="Name to be provided",action='store', required = True)
parser.add_argument('-a',type=int, help="Age to be provided",action='store', required = True)
args = parser.parse_args()

# Print the message according to the condition
print(f'{args.n} is {args.a} years old!', "Welcome to ANCIBER!" if args.a >= 18 else "You are a minor!")
