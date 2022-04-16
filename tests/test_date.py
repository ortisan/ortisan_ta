from datetime import datetime

from pandas import date_range
from pandas.testing import assert_index_equal

from ortisan_ta.util import date


def test_get_dates():
    start = datetime.strptime("15/04/2022 00:01", "%d/%m/%Y %H:%M")
    stop = datetime.strptime("18/04/2022 00:01", "%d/%m/%Y %H:%M")
    dates = date.get_dates(start=start, stop=stop, remove_weekend=False)
    expected = date_range(start, periods=4, freq="d")
    assert_index_equal(expected, dates)


def test_get_dates_weekend_removed():
    start = datetime.strptime("15/04/2022 00:01", "%d/%m/%Y %H:%M")
    stop = datetime.strptime("18/04/2022 00:01", "%d/%m/%Y %H:%M")
    dates = date.get_dates(start=start, stop=stop, remove_weekend=True)
    expected = date_range(start, periods=4, freq="d")
    assert expected[0] == dates[0]
    assert expected[-1] == dates[1]
