import pandas as pd


def get_supports_and_resistances(olhc_df: pd.DataFrame):
    supports, resistances = ([], [])
    low = olhc_df.Low
    high = olhc_df.High
    for i in range(2, olhc_df.shape[0] - 2):
        if _is_support(low, i):
            supports.append((i, low[i]))
        elif _is_resistance(high, i):
            resistances.append((i, high[i]))

    return (supports, resistances)
