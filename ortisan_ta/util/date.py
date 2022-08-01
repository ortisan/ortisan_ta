from datetime import datetime

from pandas import DataFrame, DatetimeIndex, date_range


def get_dates(
    initial_date: datetime, final_date: datetime, remove_weekend: bool = True
) -> DatetimeIndex:
    """
    Get dates between start date and stop date
    :param initial_date: initial date
    :param final_date: final date
    :param remove_weekend: flag to remove weekends
    :return: range of dates
    """
    dates = date_range(start, stop)
    if remove_weekend:
        dates = dates[dates.weekday < 5]
    return dates


def trim_dataframe(
    df: DataFrame, datetime_range: DatetimeIndex, df_date_col: str = "Date"
) -> DataFrame:
    """
    Trim dataframe based on given timerange
    :param df: Dataframe to trim
    :param datetime_range: timerange (use start and end date if available)
    :param df_date_col: Column in the dataframe to use as Date column
    :return: trimmed dataframe
    """
    start = datetime_range[0]
    df = df.loc[df[df_date_col] >= start, :]
    if len(datetime_range) > 1:
        stop = datetime_range[-1]
        df = df.loc[df[df_date_col] <= stop, :]

    return df


def get_outer_dates(dates_series: pd.Series, freq: str = "1min"):
    """
    Get the outer dates that is not in the range. Utilized by plotly to remove from graphs.
    :param dates_series: Series with dates
    :param freq: pandas datetime freq
    :return: list with the outer dates
    """
    all_dates_between_interval = date_range(
        start=dates_series[0], end=dates_series[-1], freq=freq
    )
    observed_dates = [d for d in df.index]
    outer_dates = [d for d in all_dates_between_interval if not d in observed_dates]
    return outer_dates
