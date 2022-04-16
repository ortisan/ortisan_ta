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

Environment

  ```sh
  # Create environment
  conda create -n ortisan-ta python=3.8.0
  conda activate ortisan-ta
  ```

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

Dev instalation

  ```sh
  # Install
  poetry install
  ```

### Notebooks

Check [notebooks](https://github.com/ortisan/ortisan_ta/tree/master/notebooks) with examples.

  ```sh
  # Install
  jupyter notebook notebooks
  ```
