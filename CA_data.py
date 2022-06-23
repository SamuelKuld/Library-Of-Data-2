import bs4 as bs
from utils.requester import *

attached_URL = "https://www.gasbuddy.com"
initial_URL = "https://www.gasbuddy.com/gasprices/california"

init_data = Requester(initial_URL).connect_and_get_data()

counties = [attached_URL + i["href"] for i in
            bs.BeautifulSoup(init_data, features="html.parser").
            findAll("div", {"class": "AreaCountyList-module__grid___6Le8s"})[1].
            findAll("a", {"class": "DataGrid-module__link___1Pa9Z"})]
print(counties)
cities = []
for county in counties:
    county_data = Requester(county).connect_and_get_data()
    for city in bs.BeautifulSoup(
            county_data,
            features="html.parser").find("div", {"class": "DataGrid-module__container___3Jtbu"}).findAll("a"):
        cities.append(attached_URL + city["href"])

with open("cities.py", "w+") as f:
    f.write("cities = " + str(cities))
    
