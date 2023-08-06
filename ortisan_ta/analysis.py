import numpy as np
import pandas as pd
import talib
from scipy.stats import linregress


def argmax_rolling(arr: np.ndarray):
    idx_max = np.argwhere(arr == np.amax(arr))
    return idx_max[-1][0]


def argmin_rolling(arr: np.ndarray):
    idx_min = np.argwhere(arr == np.amin(arr))
    return idx_min[-1][0]


def diff_first_last_rolling(arr: np.ndarray):
    return arr[-1] - arr[0]


def pct_first_last_rolling(arr: np.ndarray):
    return arr[-1] / arr[0]


def rolling_sum_abs_diffs(arr: np.ndarray):
    return arr.diff().abs().sum()


def mean_rolling(arr: np.ndarray):
    return np.mean(arr)


def min_rolling(arr: np.ndarray):
    return np.min(arr)


def max_rolling(arr: np.ndarray):
    return np.max(arr)


def std_rolling(arr: np.ndarray):
    return np.std(arr)


def slope_rolling(arr: np.ndarray):
    ordinal_index = np.arange(0, arr.shape[0])
    return linregress(x=ordinal_index, y=arr.values).slope


def z_score_rolling(mean):
    return lambda arr: (np.mean(arr) - mean) / np.std(arr)


def rolling_mean_high_over_mean_low(arr):
    mean_low = np.mean(arr[arr < 0]) - 0.0001
    mean_high = np.mean(arr[arr > 0]) + 0.0001
    mean_low = mean_low * -1
    return mean_high / mean_low


def sma(serie: pd.Series, period: int = 10):
    return serie.rolling(period, min_periods=period).mean()


def std(serie: pd.Series, period: int = 10):
    return serie.rolling(period).apply(std_rolling, raw=True)


def ema(serie: pd.Series, period: int = 10):
    # https://stackoverflow.com/questions/37924377/does-pandas-calculate-ewm-wrong
    sma_val = sma(serie, period)
    # usei esse mecanismo pois a solução do link nao prevê ema com valores depois nans depois do período.
    # Ou seja ema do ema, ele calculava incorretamente.
    idx_start = sma_val.isna().sum() + 1 - period
    idx_end = idx_start + period
    sma_val = sma_val[idx_start:idx_end]
    rest = serie[idx_end:]
    return pd.concat([sma_val, rest]).ewm(span=period, adjust=False).mean()


def bollinger_bands(serie: pd.Series, period=10, std_band=2):
    sma_val = sma(serie, period)
    std_val = std(serie, period)

    value_down = sma_val - std_band * std_val
    value_up = sma_val + std_band * std_val
    value_width = value_up - value_down
    return pd.DataFrame({"down": value_down, "up": value_up, "width": value_width})


def log_returns(serie: pd.Series, period=1):
    return np.log(serie / serie.shift(period))


def cumulative_log_returns(serie: pd.Series, period=1):
    lr = log_returns(serie, period)
    return lr.cumsum()


def hedge_ratio_price_ratio(serie_a: pd.Series, serie_b: pd.Series):
    return (serie_b / serie_a).mean()


def roc(serie: pd.Series, period: int = 20):
    serie_pct = serie.rolling(period).apply(pct_first_last_rolling, raw=True)
    return serie_pct * 100


def efficiency_ratio(close: pd.Series, period: int = 10):
    """
    Measure noise of values. Noise is the fluctuation of prices.
    :param close: Close prices
    :param period: Number of periods to measure
    :return: High value indicates lower noise (abs_change_prices lower than net_change).
    """
    net_change = close.rolling(window=period).apply(diff_first_last_rolling).abs()
    abs_change_prices = close.rolling(window=period).apply(rolling_sum_abs_diffs)
    return net_change / abs_change_prices


def trend_roc(serie: pd.Series, period: int = 20, threshold: float = 0.1):
    roc_val = roc(serie, period)
    df = pd.DataFrame({"roc": roc_val})

    threshold_up = threshold * 100
    threshold_down = threshold * -100

    column_name = "trend_roc"
    df[column_name] = 0
    df.loc[pd.isna(df.roc), column_name] = np.NaN
    df.loc[df.roc >= threshold_up, column_name] = 1
    df.loc[df.roc <= threshold_down, column_name] = -1

    return df


def macd(close: pd.Series, period1=12, period2=26, signal_line_period=9):
    if period1 >= period2:
        raise Exception("Period1 must be less than period2")
    ema_p1 = ema(close, period1)
    ema_p2 = ema(close, period2)
    macd = ema_p1 - ema_p2

    macd_signal = ema(macd, signal_line_period)
    macd_histogram = macd - macd_signal

    buy_alert = (macd_signal.shift(1) < macd) & (macd_signal.shift(1) > macd)
    sell_alert = (macd_signal.shift(1) < macd) & (macd_signal.shift(1) > macd)

    return pd.DataFrame(
        {
            "macd": macd,
            "signal": macd_signal,
            "histogram": macd_histogram,
            "buy_alert": buy_alert,
            "sell_alert": sell_alert,
        }
    )


