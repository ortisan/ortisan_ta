import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

def show_distribution(values: pd.Series, bins=50, title="Boxplot of a Normal Distribution", figsize=(16, 9)):
    fig, axes = plt.subplots(2, 1, figsize=figsize, sharex=True)
    axes[0].boxplot(values, vert=False)
    axes[0].set_title(title);
    axes[1].hist(values, bins=50)

def show_qqplot(values: pd.Series, figsize=(10, 10)):
    plt.figure(figsize=figsize)
    plt.axis('equal')
    stats.probplot(values, dist='norm', plot=plt);    