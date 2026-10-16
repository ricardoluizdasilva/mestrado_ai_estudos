#!/usr/bin/python3
#coding: utf-8

# Module ARGPARSE

# Function valid date input
def valid_input_date(b):
    try:
        return(datetime.strptime(b,'%Y-%m-%d'))
    except ValueError:
        err_msg = "not a valid date: {0!r}".format(b) + "! The valid date format is yyyy-m-d!"
        raise argparse.ArgumentTypeError(err_msg)

# Function to calculate the age
def my_first_function(birthdate):
    "Function to calculate the age after getting the birth date"
    global birth
    today = datetime.today()
    birth = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return birth

# Import module
import os, sys, argparse
from datetime import datetime

# Clean the screen
os.system('clear')

# Setting the args
parser = argparse.ArgumentParser(description='Age validation')
parser.add_argument('-n',type=str, help="Name" ,action='store', required = True)
parser.add_argument('-b',type=lambda b: datetime.strptime(b,'%Y-%m-%d'), help="Birth date (yyyy-m-d)",action='store', required = True)
# parser.add_argument('-b',type=valid_input_date, help="Birth date (yyyy-m-d)",action='store', required = True)
args = parser.parse_args()

# Print the message according to the conditions
print(f'{args.n} is {my_first_function(args.b)} years old!', "Welcome to ANCIBER!" if birth >= 18 else "You are a minor!")