def obv(close: pd.Series, volume: pd.Series):
    diff = close.diff()
    gt0 = diff.gt(0) * 1
    lt0 = diff.lt(0) * 1

    multiplier = gt0 - lt0
    temp = volume * multiplier
    obv = temp.shift(1) + temp

    return obv


def aroon(high: pd.Series, low: pd.Series, period: int = 25):
    idx_of_max = high.rolling(period, min_periods=period).apply(
        argmax_rolling, raw=True
    )
    idx_of_min = low.rolling(period, min_periods=period).apply(argmin_rolling, raw=True)
    # Interpretação:
    #     Se o índice aroon_up cair abaixo de 50 (máxima está abaixo da mediana), a tendência perdeu força. Isso vale o mesmo para o aroon_down
    #     Se o índice aroon_up estiver acima de 70 (máxima está acima do quartil 3), a tendência está forte. Isso vale o mesmo para o aroon_down

    # % dias em que ocorreu a última alta, se o último período é hoje, o cálculo fica = (25 - 0)/25 * 100 = 100
    aroon_up = ((period - (period - (idx_of_max + 1))) / period) * 100
    # % dias em que ocorreu a última baixa, se o último período é hoje, o cálculo fica = (25 - 0)/25 * 100 = 100
    aroon_down = ((period - (period - (idx_of_min + 1))) / period) * 100

    # Interpretação:
    #     Índice sofrerá variação de -100 a 100, caso o índice for > 0, sinaliza tendência de alta. Se o índice for < 0, tendência de baixa.
    idx_aroon = aroon_up - aroon_down
    return pd.DataFrame({"up": aroon_up, "down": aroon_down, "idx": idx_aroon})


def keltner_bands(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    period: int = 10,
    deviation: float = 2.5,
):
    atr = talib.ATR(high, low, close, timeperiod=period)
    ema = talib.EMA(close, timeperiod=period)
    upperband = ema + deviation * atr
    lowerband = ema - deviation * atr
    middleband = ema
    return (upperband, middleband, lowerband)


def cci(
    high: pd.Series, low: pd.Series, close: pd.Series, period: int = 10, constant=0.015
):
    typical_price = (high + low + close) / 3
    std_typical_price = typical_price.std()
    sma_typical_price = sma(typical_price, period)
    cci = (typical_price - sma_typical_price) / (std_typical_price * constant)
    return cci


def rsi(close: pd.Series, period: int = 10):
    diff = close.diff(1)
    up_direction = diff.where(diff > 0, 0.0)
    down_direction = -diff.where(diff < 0, 0.0)
    ema_up = ema(up_direction, period=period)
    ema_dn = ema(down_direction, period=period)
    relative_strength = ema_up / ema_dn
    rsi = pd.Series(
        np.where(ema_dn == 0, 100, 100 - (100 / (1 + relative_strength))),
        index=close.index,
    )
    return rsi


def get_slope(serie: pd.Series, period: int = 10):
    return serie.rolling(period, min_periods=period).apply(slope_rolling)


def _is_support(low: pd.Series, i: int):
    return (
        low[i] < low[i - 1]
        and low[i] < low[i + 1]
        and low[i + 1] < low[i + 2]
        and low[i - 1] < low[i - 2]
    )


def _is_resistance(high: pd.Series, i: int):
    return (
        high[i] > high[i - 1]
        and high[i] > high[i + 1]
        and high[i + 1] > high[i + 2]
        and high[i - 1] > high[i - 2]
    )


def get_supports_and_resistances(olhc_df: pd.DataFrame):
    supports, resistances = ([], [])
    low = olhc_df.Low
    high = olhc_df.High
    for i in range(2, olhc_df.shape[0] - 2):
        if _is_support(low, i):
            supports.append((i, low[i]))
        elif _is_resistance(high, i):
            resistances.append((i, high[i]))

    return (supports, resistances)


def crossover_by_value(series: pd.Series, value: float):
    return (series.shift(1) < value) & (series > value)


def crossbelow_by_value(series: pd.Series, value: float):
    return (series.shift(1) > value) & (series < value)


def cross_by_value(series: pd.Series, value: float):
    return crossover_by_value(series, value) | crossbelow_by_value(series, value)


def crossover(series1: pd.Series, series2: pd.Series):
    return (series1.shift(1) < series2.shift(1)) & (series1 > series2)


def cross(series1: pd.Series, series2: pd.Series):
    return crossover(series1, series2) | (series2, series1)
