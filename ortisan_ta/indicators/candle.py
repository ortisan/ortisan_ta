import numpy as np
import pandas as pd
import talib


def name_candlesticks(
    open: pd.Series[float],
    high: pd.Series[float],
    low: pd.Series[float],
    close: pd.Series[float],
):
    dojis = talib.CDLDOJI(open, high, low, close)
    doji_stars = talib.CDLDOJISTAR(open, high, low, close)
    dragonfly_dojis = talib.CDLDRAGONFLYDOJI(open, high, low, close)
    marubozus = talib.CDLMARUBOZU(open, high, low, close)
    hammers = talib.CDLHAMMER(open, high, low, close)
    inverted_hammers = talib.CDLINVERTEDHAMMER(open, high, low, close)
    gravestone_dojis = talib.CDLGRAVESTONEDOJI(open, high, low, close)
    longlegged_dojis = talib.CDLLONGLEGGEDDOJI(open, high, low, close)
    longlines = talib.CDLLONGLINE(open, high, low, close)
    spinning_tops = talib.CDLSPINNINGTOP(open, high, low, close)
    takuris = talib.CDLTAKURI(open, high, low, close)

    named_series = pd.Series[float](
        "None",
        index=close.index,
    )
    named_series[dojis] = "doji"
    named_series[doji_stars] = "doji_star"
    named_series[dragonfly_dojis] = "dragonfly_doji"
    named_series[marubozus] = "marubozu"
    named_series[hammers] = "hammer"
    named_series[inverted_hammers] = "inverted_hammer"
    named_series[gravestone_dojis] = "gravestone_doji"
    named_series[longlegged_dojis] = "longlegged_doji"
    named_series[longlines] = "longline"
    named_series[spinning_tops] = "spinning_top"
    named_series[takuris] = "takuri"

    return named_series


def body_length(open: pd.Series[float], close: pd.Series[float]) -> pd.Series[float]:
    return np.abs(open - close)


def wick_length(
    open: pd.Series[float], close: pd.Series[float], high: pd.Series[float]
) -> pd.Series[float]:
    return high - np.maximum(open, close)


def tail_length(
    open: pd.Series[float], close: pd.Series[float], low: pd.Series[float]
) -> pd.Series[float]:
    return np.minimum(open, close) - low


def is_bullish(open: pd.Series[float], close: pd.Series[float]) -> pd.Series[float]:
    return open < close


def is_bearish(open: pd.Series[float], close: pd.Series[float]) -> pd.Series[float]:
    return open > close


def is_hammer_like(
    open: pd.Series[float],
    close: pd.Series[float],
    high: pd.Series[float],
    low: pd.Series[float],
) -> pd.Series[bool]:
    bl = body_length(open=open, close=close)
    return (tail_length(open=open, close=close, low=low) > (bl * 2)) & (
        wick_length(open=open, close=close, high=high) < bl
    )


def is_inverted_hammer_like(
    open: pd.Series[float],
    close: pd.Series[float],
    high: pd.Series[float],
    low: pd.Series[float],
) -> pd.Series[bool]:
    bl = body_length(open=open, close=close)
    return (wick_length(open=open, close=close, high=high) > (bl * 2)) & (
        tail_length(open=open, close=close, low=low) < bl
    )


def is_engulfed(
    shortest_open: pd.Series[float],
    shortest_close: pd.Series[float],
    longest_open: pd.Series[float],
    longest_close: pd.Series[float],
) -> pd.Series[bool]:
    return body_length(open=shortest_open, close=shortest_close) < body_length(
        open=longest_open, close=longest_close
    )


def is_gap(
    lowest_open: pd.Series[float],
    lowest_close: pd.Series[float],
    upmost_open: pd.Series[float],
    upmost_close: pd.Series[float],
) -> pd.Series[bool]:
    return np.maximum(lowest_open, lowest_close) < np.minimum(upmost_open, upmost_close)


def is_gap_up(open: pd.Series[float], close: pd.Series[float]) -> pd.Series[bool]:
    open_previous = open.shift(1)
    close_previous = close.shift(1)
    return is_gap(
        lowest_open=open_previous,
        lowest_close=close_previous,
        upmost_open=open,
        upmost_close=close,
    )


def is_gap_down(open: pd.Series[float], close: pd.Series[float]) -> pd.Series[bool]:
    open_previous = open.shift(1)
    close_previous = close.shift(1)
    return is_gap(
        lowest_open=open,
        lowest_close=close,
        upmost_open=open_previous,
        upmost_close=close_previous,
    )


def is_hammer(
    open: pd.Series[float],
    close: pd.Series[float],
    high: pd.Series[float],
    low: pd.Series[float],
) -> pd.Series[bool]:
    return is_bullish(open=open, close=close) & is_hammer_like(
        open=open, close=close, high=high, low=low
    )


def is_inverted_hammer(
    open: pd.Series[float],
    close: pd.Series[float],
    high: pd.Series[float],
    low: pd.Series[float],
) -> pd.Series[bool]:
    return is_bearish(open=open, close=close) & is_inverted_hammer_like(
        open=open, close=close, high=high, low=low
    )


