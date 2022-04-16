from abc import ABC, abstractmethod

from pandas import DataFrame


class IStrategy(ABC):
    """
    Interface for strategies
    Based on [Freqtrade Strategy Interface](https://github.com/freqtrade/freqtrade/blob/develop/freqtrade/strategy/interface.py) and [Backtesting.py Strategy Interface](https://github.com/kernc/backtesting.py/blob/master/backtesting/backtesting.py)
    Defines the mandatory structure must follow any custom strategies
    Attributes you can use:
        minimal_roi -> Dict: Minimal ROI designed for the strategy
        stoploss -> float: optimal stoploss designed for the strategy
        timeframe -> str: value of the timeframe to use with the strategy
    """

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the entry signal for the given dataframe
        :param dataframe: DataFrame
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with entry columns populated
        """
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the entry signal for the given dataframe
        :param dataframe: DataFrame
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with entry columns populated
        """
        return dataframe

    def get_strategy_name(self) -> str:
        """
        Returns strategy class name
        """
        return self.__class__.__name__

    def analyze_ticker(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Parses the given candle (OHLCV) data and returns a populated DataFrame
        add several TA indicators and entry order signal to it
        :param dataframe: Dataframe containing data from exchange
        :param metadata: Metadata dictionary with additional data (e.g. 'pair')
        :return: DataFrame of candle (OHLCV) data with indicator data and signals added
        """
        dataframe = self.advise_indicators(dataframe, metadata)
        dataframe = self.advise_entry(dataframe, metadata)
        dataframe = self.advise_exit(dataframe, metadata)
        return dataframe

    def advise_entry(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the entry order signal for the given dataframe
        This method should not be overridden.
        :param dataframe: DataFrame
        :param metadata: Additional information dictionary, with details like the
            currently traded pair
        :return: DataFrame with buy column
        """

        df = self.populate_entry_trend(dataframe, metadata)
        if "enter_long" not in df.columns:
            df = df.rename(
                {"buy": "enter_long", "buy_tag": "enter_tag"}, axis="columns"
            )

        return df

    def advise_exit(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the exit order signal for the given dataframe
        This method should not be overridden.
        :param dataframe: DataFrame
        :param metadata: Additional information dictionary, with details like the
            currently traded pair
        :return: DataFrame with exit column
        """
        df = self.populate_exit_trend(dataframe, metadata)
        if "exit_long" not in df.columns:
            df = df.rename({"sell": "exit_long"}, axis="columns")
        return df
