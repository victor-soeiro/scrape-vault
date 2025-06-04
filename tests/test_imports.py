import pathlib
import py_compile
import pytest

BASE = pathlib.Path(__file__).resolve().parents[1]
FILES = [
    BASE / '01 - anime-planet' / 'main.py',
    BASE / '02 - tapas' / 'main.py',
    BASE / '03 - toomics' / 'main.py',
    BASE / '04 - jmlr' / 'main.py',
    BASE / '05 - webtoons' / 'main.py',
    BASE / '06 - afk-arena' / 'main.py',
    BASE / '07 - arknights' / 'main.py',
    BASE / '07 - arknights' / 'cleaning-data.py',
    BASE / '08 - justwatch' / 'main.py',
    BASE / '09 - funko-pop' / 'Untitled.py',
    BASE / '10 - a24 [uncompleted]' / 'main.py',
    BASE / 'steam' / 'main.py'
]

@pytest.mark.parametrize('path', FILES)
def test_compile(path):
    py_compile.compile(str(path), doraise=True)