def is_hanging_man(
    open: pd.Series[float],
    close: pd.Series[float],
    high: pd.Series[float],
    low: pd.Series[float],
) -> pd.Series[bool]:
    open_previous = open.shift(1)
    close_previous = close.shift(1)
    return (
        is_bullish(open=open_previous, close=close_previous)
        & is_bearish(open=open, close=close)
        & is_gap_up(open=open, close=close)
        & is_hammer_like(open=open, close=close, high=high, low=low)
    )


def is_shooting_star(
    open: pd.Series[float],
    close: pd.Series[float],
    high: pd.Series[float],
    low: pd.Series[float],
) -> pd.Series[bool]:
    open_previous = open.shift(1)
    close_previous = close.shift(1)
    return (
        is_bullish(open=open_previous, close=close_previous)
        & is_bearish(open=open, close=close)
        & is_gap_up(open=open, close=close)
        & is_inverted_hammer_like(open=open, close=close, high=high, low=low)
    )


def is_bullish_engulfing(
    open: pd.Series[float], close: pd.Series[float]
) -> pd.Series[bool]:
    open_previous = open.shift(1)
    close_previous = close.shift(1)
    return (
        is_bearish(open=open_previous, close=close_previous)
        & is_bullish(open=open, close=close)
        & is_engulfed(
            shortest_open=open_previous,
            shortest_close=close_previous,
            longest_open=open,
            longest_close=close,
        )
    )


def is_bearish_engulfing(
    open: pd.Series[float], close: pd.Series[float]
) -> pd.Series[bool]:
    open_previous = open.shift(1)
    close_previous = close.shift(1)
    return (
        is_bullish(open=open_previous, close=close_previous)
        & is_bearish(open=open, close=close)
        & is_engulfed(
            shortest_open=open_previous,
            shortest_close=close_previous,
            longest_open=open,
            longest_close=close,
        )
    )


def is_bullish_harami(
    open: pd.Series[float], close: pd.Series[float]
) -> pd.Series[bool]:
    open_previous = open.shift(1)
    close_previous = close.shift(1)
    return (
        is_bearish(open=open_previous, close=close_previous)
        & is_bullish(open=open, close=close)
        & is_engulfed(
            shortest_open=open,
            shortest_close=close,
            longest_open=open_previous,
            longest_close=close_previous,
        )
    )


def isBearishHarami(open: pd.Series[float], close: pd.Series[float]) -> pd.Series[bool]:
    open_previous = open.shift(1)
    close_previous = close.shift(1)
    return (
        is_bullish(open=open_previous, close=close_previous)
        & is_bearish(open=open, close=close)
        & is_engulfed(
            shortest_open=open,
            shortest_close=close,
            longest_open=open,
            longest_close=close,
        )
    )


def is_bullish_kicker(
    open: pd.Series[float], close: pd.Series[float]
) -> pd.Series[bool]:
    open_previous = open.shift(1)
    close_previous = close.shift(1)
    return (
        is_bearish(open=open_previous, close=close_previous)
        & is_bullish(open=open, close=close)
        & is_gap_up(open=open, close=close)
    )


def is_bearish_kicker(
    open: pd.Series[float], close: pd.Series[float]
) -> pd.Series[bool]:
    open_previous = open.shift(1)
    close_previous = close.shift(1)
    return (
        is_bullish(open=open_previous, close=close_previous)
        & is_bearish(open=open, close=close)
        & is_gap_down(open=open, close=close)
    )


def name_candlesticks_old(
    open: pd.Series[float],
    close: pd.Series[float],
    high: pd.Series[float],
    low: pd.Series[float],
) -> pd.Series[str]:
    diff_hi_low = high / low - 1
    diff_close_open = close / open - 1
    odds_head_tail_and_body = abs(diff_hi_low / diff_close_open)
    diff_high_close_open = np.abs(high / (np.maximum(close, open)) - 1)
    diff_low_close_open = np.abs(low / (np.minimum(close, open)) - 1)
    odds_head_tail = diff_high_close_open / diff_low_close_open

    doji = (odds_head_tail_and_body >= 5) & (np.abs(diff_close_open) <= 0.006)
    spinning_top = (
        (odds_head_tail_and_body >= 1.3)
        & (np.abs(diff_close_open) >= 0.006)
        & (np.abs(diff_close_open) <= 0.05)
        & (odds_head_tail >= 0.5)
        & (odds_head_tail <= 2)
    )
    marubozu = (np.abs(diff_close_open) >= 0.03) & (odds_head_tail_and_body <= 1.5)
    hammer = (odds_head_tail_and_body >= 1.5) & (
        (diff_high_close_open <= 0.0075) & (diff_low_close_open >= 0.015)
    )
    inverted_hammer = (odds_head_tail_and_body >= 1.5) & (
        (diff_low_close_open <= 0.0075) & (diff_high_close_open >= 0.015)
    )

    named_series = pd.Series[float](
        "N/A",
        index=close.index,
    )
    named_series[doji] = "DOJI"
    named_series[spinning_top] = "SPINNING_TOP"
    named_series[marubozu] = "MARUBOZU"
    named_series[hammer] = "HAMMER"
    named_series[inverted_hammer] = "INVERTED_HAMMER"
    return named_series
