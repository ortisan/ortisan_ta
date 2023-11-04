import pandas as pd
import talib


def avg_price(
    open: pd.Series[float],
    high: pd.Series[float],
    low: pd.Series[float],
    close: pd.Series[float],
) -> pd.Series[float]:
    return talib.AVGPRICE(open, high, low, close)


def tipical_price(
    high: pd.Series[float], low: pd.Series[float], close: pd.Series[float]
) -> pd.Series[float]:
    return talib.TYPPRICE(high, low, close)


def sma(pdserie: pd.Series[float], period: int = 10) -> pd.Series[float]:
    return talib.SMA(pdserie, timeperiod=period)


def ema(pdserie: pd.Series[float], period: int = 10) -> pd.Series[float]:
    return talib.EMA(pdserie, timeperiod=period)


def kama(pdserie: pd.Series[float], period: int = 30) -> pd.Series[float]:
    return talib.KAMA(pdserie, timeperiod=period)
