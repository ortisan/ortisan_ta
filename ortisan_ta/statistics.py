import numpy as np
import pandas as pd
import scipy.stats as stats


def is_normal(sample: pd.Series, test=stats.shapiro, p_level=0.05):
    """
    Utilizes some statistical tests (Shapiro-Wilk or D'Agostino-Pearson) to check if values follow normal distribution.
    :param sample: The sample values
    :param test: The test
    :param p_level: p_level to test
    :return: True if normal (test > p_level), False if not normal (test <= p_level)
    """
    _, p_value = test(sample)
    return p_value > p_level


def is_normal_ks(sample: pd.Series, p_level=0.05):
    """
    Verify through Kolmogorov-Smirnov test if values follow normal distribution.
    :param sample: The sample values
    :param test: The test
    :param p_level: p_level to test
    :return: True if normal (p-value > p_level), False if not normal (p-value <= p_level)
    """
    normal_args = (np.mean(sample), np.std(sample))
    _, p_value = stats.kstest(sample, "norm", normal_args)
    return p_value > p_level
