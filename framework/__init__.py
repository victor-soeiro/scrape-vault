"""Simple web scraping framework utilities."""


from typing import Any, Dict, Optional

import requests
from bs4 import BeautifulSoup


class Scraper:
    """HTTP client wrapper with convenience methods."""

    def __init__(self, session: Optional[requests.Session] = None) -> None:
        self.session = session or requests.Session()

    def fetch(self, url: str, **kwargs: Any) -> requests.Response:
        """Perform a GET request and return the response."""
        resp = self.session.get(url, **kwargs)
        resp.raise_for_status()
        return resp

    def get_soup(self, url: str, **kwargs: Any) -> BeautifulSoup:
        """Fetch ``url`` and return a BeautifulSoup parser."""
        return BeautifulSoup(self.fetch(url, **kwargs).text, "html.parser")


def get(url: str, **kwargs: Any) -> requests.Response:
    """Convenience wrapper around :meth:`Scraper.fetch`."""
    return Scraper().fetch(url, **kwargs)


def post(
    url: str,
    data: Any = None,
    json: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> requests.Response:
    """Convenience wrapper performing a POST request."""
    s = Scraper()
    resp = s.session.post(url, data=data, json=json, **kwargs)
    resp.raise_for_status()
    return resp


def get_soup(url: str, **kwargs: Any) -> BeautifulSoup:
    """Convenience wrapper around :meth:`Scraper.get_soup`."""
    return Scraper().get_soup(url, **kwargs)

