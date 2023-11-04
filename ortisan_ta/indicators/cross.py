import pandas as pd


def crossover_by_value(series: pd.Series[float], value: float) -> pd.Series[bool]:
    return (series.shift(1) < value) & (series > value)


def crossbelow_by_value(series: pd.Series[float], value: float) -> pd.Series[bool]:
    return (series.shift(1) > value) & (series < value)


def cross_by_value(series: pd.Series[float], value: float) -> pd.Series[bool]:
    return crossover_by_value(series, value) | crossbelow_by_value(series, value)


def crossover(series1: pd.Series[float], series2: pd.Series[float]) -> pd.Series[bool]:
    return (series1.shift(1) < series2.shift(1)) & (series1 > series2)


def cross(series1: pd.Series[float], series2: pd.Series[float]):
    return crossover(series1, series2) | crossover(series2, series1)
