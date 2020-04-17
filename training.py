import pandas as pd
import csv
from plot import plot_graph_cost 

def isNaN(num):
    return num != num

def least_square(data):
	t0, t1 = 0, 0
	x, y, x_square, xy, cars_nb = 0, 0, 0, 0, len(data)
	for car in data.itertuples():
		x += car.km
		y += car.price
		x_square += car.km ** 2
		xy += car.km * car.price
	x /= cars_nb
	y /= cars_nb
	xy /= cars_nb
	x_square /= cars_nb

	t1 = abs(xy) - (abs(x) * abs(y))
	t1 /= abs(x_square) - (abs(x) ** 2)
	t0 = abs(y) - t1 * abs(x)
	return (t0, t1, "")

def gradient(data, t0, t1):
	sumt0, sumt1, m = 0, 0, len(data)
	for car in data.itertuples():
		sumt0 += (t0 + (t1 * car.km)) - car.price
		sumt1 += ((t0 + (t1 * car.km)) - car.price) * car.km
	return(sumt0 / m, sumt1 / m)

def cost(t0, t1, df):
	cost, m = 0, len(df)
	for car in df.itertuples():
		cost += (t1*car.km + t0 - car.price)**2
	cost_final = (1/(2*m)) * cost
	return(cost_final)

def normalize_data(csv):
	return((pd.DataFrame({"km": csv.km / csv.km.max(), "price": csv.price / csv.price.max()})), csv.price.max(), csv.km.max())

def training(args, max_iter, learning_rate):
	try :
		data = pd.read_csv(args.file, delimiter=',')
		for car in data.itertuples():
			if (isNaN(car.km) or isNaN(car.price)):
				return(0, 0, "Invalid file")
	except FileNotFoundError as error :
		return(0, 0, "Error system : {}".format(error))
	cars_nb = len(data)
	if len(data.columns) != 2:
		return (0, 0, "invalid file")
	if (cars_nb == 0):
		return (0,0, "No car")
	if (data.km.min() < 0):
		return (0,0, "km value must be positive")
	if (data.price.min() < 0):
		return (0,0, "price value must be positive")
	if (args.square):
		return least_square(data)
	data, max_price, max_km = normalize_data(data)
	t0 = 0
	t1 = 0
	cost_history = []
	for i in range(max_iter):
		tmpt0, tmpt1 = gradient(data, t0, t1)
		t0 = t0 - (learning_rate * tmpt0)
		t1 = t1 - (learning_rate * tmpt1)
		cost_history.append(cost(t0, t1, data))
	if args.visualise:
		plot_graph_cost(max_iter, cost_history)
	return(t0*max_price, (t1 * max_price) / max_km, "")
