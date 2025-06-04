import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from framework import get_soup, get, post


def test_get_soup():
    soup = get_soup('https://httpbin.org/html')
    assert soup.find('h1') is not None


def test_get():
    resp = get('https://httpbin.org/get')
    assert resp.status_code == 200


def test_post():
    resp = post('https://httpbin.org/post', json={'a': 1})
    assert resp.status_code == 200
