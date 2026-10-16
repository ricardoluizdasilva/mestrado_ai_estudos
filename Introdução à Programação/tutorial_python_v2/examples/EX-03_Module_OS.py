#!/usr/bin/python3
#coding: utf-8

# Module OS

# Function to clean the screen
def pressenter():
    input ("Type any key to continue")
    os.system('clear')
    return()
    # End the function

# Import module
import os
from datetime import date

# Clean the screen
os.system('clear')

# Get current directory
cwd = os.getcwd()
print ("The current folder is: ", cwd)

pressenter()

# Create Directory
newcd = "dir_test"
print ("Creating the folder " + newcd)
os.mkdir(newcd)

# Change directory
print ("Changing to folder " + newcd)
os.chdir(newcd)
pressenter()
print ("The current folder is: " + os.getcwd())
pressenter()

# Go back to initial directory
print ("Going back to the original folder " + cwd)
os.chdir(cwd)
pressenter()

# Rename directory
print ("Chaning the name of the folder " + newcd + " to dir_test_name")
os.rename(newcd, "dir_test_rename")
pressenter()

# Remove Direcotry
print ("Deleting the folder dir_test_name")
os.rmdir("dir_test_rename")

# End the main program
