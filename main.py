#!/usr/bin/python3

import pandas as pd
import sys
import csv
import sys
import matplotlib.pyplot as plt

def derivate_t1(data, t0, t1):
	dt1 = 0
	for car in data.itertuples():
		dt1 += car.km * (t1 * car.km + t0 - car.price)
	return (dt1 / len(data))

def derivate_t0(data, t0, t1):
	dt0 = 0
	for car in data.itertuples():
		dt0 += t1 * car.km + t0 - car.price
	return (dt0 / len(data))

def cost(t0, t1, df):
	cost = 0
	for car in df.itertuples():
		cost += (t1*car.km + t0 - car.price)**2
	cost_final = 1/(2*len(df)) * cost
	return(cost_final)

def estimate_price(km, theta0, theta1):
	print("theta0 = {} et theta1 = {}".format(theta0, theta1))
	return (km * theta1 + theta0)

def normalize_data(csv):
	return(pd.DataFrame({"km": csv.km / csv.km.max(), "price": csv.price / csv.price.max()}), csv.price.max())
	# (price - min(price)) / (max(price) - min(price))

def training(file_name):
	data = pd.read_csv(file_name, delimiter=',')
	cars_nb = len(data)
	if len(data.columns) != 2:
		return 0, 0, "invalid file"
	if (cars_nb == 0):
		return (0,0, "No car")
	# print(csv)
	data, max_price = normalize_data(data)
	max_iter = 1000
	learning_rate = 0.01
	precision = 0.0001
	cost_min = float(sys.maxsize)
	t0 = 0
	t1 = 0
	last_cost = 0
	current_cost = 0
	for i in range(max_iter):
		tmpt0 = t0
		t0 -= learning_rate*derivate_t0(data, t0, t1)
		t1 -= learning_rate*derivate_t1(data, tmpt0, t1)
		# print("Deriv t0 = {} and Deriv t1 = {}".format(derivate_t0(data, t0, t1), derivate_t1(data, t0, t1)))
		current_cost = cost(t0, t1, data)
		if (abs(last_cost - current_cost) < precision):
			break
		last_cost = current_cost
	return(t0*max_price, t1, "")

def plot_graph(t0, t1, data):
	fig = plt.figure()
	plt.scatter(data.km, data.price)
	plt.plot(data.km, t0 + t1 * data.km)
	plt.xlabel('km')
	plt.ylabel('price')
	plt.savefig("Test.png")

def save_theta(theta0, theta1):
	# print("Theta0 =", theta0, "\nTheta1 =", theta1)
	with open(".save_model.csv", 'w', newline='') as csvfile:
  	  spamwriter = csv.writer(csvfile, delimiter=',')
  	  spamwriter.writerow(["Theta0", "Theta1"])
  	  spamwriter.writerow([theta0, theta1])

if __name__ == "__main__":
	# try :
		if len(sys.argv) != 2:
			print("Usage:", sys.argv[0], "<file1>")
			sys.exit(0)
		theta0, theta1, error = training(sys.argv[1])
		if error != "":
			print(error)
			sys.exit(0)
		save_theta(theta0, theta1)
		theta = pd.read_csv(".save_model.csv", delimiter=',')
		t0 = theta.Theta0[0]
		t1 = theta.Theta1[0]
		print("estimate =",estimate_price(200000, t0,  t1))
		data = pd.read_csv("data.csv", delimiter=',')
		plot_graph(t0, t1, data)

	# except AttributeError as error:
	# 	print("Error system : {}".format(error))
