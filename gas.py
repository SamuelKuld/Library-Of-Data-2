from datetime import datetime as dt
import matplotlib.pyplot as plt
import matplotlib
import glob
from utils.requester import *
import time
import numpy
import csv
from textwrap import wrap

url = "https://www.google.com/"
request_delay = 1
plots = 0
states = ['alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut', 'delaware', 'florida', 'georgia', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas', 'kentucky', 'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota', 'mississippi', 'missouri', 'montana', 'nebraska',
          'nevada', 'new-hampshire', 'new-jersey', 'new-mexico', 'new-york', 'north-carolina', 'north-dakota', 'ohio', 'oklahoma', 'oregon', 'pennsylvania', 'rhode-island', 'south-carolina', 'south-dakota', 'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'washington', 'washington-dc', 'west-virginia', 'wisconsin', 'wyoming']
#states = ["\n".join(wrap(state, 5)) for state in states]
matplotlib.rcParams.update({'font.size': 7})
matplotlib.rcParams["figure.figsize"] = [7.50, 3.50]
matplotlib.style.use(['dark_background'])


class csv_data():
    def __init__(self, file_name="gas/gas.csv"):
        self.file_name = file_name

    def write_prices(self, prices):
        with open(self.file_name, "w+") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(["state", "price", "time"])
            for row in prices:
                csv_writer.writerow([row.state, row.price, row.time_])

    def read_prices(self):
        with open(self.file_name, "r") as csv_file:
            prices = []
            csv_reader = csv.reader(csv_file, delimiter=',')
            for i, row in enumerate(csv_reader):
                if i % 2 == 0 and i != 0:
                    prices.append(Price(row[1], row[2], row[0]))
        return prices


class Price():
    def __init__(self, price, time_, state="california"):
        self.price = price
        self.time_ = time_ or time.time()
        self.state = state

    def __repr__(self):
        return "Price: {}, Time: {}".format(self.price, self.time_)


class gas_money():
    def __init__(self):
        self.data = Requester(
            "https://www.gasbuddy.com/")
        try:
            self.data.connect_and_get_data()
        except:
            print("Could not connect to gasbuddy")
        self.prices = []

    def get_gas_prices(self):
        self.prices = []
        states = self.data.bullshit.find_all(
            "div", {"class": "SearchStateCloud-module__stateContainer___2StKz"})
        state_links = []
        prices = []
        for i in states:
            state_links.append("https://www.gasbuddy.com" +
                               i.find("a").get("href"))

        for i, link in enumerate(state_links):
            print(f"{i + 1} of 51 ")
            self.data = Requester(link)
            self.data.connect_and_get_data()

            prices.append(Price(self.data.bullshit.find(
                "span", {"class": "text__xl___2MXGo text__left___1iOw3 StationDisplayPrice-module__price___3rARL"}).text, time_=time.time(),  state=link.split("/")[-1]))  # ? This is the price of gas in a state
            print("Price got.")
            time.sleep(request_delay)

        self.prices.append(prices)
        print("Got prices")

    def save_gas_prices(self):
        for list_of_prices in self.prices:
            data = csv_data("gas/" + str(list_of_prices[0].time_) + ".csv")
            data.write_prices(list_of_prices)
        self.prices = []

        print("Saving Prices")

    def read_gas_prices(self):
        gas_lists = [i for i in glob.glob("gas/*.csv")]
        self.prices = []
        for list_ in gas_lists:
            data = csv_data(str(list_))
            self.prices.append(data.read_prices())

    def display_gas_prices_bar(self, item=0):
        global plots
        # Sort by price
        prices = [i.price for i in self.prices[item]]
        X_axis = numpy.arange(len(states))
        now = dt.fromtimestamp(float(self.prices[item][0].time_))
        plt.xticks(X_axis, states)
        plt.bar(X_axis + (0.2 * item), [float(i.replace('$', '')) for i in prices],
                label=f"Gas Prices - {now.strftime('%Y-%m-%d %H:%M:%S')}", width=.2, )
        plt.xticks()

    def display_gas_prices_graph(self):
        self.read_gas_prices()
        states_and_prices = []
        for j in range(len(states)):
            states_and_prices.append(
                [i for i in [k[j] for k in self.prices]])
        for i in states_and_prices:
            plt.plot([dt.fromtimestamp(round(float(i.time_))) for i in i], [float(i.price.replace('$', ''))
                                                                            for i in i], label=states[states_and_prices.index(i)])

    def display_average_gas_prices_graph(self):
        old = 0
        avg_prices = []
        times = []
        for record in self.prices:
            for i in record:
                old += float(i.price.replace('$', ''))
            record_time = dt.fromtimestamp(round(float(record[0].time_)))
            times.append(record_time)
            avg_prices.append(old / 51)
            old = 0
        axes = plt.axes()
        axes.plot(times, avg_prices)
        plt.scatter(times, avg_prices, label="Average Prices", s=0)

    def display_average_CA_gas_prices_graph(self):
        old = 0
        avg_prices = []
        times = []
        for record in self.prices:
            avg_prices.append(float(record[4].price.replace('$', '')))
            record_time = dt.fromtimestamp(round(float(record[0].time_)))
            times.append(record_time)
        axes = plt.axes()
        axes.plot(times, avg_prices)
        plt.scatter(times, avg_prices, label="Average Prices")

    def display_average_OR_gas_prices_graph(self):
        old = 0
        avg_prices = []
        times = []
        for record in self.prices:
            avg_prices.append(
                float(record[states.index("oregon")].price.replace('$', '')))
            record_time = dt.fromtimestamp(round(float(record[0].time_)))
            times.append(record_time)
        axes = plt.axes()
        axes.plot(times, avg_prices)
        plt.scatter(times, avg_prices, label="Average Prices")

    def display_plot(self):
        plt.legend(loc='upper left')
        plt.show()


def main():
    try:
        gas = None
        gas = gas_money()
        gas.prices = []
        gas.get_gas_prices()
        gas.save_gas_prices()
    except:
        print("error")
        return


def debug():
    gas = gas_money()
    gas.get_gas_prices()
    gas.save_gas_prices()


if __name__ == "__main__":
    while True:
        main()
