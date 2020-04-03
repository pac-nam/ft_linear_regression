#!/usr/bin/python3

import pandas
import sys

def estimate_price(km, theta0, theta1):
	return (km * theta1 + theta0)

def training(file_name):
	t0, t1 = 0, 0
	csv = pandas.read_csv(file_name, delimiter=',')
	if len(csv.columns) != 2:
		return 0, 0, "invalid file"
	cars_number = len(csv)
	if (cars_number == 0):
		return (0,0,"No car")
	for car in csv.itertuples():
		print("t0", t0, "| t1", t1, car)
		if (car.Index == 0):
			tmpt0, tmpt1 = 0, 0
		else:
			tmpt0 = t0 / car.Index
			tmpt1 = t1 / car.Index
		print("tmpt0", tmpt0, "| tmpt1", tmpt1)
		t0 += estimate_price(car.km, tmpt0, tmpt1) - car.price
		t1 -= (estimate_price(car.km, tmpt0, tmpt1) - car.price) / car.km
	t0 = t0 / cars_number
	t1 = t1 / cars_number
	return (t0, t1, "")

def save_theta(theta0, theta1):
	print("Theta0 =", theta0, "\nTheta1 =", theta1)
	print(estimate_price(150000, theta0, theta1))

if __name__ == "__main__":
	try :
		if len(sys.argv) != 2:
			print("Usage:", sys.argv[0], "<file1>")
			sys.exit(0)
		theta0, theta1, error = training(sys.argv[1])
		if error != "":
			print(error)
			sys.exit(0)
		save_theta(theta0, theta1)
	except AttributeError as error:
		print("Error system : {}".format(error))
