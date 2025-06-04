# Repository Overview

This repository contains various web scraping projects organized by numbered folders. Each project typically includes a `main.py` script (exported from Jupyter notebooks) and accompanying data files.

Project directories:
- `01 - anime-planet`
- `02 - tapas`
- `03 - toomics`
- `04 - jmlr`
- `05 - webtoons`
- `06 - afk-arena`
- `07 - arknights`
- `08 - justwatch`
- `09 - funko-pop`
- `10 - a24 [uncompleted]`
- `steam`

The repository also provides a small test suite under `tests/` and a simple scraping framework which now lives in the `framework/` package.

## Change Log
- Created `framework` package from existing `framework.py` with type hints and docstrings.
- Fixed lint errors using the Rust-based linter **ruff**.
- Updated `.gitignore` to exclude caches.
- Adjusted Python scripts and tests to satisfy linter and unit tests.

## TODO
- [ ] Improve separation of concerns across project scripts (many are exported notebooks).
- [ ] Expand test coverage for individual projects.
- [ ] Document each project folder in more detail.

