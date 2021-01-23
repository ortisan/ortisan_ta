# coding=utf-8
__author__ = 'Marcelo Ortiz'

import pandas as pd


def get_dates(initial_date, final_date, remove_weekend: bool = True):
    dates = pd.date_range(initial_date, final_date)
    if remove_weekend:
        dates = dates[dates.weekday < 5]
    return dates
