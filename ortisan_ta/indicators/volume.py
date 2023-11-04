import pandas as pd
import talib


def obv(close: pd.Series[float], volume: pd.Series[float]):
    return talib.OBV(close, volume)
