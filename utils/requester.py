import requests
from bs4 import BeautifulSoup as bullshit
from bs4.element import Comment


# ? Can only be used once due to a requests
# ? session object being the method of data retreival
class Requester():
    def __init__(self, url="https://www.google.com", headers={
            "user-agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G920A) AppleWebKit (KHTML, like Gecko) Chrome Mobile Safari (compatible; AdsBot-Google-Mobile; +http://www.google.com/mobile/adsbot.html)",
            "Accept": "text/html, application/xhtml+xml, application/xml; q=0.9, image/webp",
            "Upgrade-Insecure-Requests": "1",
            "Accept-Encoding": "gzip",
            "Referer": "https://www.google.com/"}, timeout=10):

        self.url = url
        self.headers = headers
        self.timeout = timeout
        self.requests_object = requests.Session()

        self.data = None
        self.status = None
        self.string = None
        self.bullshit = None

    def connect_and_get_data(self):
        self.requests_object.headers.update(self.headers)
        data_got = self.requests_object.get(self.url, timeout=self.timeout)
        self.status, self.data, self.string = data_got.status_code, data_got, data_got.text
        self.bullshit = bullshit(self.string, "html.parser")
        return self.string
