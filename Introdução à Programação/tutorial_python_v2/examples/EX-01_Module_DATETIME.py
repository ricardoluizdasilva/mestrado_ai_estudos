#!/usr/bin/python3
#coding: utf-8

# Module DATETIME

import os
from datetime import datetime

def my_first_function(birthdate):
    "Function to calculate the age after getting the birth date"
    today = datetime.today()

    #age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    #return age

    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

name = input("What's your name? ")
birth = str(input("When were you born (yyyy-m-d)? "))
birthdate = datetime.strptime(birth, "%Y-%m-%d")

#age = my_first_function(birthdate)
#print("My name is %s and I am %s years old" %(name,age))

print("My name is %s and I am %s years old" %(name,my_first_function(birthdate)))
