import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
from statsmodels.graphics.tsaplots import plot_acf


def show_distribution(
    values: pd.Series,
    bins=50,
    title="Boxplot of a Normal Distribution",
    figsize=(16, 9),
):
    _, axes = plt.subplots(2, 1, figsize=figsize, sharex=True)
    axes[0].boxplot(values, vert=False)
    axes[0].set_title(title)
    axes[1].hist(values, bins=bins)


def show_qqplot(values: pd.Series, figsize=(10, 10)):
    plt.figure(figsize=figsize)
    plt.axis("equal")
    stats.probplot(values, dist="norm", plot=plt)


def show_autocorrelation(values: pd.Series, lags=10, title="Autocorrelation"):
    plot_acf(values, lags=lags, title=title)
