import pandas as pd
import talib


def bollinger_bands(
    pdserie: pd.Series[float], period: int = 10, std_band: int = 2
) -> (pd.Series[float], pd.Series[float], pd.Series[float]):
    upperband, middleband, lowerband = talib.BBANDS(
        pdserie, timeperiod=period, nbdevup=std_band, nbdevdn=std_band
    )
    return (upperband, middleband, lowerband)


def keltner_bands(
    high: pd.Series[float],
    low: pd.Series[float],
    close: pd.Series[float],
    period: int = 10,
    std_band: float = 2.5,
):
    atr = talib.ATR(high, low, close, timeperiod=period)
    ema = talib.EMA(close, timeperiod=period)
    upperband = ema + std_band * atr
    lowerband = ema - std_band * atr
    middleband = ema
    return (upperband, middleband, lowerband)
