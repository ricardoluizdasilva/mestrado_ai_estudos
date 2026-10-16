#!/usr/bin/python3
#coding: utf-8

# Module threading - single thread
import os, sys
from time import sleep, perf_counter

def task():
    print('Starting a task...')
    sleep(1)
    print('done')

os.system('clear')

start_time = perf_counter()

task()
task()

end_time = perf_counter()

print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')
