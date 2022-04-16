from datetime import datetime, timezone

from pandas import DataFrame, DatetimeIndex, date_range


def get_dates(
    start: datetime, stop: datetime, remove_weekend: bool = True
) -> DatetimeIndex:
    """
    Get dates between start date and stop date
    :param start: start date
    :param datetime_range: timerange (use start and end date if available)
    :param stop: stop date
    :param remove_weekend: flag to remove weekends
    :return: range of dates
    """
    dates = date_range(start, stop)
    if remove_weekend:
        dates = dates[dates.weekday < 5]
    return dates


def trim_dataframe(
    df: DataFrame, datetime_range: DatetimeIndex, df_date_col: str = "date"
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
