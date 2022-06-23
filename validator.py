from signal import valid_signals
from cities_valid import cities
from utils.requester import *
import time


class Price():
    def __init__(self, price, time_, state="california"):
        self.price = price
        self.time_ = time_ or time.time()
        self.state = state

    def __repr__(self):
        return "Price: {}, Time: {}".format(self.price, self.time_)


repeat = 0
valid_cities = []
for v, i in enumerate(cities):
    for j in cities:
        if repeat <= 1:
            valid_cities.append(j)
        if j == i:
            repeat += 1
    if repeat > 1:
        print(i)

with open("cities_valid.py", "w+") as f:
    f.write("cities = " + str(valid_cities))

print(len(cities))
print(len(str(cities)))
