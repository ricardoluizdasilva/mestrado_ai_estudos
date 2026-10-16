#!/usr/bin/python3
#coding: utf-8

# Module threading --> thread_list(), thread append, start, join

import os, sys, logging, threading, time

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)

# Clean the screen
os.system('clear')

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")

threads = list()
for index in range(10):
    logging.info("Main     : create and start thread %d.", index)
    x = threading.Thread(target=thread_function, args=(index,))
    threads.append(x)
    x.start()

for index, thread in enumerate(threads):
    logging.info("Main     : before joining thread %d.", index)
    thread.join()
    logging.info("Main     : thread %d done", index)
