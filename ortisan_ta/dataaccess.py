# coding=utf-8
__author__ = 'Marcelo Ortiz'

from datetime import datetime

import MetaTrader5 as mt5
import pandas as pd


class DataItem(object):
    DATE = 'Date'
    OPEN = 'Open'
    CLOSE = 'Close'
    HIGH = 'High'
    LOW = 'Low'
    VOLUME = 'Volume'
    ADJUSTED_CLOSE = 'Adj Close'
    SPREAD = 'Spread'

    @staticmethod
    def get_list():
        return [DataItem.OPEN, DataItem.CLOSE, DataItem.HIGH, DataItem.LOW, DataItem.ADJUSTED_CLOSE, DataItem.VOLUME]


class MetaTraderDataAccess(object):

    def __init__(self):
        if not mt5.initialize():
            print("initialize() failed, error code =", mt5.last_error())
            raise Exception("Error to connect to Metatrader.", mt5.last_error())

    def get_rates_from_symbol(self, symbol: str, date_from: datetime, date_to: datetime, timeframe=mt5.TIMEFRAME_M5):
        rates = mt5.copy_rates_range(symbol, timeframe, date_from, date_to)
        df = pd.DataFrame(rates)
        if df.empty:
            return df
        df.time = df.time.transform([datetime.fromtimestamp])
        df.drop(['tick_volume'], axis=1, inplace=True)
        df.columns = [DataItem.DATE, DataItem.OPEN, DataItem.HIGH, DataItem.LOW, DataItem.CLOSE, DataItem.SPREAD,
                      DataItem.VOLUME]
        df.set_index(DataItem.DATE, inplace=True)
        return df

    def get_rates_from_symbols(self, symbols: list, date_from: datetime, date_to: datetime, timeframe=mt5.TIMEFRAME_M5):
        dfs = {}
        for symbol in symbols:
            dfs[symbol] = self.get_rates_from_symbol(symbol, date_from, date_to, timeframe)
        return dfs
