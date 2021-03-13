# coding=utf-8
__author__ = 'Marcelo Ortiz'

import numpy as np
import pandas as pd
import scipy.stats as stats

def is_normal(sample: pd.Series, test=stats.shapiro, p_level=0.05):    
    t_stat, p_value = test(sample)
    return p_value > p_level

def is_normal_ks(sample: pd.Series, p_level=0.05):
    normal_args = (np.mean(sample), np.std(sample))
    t_stat, p_value = stats.kstest(sample, 'norm', normal_args)
    return p_value > p_level