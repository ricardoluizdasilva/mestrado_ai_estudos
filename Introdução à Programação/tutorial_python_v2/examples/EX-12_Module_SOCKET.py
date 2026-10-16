#!/usr/bin/python3
#coding: utf-8

# Module SOCKET

# Import module
import os, sys, socket

# Clean the screen
os.system('clear')

HOST = "127.0.0.1"
PORT = 8085

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello ANCIBER!")
    data = s.recv(1024)

print(f"Received {data!r}")
