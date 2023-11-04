import pandas as pd
from utils import diff_first_last_rolling, rolling_sum_abs_diffs


def efficiency_ratio(close: pd.Series[float], period: int = 10) -> pd.Series[float]:
    """
    Measure noise of values. Noise is the fluctuation of prices.
    :param close: Close prices
    :param period: Number of periods to measure
    :return: High value indicates lower noise (abs_change_prices lower than net_change).
    """
    net_change = close.rolling(window=period).apply(diff_first_last_rolling).abs()
    abs_change_prices = close.rolling(window=period).apply(rolling_sum_abs_diffs)
    return net_change / abs_change_prices
