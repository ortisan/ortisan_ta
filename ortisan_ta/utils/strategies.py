import pandas as pd
from analysis import bollinger_bands

def bollinger_bands_strategy(close_prices: pd.Series, current_close_price: float, period=10, std_band: float=2.0):
    """
    If close price is bellow lower band, buys (1), if close price is above upper band sell (-1), else do noting (0)
    :param close_prices: Historical close prices
    :param current_close_price: Current close price
    :param period: Period to use on averages and std
    :param std_band: Number of deviation to upper or lower bands
    :return: 1(buy signal), -1(sell signal) or 0(do nothing)
    """
    bands_df = bollinger_bands(close_prices, period=period, std_band=std_band)
    last_bb = bands_df[-1]    
    return 1 if current_close_price < last_bb['down'] elif current_close_price > last_bb['up'] else 0


    



