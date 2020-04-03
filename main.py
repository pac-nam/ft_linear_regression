#!/usr/bin/python3

import pandas
import sys

def training(file_name):
	teta0, teta1, cars_number = 0, 0, 0
	csv = pandas.read_csv(file_name, delimiter=',')
	if len(csv.columns) != 2:
		return 0, 0, "invalid file"
	try:	csv.km
			csv.price
	except AttributeError as error:
		print("lol", error)
	print(csv.km)
	cars_number = len(csv)
	return 0, 0, ""

def save_teta(teta0, teta1):
	print("tetas will be saved here")

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage:", sys.argv[0], "<file1>")
		sys.exit(0)
	teta0, teta1, error = training(sys.argv[1])
	if error != "":
		print(error)
		sys.exit(0)
	save_teta(teta0, teta1)
