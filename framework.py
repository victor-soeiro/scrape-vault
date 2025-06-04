import requests
from bs4 import BeautifulSoup

class Scraper:
    """Simple base scraper providing helper methods."""
    def __init__(self, session=None):
        self.session = session or requests.Session()

    def fetch(self, url, **kwargs):
        resp = self.session.get(url, **kwargs)
        resp.raise_for_status()
        return resp

    def get_soup(self, url, **kwargs):
        return BeautifulSoup(self.fetch(url, **kwargs).text, 'html.parser')


def get(url, **kwargs):
    return Scraper().fetch(url, **kwargs)


def post(url, data=None, json=None, **kwargs):
    s = Scraper()
    resp = s.session.post(url, data=data, json=json, **kwargs)
    resp.raise_for_status()
    return resp


def get_soup(url, **kwargs):
    return Scraper().get_soup(url, **kwargs)
