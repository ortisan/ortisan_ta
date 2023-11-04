import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
import scipy.stats as stats
from mplfinance import candlestick_ohlc
from statsmodels.graphics.tsaplots import plot_acf


def basic_olhc_plot(olhc_df):
    fig, ax = plt.subplots()

    candlestick_ohlc(
        ax, olhc_df.values, width=0.6, colorup="green", colordown="red", alpha=0.8
    )

    date_format = mpl_dates.DateFormatter("%d %b %Y")
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()

    fig.tight_layout()

    for level in levels:
        plt.hlines(
            level[1], xmin=df["Date"][level[0]], xmax=max(df["Date"]), colors="blue"
        )

    fig.show()


def show_distribution(
    values,
    bins=50,
    title="Boxplot of a Normal Distribution",
    figsize=(16, 9),
):
    _, axes = plt.subplots(2, 1, figsize=figsize, sharex=True)
    axes[0].boxplot(values, vert=False)
    axes[0].set_title(title)
    axes[1].hist(values, bins=bins)


def show_qqplot(values, figsize=(10, 10)):
    plt.figure(figsize=figsize)
    plt.axis("equal")
    stats.probplot(values, dist="norm", plot=plt)


def show_autocorrelation(values, lags=10, title="Autocorrelation"):
    plot_acf(values, lags=lags, title=title)
