#!/usr/bin/python3
#coding: utf-8

# Module Pandas - create json

import os, pandas as pd

os.system('clear')

data = {
    "Name": {
		"0":"Marina",
		"1":"Andre",
		"2":"Carlos",
		"3":"David",
		"4":"Adriana",
		"5":"Carina",
		"6":"Alice",
		"7":"Roberta",
		"8":"Carlos",
		"9":"Eduardo",
		"10":"Maria",
		"11":"Roberto"
	},
	"Age": {
		"0":24,
		"1":42,
		"2":24,
		"3":38,
		"4":24,
		"5":30,
		"6":24,
		"7":42,
		"8":18,
		"9":68,
		"10":24,
		"11":30
	},
    "Location": {
		"0":"Porto",
		"1":"Lisbon",
		"2":"Faro",
		"3":"Setubal",
		"4":"Leixoes",
		"5":"Faro",
		"6":"Beja",
		"7":"Coimbra",
		"8":"Viseu",
		"9":"Porto",
		"10":"Lisbon",
		"11":"Setubal"
	},
	"Grade": {
		"0":64,
		"1":92,
		"2":70,
		"3":70,
		"4":88,
		"5":67,
		"6":64,
		"7":92,
		"8":70,
		"9":70,
		"10":88,
		"11":57
	}
  }

df = pd.DataFrame(data)
print(df)

df.to_json(r'grades.json', orient='records')
