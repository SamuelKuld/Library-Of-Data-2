from datetime import datetime as dt
from tkinter import N
import matplotlib.pyplot as plt
import matplotlib
import glob
from utils.requester import *
import time
import numpy
import csv
from textwrap import wrap
from cities_valid import cities


request_delay = 1
plots = 0
#states = ["\n".join(wrap(state, 5)) for state in states]
matplotlib.rcParams.update({'font.size': 7})
matplotlib.rcParams["figure.figsize"] = [7.50, 2.50]
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
    def __init__(self, price, time_=None, state="california"):
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
        state_links = cities
        prices = []
        for i, link in enumerate(state_links):
            retry = True
            while retry:
                try:
                    print(f"{i + 1} of {len(cities)} ")
                    self.data = Requester(link)
                    self.data.connect_and_get_data()
                    price = self.data.bullshit.find(
                        "span", {"class": "text__xl___2MXGo text__left___1iOw3 StationDisplayPrice-module__price___3rARL"}).text
                    # When price is available save it
                    if price != "---":
                        # ? This is the price of gas in a state
                        prices.append(
                            Price(price, time_=time.time(),  state=link.split("/")[-1]))
                        print("Price got.")

                    time.sleep(request_delay)
                    retry = False
                except ValueError:
                    # ? This is the price of gas in a state
                    prices.append(
                        Price("$4.50", time_=time.time(),  state=link.split("/")[-1]))
                    print("Could not get price")
                    retry = False
                    continue
                except AttributeError:
                    prices.append(Price(self.data.bullshit.find("$4.50", time_=time.time(
                    ),  state=link.split("/")[-1])))  # ? This is the price of gas in a state
                    print("Could not get price")
                    retry = False
                    continue
                except Exception as e:
                    print("Retrying : " + str(e))
                    retry = True

        self.prices.append(prices)
        print("Got prices")

    def save_gas_prices(self):
        for list_of_prices in self.prices:
            data = csv_data("gas_CA/" + str(list_of_prices[0].time_) + ".csv")
            data.write_prices(list_of_prices)
        self.prices = []

        print("Saved Prices")

    def read_gas_prices(self):
        gas_lists = [i for i in glob.glob("gas_CA/*.csv")]
        self.prices = []
        for list_ in gas_lists:
            data = csv_data(str(list_))
            self.prices.append(data.read_prices())

    def display_gas_prices_bar(self, item=0):
        global plots
        # Sort by price
        prices = [i.price for i in self.prices[item]]
        X_axis = numpy.arange(len(cities))
        now = dt.fromtimestamp(float(self.prices[item][0].time_))
        plt.xticks(X_axis, cities)
        plt.bar(X_axis + (0.2 * item), [float(i.replace('$', '')) for i in prices],
                label=f"Gas Prices - {now.strftime('%Y-%m-%d %H:%M:%S')}", width=.2, )
        plt.xticks()

    def display_gas_prices_graph(self):
        self.read_gas_prices()
        states_and_prices = []
        for j in range(len(cities)):
            states_and_prices.append(
                [i for i in [k[j] for k in self.prices]])
        for i in states_and_prices:
            for j in i:
                if j.price != "---" and j.price != "":
                    plt.scatter([dt.fromtimestamp(round(float(i.time_))) for i in i], [float(i.price.replace('$', ''))
                                                                                       for i in i], label=cities[states_and_prices.index(i)])

    def display_average_gas_prices_graph(self):
        old = 0
        avg_prices = []
        times = []
        for record in self.prices:
            for i in record:
                if i.price != "---" and i.price != '':
                    old += float(i.price.replace('$', ''))
            record_time = dt.fromtimestamp(round(float(record[0].time_)))
            times.append(record_time)
            avg_prices.append(old / len(record))
            old = 0
        axes = plt.axes()
        if len(avg_prices) > 3:
            for i in range(len(avg_prices)):
                if i > 0:
                    if avg_prices[i] > avg_prices[i - 1]:
                        axes.plot([times[i-1], times[i]],
                                  [avg_prices[i-1], avg_prices[i]], color="red")
                    elif avg_prices[i] < avg_prices[i - 1]:
                        axes.plot([times[i-1], times[i]],
                                  [avg_prices[i-1], avg_prices[i]], color="green")
                    else:
                        axes.plot([times[i-1], times[i]],
                                  [avg_prices[i-1], avg_prices[i]], color="white")
        else:
            axes.plot(times, avg_prices, color="red")

    def print_statictics(self, item=0):
        sorted_prices = sorted(self.prices[item], key=lambda x: x.price)
        numeric_prices = []
        for j in sorted_prices:
            if j.price != "---" and j.price != "":
                numeric_prices.append(float(j.price.replace('$', '')))
                print(j.state.split("/")[-1] + ": " + j.price)

        print("State Average : " + str(sum(numeric_prices) / len(numeric_prices)))

    def display_plot(self):
        plt.legend(loc='upper left', bbox_to_anchor=(
            0.5, -0.05), fancybox=True, shadow=True, ncol=5)
        plt.show()


def main():
    try:
        gas = None
        gas = gas_money()
        gas.prices = []
        gas.get_gas_prices()
        gas.save_gas_prices()
    except Exception as e:
        print(f"error : {e}")
        return


def debug():
    gas = gas_money()
    gas.get_gas_prices()
    gas.save_gas_prices()


if __name__ == "__main__":
    while True:
        main()
