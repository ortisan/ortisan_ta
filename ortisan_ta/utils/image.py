# coding=utf-8
__author__ = 'Marcelo Ortiz'
import numpy as np
import pandas as pd
import uuid
from PIL import Image, ImageDraw


def scale_between(unscaled_number, min_allowed, max_allowed, min, max):
    return ((max_allowed - min_allowed) * (unscaled_number - min) / (max - min)) + min_allowed


def gen_candlesticks(high: pd.Series, low: pd.Series, close: pd.Series, open: pd.Series, directory="."):
    height = 128
    width = 128
    half_height = height/2
    half_width = width/2

    for i, v in close.items():
        max_high = np.max(high)
        min_low = np.min(low)

        high1 = high[i]
        low1 = low[i]
        close1 = close[i]
        open1 = open[i]

        y1 = scale_between(low1, 0, height, min_low, max_high)
        y2 = scale_between(high1, 0, height, min_low, max_high)

        # Calculate the center of object
        object_height = y2 - y1
        half_object_height = object_height/2

        candle_body_y1 = scale_between(
            min(open1, close1), 0, height, min_low, max_high)
        candle_body_y2 = scale_between(
            max(open1, close1), 0, height, min_low, max_high)

        translate_y = (half_height - (y1 + half_object_height))
        center_y1 = y1 + translate_y
        center_y2 = y2 + translate_y

        candle_body_y1_trans = candle_body_y1 + translate_y
        candle_body_y2_trans = candle_body_y2 + translate_y

        im = Image.new('RGB', (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(im)
        # line
        #draw.rectangle((0, half_height, width, half_height), fill=(0, 0, 0), outline=(0, 0, 0))
        draw.rectangle((width/2, center_y1, width/2, center_y2),
                       fill=(0, 0, 0), outline=(0, 0, 0))
        # body
        fill_color = (0, 0, 0)
        if close1 > open1:
            fill_color = (255, 255, 255)
        draw.rectangle((half_width-5, candle_body_y1_trans, half_width+5,
                        candle_body_y2_trans), fill=fill_color, outline=(0, 0, 0))

        im.save(f'{directory}/{str(uuid.uuid1())}.jpg')
