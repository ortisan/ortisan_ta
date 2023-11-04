import numpy as np
import pandas as pd

import ortisan_ta.indicators as indicators


def test_arg_max():
    closes = pd.Series([1, 2, 3, 2, 1])
    assert 2 == indicators.argmax_rolling(closes)


def test_arg_min():
    closes = pd.Series([0, 1, 2, 3, 4])
    assert 0 == indicators.argmin_rolling(closes)


def test_sma():
    closes = pd.Series([1, 2, 1, 2])
    sma2 = indicators.sma(closes, 2)
    assert True == np.isnan(sma2[0])
    assert 1.5 == sma2[1]
    assert 1.5 == sma2[2]
    assert 1.5 == sma2[3]


def test_ema():
    closes = pd.Series([1, 1, 1, 1])
    ema2 = indicators.ema(closes, 2)
    assert True == np.isnan(ema2[0])
    assert 1 == ema2[1]
    assert 1 == ema2[2]
    assert 1 == ema2[3]


def test_std():
    closes = pd.Series([1, 1, 2, 4])
    std = indicators.std(closes, 2)
    assert True == np.isnan(std[0])
    assert 0 == std[1]
    assert 0.5 == std[2]
    assert 1 == std[3]


# open = pd.Series([2, 2, 2], copy=False)
# close = pd.Series([4, 4, 4], copy=False)
# bodylen = candlestick.body_length(open=open, close=close)
# expeted = pd.Series([2, 2, 2])
# assert_series_equal(expeted, bodylen)
