import pandas as pd
import talib


def macd(
    pdserie: pd.Series[float],
    fastperiod: int = 12,
    slowperiod: int = 26,
    signalperiod: int = 9,
) -> (pd.Series[float], pd.Series[float], pd.Series[float]):
    if fastperiod >= slowperiod:
        raise Exception("fast period must be less than slow period")

    macd, macdsignal, macdhist = talib.MACD(
        pdserie, fastperiod, slowperiod, signalperiod
    )

    return (macd, macdsignal, macdhist)


def aroon(
    high: pd.Series[float], low: pd.Series[float], period: int = 25
) -> (pd.Series[float], pd.Series[float]):
    aroondown, aroonup = talib.AROON(high, low, timeperiod=period)
    return (aroondown, aroonup)


def roc(pdserie: pd.Series[float], period: int = 20) -> pd.Series[float]:
    roc = talib.ROC(pdserie, timeperiod=period)
    return roc


def rsi(pdserie: pd.Series[float], period: int = 20) -> pd.Series[float]:
    rsi = talib.RSI(pdserie, timeperiod=period)
    return rsi
