from datetime import datetime

import pandas as pd
from pandas.testing import assert_index_equal

from ortisan_ta.util import date


def test_get_dates():
    initial_date = datetime.strptime("15/04/2022 00:01", "%d/%m/%Y %H:%M")
    final_date = datetime.strptime("18/04/2022 00:01", "%d/%m/%Y %H:%M")
    dates = date.get_dates(
        initial_date=initial_date, final_date=final_date, remove_weekend=False
    )
    expected = pd.date_range(initial_date, periods=4, freq="d")
    assert_index_equal(expected, dates)


def test_get_dates_weekend_removed():
    initial_date = datetime.strptime("15/04/2022 00:01", "%d/%m/%Y %H:%M")
    final_date = datetime.strptime("18/04/2022 00:01", "%d/%m/%Y %H:%M")
    dates = date.get_dates(
        initial_date=initial_date, final_date=final_date, remove_weekend=True
    )
    expected = pd.date_range(initial_date, periods=4, freq="d")
    assert expected[0] == dates[0]
    assert expected[-1] == dates[1]
