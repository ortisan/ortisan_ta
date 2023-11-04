# def test_body_length():
#     open = pd.Series([2, 2, 2], copy=False)
#     close = pd.Series([4, 4, 4], copy=False)
#     bodylen = candlestick.body_length(open=open, close=close)
#     expeted = pd.Series([2, 2, 2])
#     assert_series_equal(expeted, bodylen)

#     open = pd.Series([4, 4, 4], copy=False)
#     close = pd.Series([2, 2, 2], copy=False)
#     bodylen = candlestick.body_length(open=open, close=close)
#     expeted = pd.Series([2, 2, 2])
#     assert_series_equal(expeted, bodylen)


# def test_wick_length():
#     open = pd.Series([2, 2, 2], copy=False)
#     close = pd.Series([4, 4, 4], copy=False)
#     high = pd.Series([5, 5, 5], copy=False)
#     wicklen = candlestick.wick_length(open=open, close=close, high=high)
#     expeted = pd.Series([1, 1, 1])
#     assert_series_equal(expeted, wicklen)


# def test_tail_length():
#     open = pd.Series([2, 2, 2], copy=False)
#     close = pd.Series([4, 4, 4], copy=False)
#     low = pd.Series([1, 1, 1], copy=False)
#     taillen = candlestick.tail_length(open=open, close=close, low=low)
#     expeted = pd.Series([1, 1, 1])
#     assert_series_equal(expeted, taillen)


# def test_is_bullish():
#     open = pd.Series([2, 2, 2], copy=False)
#     close = pd.Series([4, 1, 4], copy=False)
#     expeted = pd.Series([True, False, True])
#     bullish_test = candlestick.is_bullish(open, close)
#     assert_series_equal(expeted, bullish_test)


# def test_is_bearish():
#     open = pd.Series([2, 2, 2], copy=False)
#     close = pd.Series([4, 1, 4], copy=False)
#     expeted = pd.Series([False, True, False])
#     bearish_test = candlestick.is_bearish(open, close)
#     assert_series_equal(expeted, bearish_test)
