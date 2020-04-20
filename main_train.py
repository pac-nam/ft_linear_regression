import sys
import argparse
import csv
import pandas as pd
from plot import *
from training import training

def save_theta(theta0, theta1):
	with open(".save_model.csv", 'w', newline='') as csvfile:
  	  spamwriter = csv.writer(csvfile, delimiter=',')
  	  spamwriter.writerow(["Theta0", "Theta1"])
  	  spamwriter.writerow([theta0, theta1])

def model_train(args, max_iter, learning_rate):
	theta0, theta1, error = training(args, max_iter, learning_rate)
	if error != "":
		print(error)
		return
	save_theta(theta0, theta1)
	theta = pd.read_csv(".save_model.csv", delimiter=',')
	t0 = theta.Theta0[0]
	t1 = theta.Theta1[0]
	data = pd.read_csv(args.file, delimiter=',')
	if args.visualise:
		plot_graph_model(t0, t1, data)

if __name__ == "__main__":
	try :
		max_iter, learning_rate = 1000, 0.1
		parser = argparse.ArgumentParser()
		parser.add_argument("file", help="define our file", type = str)
		parser.add_argument("-m","--maxIter", help="define hyperparameter 'max_iter' (default = 1000)", type = int)
		parser.add_argument("-l","--learningRate", help="define hyperparameter 'learning_rate' (default = 0.1)", type = float)
		parser.add_argument("-v","--visualise", help="define create files model.png and cost.png that represent the graph training result", action="store_true")
		parser.add_argument("-s","--square", help="use the least square method to calculate prediction parameters", action="store_true")
		args = parser.parse_args()
		if args.maxIter:
			max_iter = args.maxIter
		if (args.learningRate):
			learning_rate = args.learningRate
		model_train(args, max_iter, learning_rate)
		print("training complete")

	except AttributeError as error:
		print("Error system : {}".format(error))
