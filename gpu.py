from datetime import datetime as dt
import matplotlib.pyplot as plt
import matplotlib
import glob
from utils.requester import *
import time
import numpy
import csv
from textwrap import wrap

amazon = "https://www.amazon.com/s?k=rtx+3080"
newegg = "https://www.newegg.com/p/pl?d=rtx+3080"


class Price():
    def __init__(self, price, time_, site="amazon"):
        self.price = price
        self.time_ = time_ or time.time()
        self.site = site

    def __repr__(self):
        return "Price: {}, Time: {}".format(self.price, self.time_)


class csv_data():
    def __init__(self, file_name="gas/gas.csv"):
        self.file_name = file_name

    def write_prices(self, prices):
        with open(self.file_name, "w+") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(["site", "price", "time"])
            for row in prices:
                csv_writer.writerow([row.site, row.price, row.time_])

    def read_prices(self):
        with open(self.file_name, "r") as csv_file:
            prices = []
            csv_reader = csv.reader(csv_file, delimiter=',')
            for i, row in enumerate(csv_reader):
                if i % 2 == 0 and i != 0:
                    prices.append(Price(row[1], row[2], row[0]))
        return prices


class gpu_analyzer():
    def __init__(self):
        self.amazon_data = Requester(amazon)
        self.newegg_data = Requester(newegg)
        self.amazon_prices = []
        self.newegg_prices = []
        try:
            self.amazon_data.connect_and_get_data()
        except:
            print("Could not connect to amazon")
        try:
            self.newegg_data.connect_and_get_data()
        except:
            print("Could not connect to newegg")
        self.prices = []

    def get_gpu_prices(self):
        self.prices = []
        amazon_prices = self.amazon_data.bullshit.find_all(
            'span', {'class': 'a-price-whole'})
        amazon_prices_prices = []
        newegg_prices = self.newegg_data.bullshit.find_all(
            'li', {'class': 'price-current'})
        newegg_prices_prices = []

        for price in newegg_prices:
            if type(Price) != type(price):
                newegg_prices_prices.append(
                    Price(price.find('strong').text, time_=time.time(), site="newegg"))
        for price in amazon_prices:
            amazon_prices_prices.append(
                Price(price.text, time_=time.time(), site="amazon"))

        self.amazon_prices = amazon_prices_prices
        self.newegg_prices = newegg_prices_prices

    def save_gpu_prices(self):
        data = csv_data("gpu/" + str(self.amazon_prices[0].time_) + ".csv")
        data.write_prices(self.amazon_prices + self.newegg_prices)
        print("Saved Prices")

    def read_gpu_prices(self):
        price_lists = [i for i in glob.glob("gpu/*.csv")]
        for price_list in price_lists:
            data = csv_data(price_list)
            data = data.read_prices()
            amazon_to_append = []
            newegg_to_append = []
            for i in data:
                if i.site == "amazon":
                    amazon_to_append.append(i)
                else:
                    newegg_to_append.append(i)
            self.amazon_prices.append(amazon_to_append)
            self.newegg_prices.append(newegg_to_append)

    def clean_data(self):
        new_amazon_prices = []  
        new_newegg_prices = []
        for i in self.amazon_prices:
            if type(i) == type(Price(1, 1)):
                i.price = i.price.replace("$", "")
                i.price = i.price.replace(",", "")
                new_amazon_prices.append(i)

        for i in self.newegg_prices:
            if type(i) == type(Price(1, 1)):
                i.price = i.price.replace("$", "")
                i.price = i.price.replace(",", "")
                new_newegg_prices.append(i)
        self.amazon_prices = new_amazon_prices
        self.newegg_prices = new_newegg_prices

    def display_average_gpu_prices_graph(self):
        self.read_gpu_prices()
        self.clean_data()
        plt.plot([record.time_ for record in self.amazon_prices], [
                 record.price for record in self.amazon_prices], "ro", label="Amazon")

        plt.plot([record.time_ for record in self.newegg_prices], [
                 record.price for record in self.newegg_prices], "ro", label="Newegg")

    def display_plot(self):
        plt.legend(loc='upper left')
        plt.show()


gpu = gpu_analyzer()
gpu.get_gpu_prices()
gpu.read_gpu_prices()
gpu.clean_data()
gpu.display_average_gpu_prices_graph()
gpu.display_plot()
