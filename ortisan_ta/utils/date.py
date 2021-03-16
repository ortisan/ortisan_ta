# coding=utf-8
__author__ = 'Marcelo Ortiz'

import pandas as pd
from datetime import datetime


def get_dates(initial_date: datetime, final_date: datetime, remove_weekend: bool = True):
    dates = pd.date_range(initial_date, final_date)
    if remove_weekend:
        dates = dates[dates.weekday < 5]
    return dates
