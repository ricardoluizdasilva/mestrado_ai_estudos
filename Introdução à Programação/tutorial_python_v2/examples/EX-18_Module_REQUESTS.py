#!/usr/bin/python3
#coding: utf-8

# Module REQUETS

import os, requests

os.system("clear")

x_search = input("Please enter a search term: ")
x_term_search = "https://itunes.apple.com/search?term="+x_search+"&entity=album"
x_request = requests.get(x_term_search)
x_json = x_request.json()

print("The search resturned", x_request.text.count(x_search), " results.")
for x in x_json["results"]:
    print("Artist", x["artistName"], " - Album:", x["collectionCensoredName"], " - Track Count:", x["trackCount"])
