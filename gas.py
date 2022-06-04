from utils.requester import *
import time
import csv

url = "https://www.google.com/"
request_delay = 1


class csv_data():
    def __init__(self, file_name="gas.csv"):
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
            for row in csv_reader:
                prices.append(Price(row[0], row[1], row[2]))

        return prices


class Price():
    def __init__(self, price, time_=time.time(), state="california"):
        self.price = price
        self.time_ = time_
        self.state = state

    def __repr__(self):
        return "Price: {}, Time: {}".format(self.price, self.time_)


class gas_money():
    def __init__(self):
        self.data = Requester(
            "https://www.gasbuddy.com/")
        self.data.connect_and_get_data()
        self.prices = []

    def get_gas_prices(self):
        states = self.data.bullshit.find_all(
            "div", {"class": "SearchStateCloud-module__stateContainer___2StKz"})
        state_links = []
        prices = []
        for i in states:
            state_links.append("https://www.gasbuddy.com" +
                               i.find("a").get("href"))

        for link in state_links:
            self.data = Requester(link)
            self.data.connect_and_get_data()

            prices.append(Price(self.data.bullshit.find(
                "span", {"class": "text__xl___2MXGo text__left___1iOw3 StationDisplayPrice-module__price___3rARL"}).text, state=link.split("/")[-1]))  # ? This is the price of gas in a state
            print("Price got.")
            time.sleep(request_delay)

        self.prices.append(prices)
        print("Got prices")

    def save_gas_prices(self):
        for list_of_prices in self.prices:
            data = csv_data(str(list_of_prices[0].time_))
            data.write_prices(list_of_prices)

        print("Saving Prices")


gas = gas_money()
gas.get_gas_prices()
gas.save_gas_prices()
