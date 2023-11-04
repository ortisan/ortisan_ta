import numpy as np
from scipy import stats


def argmax_rolling(ndarray: np.ndarray[float]) -> int:
    idx_max = np.argwhere(ndarray == np.amax(ndarray))
    return idx_max[-1][0]


def argmin_rolling(ndarray: np.ndarray[float]) -> int:
    idx_min = np.argwhere(ndarray == np.amin(ndarray))
    return idx_min[-1][0]


def diff_first_last_rolling(ndarray: np.ndarray[float]) -> float:
    return ndarray[-1] - ndarray[0]


def pct_first_last_rolling(ndarray: np.ndarray[float]) -> float:
    return ndarray[-1] / ndarray[0]


def rolling_sum_abs_diffs(ndarray: np.ndarray[float]) -> float:
    return ndarray.diff().abs().sum()


def mean_rolling(ndarray: np.ndarray[float]) -> float:
    return np.mean(ndarray)


def min_rolling(ndarray: np.ndarray[float]) -> float:
    return np.min(ndarray)


def max_rolling(ndarray: np.ndarray[float]) -> float:
    return np.max(ndarray)


def std_rolling(ndarray: np.ndarray[float]) -> float:
    return np.std(ndarray)


def slope_rolling(ndarray: np.ndarray[float]) -> float:
    ordinal_index = np.arange(0, ndarray.shape[0])
    return stats.linregress(x=ordinal_index, y=ndarray.values).slope
