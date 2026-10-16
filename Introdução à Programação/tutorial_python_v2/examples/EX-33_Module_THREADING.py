#!/usr/bin/python3
#coding: utf-8

# Module threading - Example no threading

import os, sys
from time import sleep, perf_counter
from threading import Thread

def replace(filename, substr, new_substr):
    print(f'Processing the file {filename}')
    # get the contents of the file
    with open(filename, 'r') as f:
        content = f.read()

    # replace the substr by new_substr
    content = content.replace(substr, new_substr)

    # write data into the file
    with open(filename, 'w') as f:
        f.write(content)

# Clean the screen
os.system('clear')

def main():
    filenames = [
        'file1.txt',
        'file2.txt',
        'file3.txt',
        'file4.txt',
        'file5.txt',
        'file6.txt',
        'file7.txt',
        'file8.txt',
        'file9.txt',
        'file10.txt',
    ]

    for filename in filenames:
        replace(filename, 'ID', 'IDS NAME')

if __name__ == "__main__":
    start_time = perf_counter()

    main()

    end_time = perf_counter()
    print(f'It took {end_time- start_time :0.2f} second(s) to complete.')

