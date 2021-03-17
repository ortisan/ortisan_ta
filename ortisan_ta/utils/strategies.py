import pandas as pd
from analysis import bollinger_bands, sma, max_rolling


def bollinger_bands_strategy(close_prices: pd.Series, current_close_price: float, period=10, std_band: float = 2.0):
    """
    If close price is bellow lower band, buys (1), if close price is above upper band sell (-1), else do noting (0)
    :param close_prices: Close prices
    :param current_close_price: Current close price
    :param period: Period to use on averages and std
    :param std_band: Number of deviation to upper or lower bands
    :return: 1(buy signal), -1(sell signal) or 0(do nothing)
    """
    bands_df = bollinger_bands(close_prices, period=period, std_band=std_band)
    last_bb = bands_df[-1]
    return 1 if current_close_price < last_bb['down'] elif current_close_price > last_bb['up'] else 0


def key_reversal_days_down(close_prices: pd.Series, high_prices: pd.Series, low_prices: pd.Series, period=10):
    """
    Strategy that indicates possible days reversion to down.
    :param close_prices: Close prices
    :param high_prices: High prices
    :param low_prices: Low prices
    :param period: Period to use on averages and std
    :return: True, False indicates posible reversions to down
    """
    close_shifted_1 = close_prices.shift(1)
    sma_close_2_n = sma(close_prices.shift(2), period)
    highest_1_n = high_prices.shift(1).rolling(period).apply(max_rolling, raw=True)
    low_shifted_1 = low_prices.shift(1)
    return (close_prices > sma_close_shifted) & (high_prices >= highest_1_n) & (low < low_shifted_1) & (close < close_shifted_1)
