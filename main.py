#!/usr/bin/python3

import pandas as pd
import sys
import csv
import matplotlib.pyplot as plt
from random import *

def estimate_price(km, theta0, theta1):
	return (theta1*km + theta0)

def gradient(data, t0, t1):
	sumt0, sumt1, m = 0, 0, len(data)
	for car in data.itertuples():
		sumt0 += (t0 + (t1 * car.km)) - car.price
		sumt1 += ((t0 + (t1 * car.km)) - car.price) * car.km
	return((1 / m) * sumt0, (1 / m) * sumt1)

def plot_graph_model(t0, t1, data):
	fig = plt.figure()
	plt.scatter(data.km, data.price)
	plt.plot(data.km, estimate_price(data.km, t0, t1), c='r')
	plt.xlabel('km')
	plt.ylabel('price')
	plt.savefig("model.png")

def plot_graph_cost(max_iter, cost_history):
	plt.plot(range(max_iter), cost_history)
	plt.savefig("cost.png")

def cost(t0, t1, df):
	cost, m = 0, len(df)
	for car in df.itertuples():
		cost += (t1*car.km + t0 - car.price)**2
	cost_final = (1/(2*m)) * cost
	return(cost_final)

def normalize_data(csv):
	return((pd.DataFrame({"km": csv.km / csv.km.max(), "price": csv.price / csv.price.max()})), csv.price.max(), csv.km.max())

def training(file_name):
	data = pd.read_csv(file_name, delimiter=',')
	cars_nb = len(data)
	if len(data.columns) != 2:
		return (0, 0, "invalid file")
	if (cars_nb == 0):
		return (0,0, "No car")
	data, max_price, max_km = normalize_data(data)
	max_iter = 1000
	learning_rate = 0.1
	t0 = 0
	t1 = 0
	cost_history = []
	for i in range(max_iter):
		tmpt0, tmpt1 = gradient(data, t0, t1)
		t0 = t0 - (learning_rate * tmpt0)
		t1 = t1 - (learning_rate * tmpt1)
		cost_history.append(cost(t0, t1, data))
	plot_graph_cost(max_iter, cost_history)
	return(t0*max_price, (t1 * max_price) / max_km, "")

def save_theta(theta0, theta1):
	with open(".save_model.csv", 'w', newline='') as csvfile:
  	  spamwriter = csv.writer(csvfile, delimiter=',')
  	  spamwriter.writerow(["Theta0", "Theta1"])
  	  spamwriter.writerow([theta0, theta1])

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
		theta = pd.read_csv(".save_model.csv", delimiter=',')
		t0 = theta.Theta0[0]
		t1 = theta.Theta1[0]
		data = pd.read_csv("data.csv", delimiter=',')
		plot_graph_model(t0, t1, data)

	except AttributeError as error:
		print("Error system : {}".format(error))
