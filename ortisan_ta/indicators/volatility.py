import pandas as pd
import talib


def average_true_range(
    high: pd.Series[float],
    low: pd.Series[float],
    close: pd.Series[float],
    period: int = 14,
) -> pd.Series[float]:
    return talib.ATR(high, low, close, timeperiod=period)


def true_range(
    high: pd.Series[float], low: pd.Series[float], close: pd.Series[float]
) -> pd.Series[float]:
    return talib.TRANGE(high, low, close)
