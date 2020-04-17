import matplotlib.pyplot as plt

def estimate_price(km, theta0, theta1):
	return (theta1*km + theta0)

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