# On hold since i can't find a live dataset...
from datetime import datetime as dt
import matplotlib.pyplot as plt
import matplotlib
import glob
from utils.requester import *
import time
import numpy
import csv
from textwrap import wrap

url = "https://www.worldometers.info/world-population/us-population/"


class Live():
    def __init__(self, lives, time_):
        self.lives = lives
        self.time_ = time_ or time.time()

    def __repr__(self):
        return "Price: {}, Time: {}".format(self.lives, self.time_)


class csv_data():
    def __init__(self, file_name="lifes/life.csv"):
        self.file_name = file_name

    def write_prices(self, lives):
        with open(self.file_name, "w+") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(["lives", "time"])
            for row in lives:
                csv_writer.writerow([row.lives, row.time_])

    def read_prices(self):
        with open(self.file_name, "r") as csv_file:
            lives = []
            csv_reader = csv.reader(csv_file, delimiter=',')
            for i, row in enumerate(csv_reader):
                if i % 2 == 0 and i != 0:
                    lives.append(Live(row[0], row[1]))
        return lives


class livelihood():
    def __init__(self):
        self.data = Requester(url)
        try:
            self.data.connect_and_get_data()
        except:
            print("Could not connect to worldometers")
        self.lives = []

    def get_lives(self):
        self.lives = []
        self.data = Requester(url)
        self.data.connect_and_get_data()
        self.data = self.data.bullshit.find(
            "span", {"class": "maincounter-number"})
        number = ""
        for child in self.data.children:
            if child.class_ != "rts-nr-sign" or child.class_ != "rts-nr-thsep":
                number += child.text

        self.lives.append(Live(number, time.time()))

        print(self.lives)


lives = livelihood()
lives.get_lives()
