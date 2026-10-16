#!/usr/bin/python3
#coding: utf-8

# Module threading - explaining join()

import os, sys, logging, threading, time

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)

# Clean the screen
os.system('clear')

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")

logging.info("Main     : before creating thread")
x = threading.Thread(target=thread_function, args=(1,))
#x = threading.Thread(target=thread_function, args=(1,), daemon=True)
logging.info("Main     : before running thread")
x.start()
logging.info("Main     : wait for the thread to finish")
#x.join()
logging.info("Main     : all done")
