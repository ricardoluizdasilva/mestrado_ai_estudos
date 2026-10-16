#!/usr/bin/python3
#coding: utf-8

# Module threading --> ThreadPoolExecutor

import os, sys, logging, threading, time, concurrent.futures

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)

# Clean the screen
os.system('clear')

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    executor.map(thread_function,range(10))
