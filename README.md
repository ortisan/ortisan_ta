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

Commands

  ```sh
  # Install dependencies
  poetry add <dependency name>
  # Activate Env
  poetry shell
  # Organize imports and format code
  poetry run autoflake --expand-star-imports --remove-all-unused-imports --remove-duplicate-keys --remove-unused-variables --recursive --in-place .  && poetry run isort . && poetry run black .
  # Test
  poetry run coverage run -m pytest && poetry run coverage report -m
  ```

Tox

  ```sh
  # Run tox multiple python versions
  tox
  ```

Dev installation

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
