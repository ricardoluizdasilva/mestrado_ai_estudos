#!/usr/bin/python3
#coding: utf-8

# Module BEAUTIFULSOUP

import requests
from bs4 import BeautifulSoup

r = requests.get("https://www.nbcnews.com/tech/cyber-security")
soup = BeautifulSoup(r.text)

for title in soup.find_all("h3"):
    print(title.text)