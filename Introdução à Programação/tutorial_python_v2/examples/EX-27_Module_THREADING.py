#!/usr/bin/python3
#coding: utf-8

# Module threading - parsing arguments to threads

import os, sys
from time import sleep, perf_counter
from threading import Thread

def task(id):
    print(f'Starting the task {id}...')
    sleep(1)
    print('done')


os.system('clear')

start_time = perf_counter()

# create and start 10 threads
threads = []
for n in range(1, 11):
    t = Thread(target=task, args=(n,))
    threads.append(t)
    t.start()

# wait for the threads to complete
for t in threads:
    t.join()

end_time = perf_counter()

print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')
