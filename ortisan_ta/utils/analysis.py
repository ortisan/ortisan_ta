# coding=utf-8
__author__ = 'Marcelo Ortiz'

import numpy as np
import pandas as pd


def argmax_rolling(arr: np.ndarray):
    idx_max = np.argwhere(arr == np.amax(arr))
    return idx_max[-1][0]


def argmin_rolling(arr: np.ndarray):
    idx_min = np.argwhere(arr == np.amin(arr))
    return idx_min[-1][0]


def diff_first_last_rolling(arr: np.ndarray):
    return arr[-1] - arr[0]


def pct_first_last_rolling(arr: np.ndarray, absolute_value: bool = False):
    return arr[-1] / arr[0] - 1


def mean_rolling(arr: np.ndarray):
    return np.mean(arr)


def min_rolling(arr: np.ndarray):
    return np.min(arr)


def max_rolling(arr: np.ndarray):
    return np.max(arr)


def std_rolling(arr: np.ndarray):
    return np.std(arr)


def z_score_rolling(mean):
    return lambda arr: (np.mean(arr) - mean) / np.std(arr)


def array_rolling(arr: np.ndarray):
    return arr.tostring()

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
    sma_val = sma_val[idx_start: idx_end]
    rest = serie[idx_end:]
    return pd.concat([sma_val, rest]).ewm(span=period, adjust=False).mean()


def bollinger_bands(serie: pd.Series, period=10, std_band=2):
    """
    Cria colunas representam a banda inferior VL - X * Desvio Padrão e superior VL + X * Desvio Padrão.

    Keyword arguments:
    df - Dataframe
    items - Colunas que serão usadas.
    periods - Períodos a serem considerados nos cálculos.
    std_band - Número de desvio padrão a ser considerado nos cálculos
    """
    sma_val = sma(serie, period)
    std_val = std(serie, period)

    value_down = sma_val - std_band * std_val
    value_up = sma_val + std_band * std_val
    value_width = value_up - value_down
    return pd.DataFrame({'down': value_down, 'up': value_up, 'width': value_width})


def roc(serie: pd.Series, period: int = 20):
    """
    Cria coluna de porcentagem de lucro ou prejuizo.
    :param df: Dataframe
    :param item: Item do dataframe utilizado para os cálculos
    :param period: Período que será utilizado no cálculo
    :return: pandas.Series com os valores de ROC
    """
    serie_pct = serie.rolling(period).apply(pct_first_last_rolling, raw=True)
    return serie_pct * 100


def trend_roc(serie: pd.Series, period: int = 20, threshold: float = 0.1):
    """
    Cria colunas de tendência onde 1 é uma tendência de alta, -1, uma tendência de baixa e 0 não apresentando tendência.
    :param df: Dataframe
    :param col: Coluna no dataframe que será utilizada nos cálculos
    :param period: Lista de períodos
    :param threshold: Limite que indique uma porcentagem Ex: 0.1, indicará > 10% ou -10%
    :return: Novo dataframe com colunas roc e trend_roc
    """
    roc_val = roc(serie, period)
    df = pd.DataFrame({'roc': roc_val})

    threshold_up = threshold * 100
    threshold_down = threshold * -100

    column_name = 'trend_roc'
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

    return pd.DataFrame({"macd": macd, "signal": macd_signal, "histogram": macd_histogram, "buy_alert": buy_alert, "sell_alert": sell_alert})


def obv(close: pd.Series, volume: pd.Series):
    """
    O OBV é um indicador de tendência.
    Se o valor de fechamento atual é maior que o fechamento anterior, OBV = OBV + VOLUME.
    Se o valor de fechamento atual é menor que o fechamento anterior, OBV = OBV - VOLUME.
    Se o valor de fechamento é igual ao fechamento anterior, OBV = OBV
    :param df: Dataframe
    :return: Dataframe contendo o OBV df['OBV']
    """
    diff = close.diff()
    gt0 = diff.gt(0) * 1
    lt0 = diff.lt(0) * 1

    multiplier = gt0 - lt0
    temp = (volume * multiplier)
    obv = temp.shift(1) + temp

    return obv


def aroon(high: pd.Series, low: pd.Series, period: int = 25):
    """
    O sistema Aroon indica se a ação está em tendência e o quão forte ela é.
    Keyword arguments:
    df - Dataframe
    period - Período.
    """
    idx_of_max = high.rolling(period, min_periods=period).apply(
        argmax_rolling, raw=True)
    idx_of_min = low.rolling(period, min_periods=period).apply(
        argmin_rolling, raw=True)
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


def rsi(close, period=10):
    diff = close.diff(1)
    up_direction = diff.where(diff > 0, 0.0)
    down_direction = -diff.where(diff < 0, 0.0)
    emaup = ema(up_direction, period=period)
    emadn = ema(down_direction, period=period)
    relative_strength = emaup / emadn
    rsi = pd.Series(
        np.where(emadn == 0, 100, 100 - (100 / (1 + relative_strength))),
        index=close.index,
    )
    return rsi