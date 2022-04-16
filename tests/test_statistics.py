import numpy as np
import pandas as pd
from pandas.testing import assert_index_equal

from ortisan_ta.statistics import is_normal, is_normal_ks


def test_is_normal():
    mu, sigma = 0, 0.05  # mean and standard deviation
    s = pd.Series(np.random.normal(mu, sigma, size=1000))
    result = is_normal(s)
    assert result

    mu, sigma = 0, 0.05  # mean and standard deviation
    s = pd.Series(np.random.uniform(size=1000))
    result = is_normal(s)
    assert not result


def test_is_normal_ks():
    mu, sigma = 0, 0.05  # mean and standard deviation
    s = pd.Series(np.random.normal(mu, sigma, size=1000))
    result = is_normal_ks(s)
    assert result

    mu, sigma = 0, 0.05  # mean and standard deviation
    s = pd.Series(np.random.uniform(size=1000))
    result = is_normal_ks(s)
    assert not result
