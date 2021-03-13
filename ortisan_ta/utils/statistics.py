import pandas as pd
import scipy.stats as stats

def is_normal(sample: pd.Series, test=stats.shapiro, p_level=0.05):
    t_stat, p_value = test(sample, **kwargs)
    return p_value > p_level