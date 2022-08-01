# Library for Technical Analysis

### Features

- Technical indicators
  - EMA
  - SMA
  - Bollinger Bands
  - Roc
  - Trends
  - OBV
  - AROON
  - CCI
  - RSI
- Candlestick
- Statistics

### Dev Environment


Tests and coverage

  ```sh
  # Run tests
  poetry run pytest
  # Run coverage
  poetry run coverage run -m pytest && poetry run coverage report -m
  ```

Tox

  ```sh
  # Run tox multiple python versions
  tox
  ```

Dev instalati'http://localhost:8000/prices?symbol=WINQ22&timeframe=TIMEFRAME_M1&initial_date=2022-07-28%2000%3A00%3A00.001&final_date=2022-07-30%2023%3A59%3A59.999on

  ```sh
  # Install
  poetry install
  ```

### Notebooks

Check [notebooks](https://github.com/ortisan/ortisan_ta/tree/master/notebooks) with examples.

  ```sh
  # Install
  poetry run jupyter notebook notebooks
  ```
