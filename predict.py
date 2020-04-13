import csv
import argparse
import pandas as pd

def estimate_price(km):
    theta = pd.read_csv(".save_model.csv", delimiter=',')
    theta0 = theta.Theta0[0]
    theta1 = theta.Theta1[0]
    return (theta1*km + theta0)

if __name__ == "__main__":
    try :
        parser = argparse.ArgumentParser()
        parser.add_argument("kilometers", help="Define parameter 'kilometer' to prediction", type = int)
        args = parser.parse_args()
        estimate_price = estimate_price(args.kilometers)
        print("Price estimate is : {}".format(round(estimate_price, 2)))
    except FileNotFoundError as error :
        print("File not found. Please, run train_model.py")
