from utils.requester import *
from bs4 import BeautifulSoup as bullshit

url = "https://www.google.com/"


def get_gas_price():
    request = Requester(url)
    request.connect_and_get_data()

    if request.status == 200:
        request.get_internal_text()


