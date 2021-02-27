# coding=utf-8
__author__ = 'Marcelo Ortiz'

import numpy as np
import pandas as pd
import uuid
import svgwrite
import json
import re


def scale_between(unscaled_number, min_allowed, max_allowed, min, max):
    return ((max_allowed - min_allowed) * (unscaled_number - min) / (max - min)) + min_allowed


candle_types = ['doji', 'marubozu', 'spinning top',
                'long candle', 'hammer', 'inverted_hammer']


def gen_candlesticks(high_values: pd.Series, low_values: pd.Series, close_values: pd.Series, open_values: pd.Series, directory="."):

    width = 1000
    height = 1000
    half_width = width/2
    half_height = height/2
    # Candle Body is 10%
    candle_body_width = width * 0.1
    line_x = half_width
    candle_body_x1 = half_width - (candle_body_width / 2)

    max_high = np.max(high_values)
    min_low = np.min(low_values)

    data = []
    for i, v in close_values.items():

        h = high_values[i]
        l = low_values[i]
        c = close_values[i]
        o = open_values[i]

        h_scaled = scale_between(h, 0, height, min_low, max_high)
        l_scaled = scale_between(l, 0, height, min_low, max_high)
        c_scaled = scale_between(c, 0, height, min_low, max_high)
        o_scaled = scale_between(o, 0, height, min_low, max_high)

        candle_body_y1 = min(o_scaled, c_scaled)
        candle_body_y2 = max(o_scaled, c_scaled)

        # Calculate the center of object
        object_height = h_scaled - l_scaled
        half_object_height = object_height/2
        candle_body_height = candle_body_y2 - candle_body_y1

        translate_y = (half_height - (l_scaled + half_object_height))

        y1 = l_scaled + translate_y
        y2 = h_scaled + translate_y
        candle_body_y1 = candle_body_y1 + translate_y

        id = re.sub('[^0-9]', '', str(i)) + "_1"
        name = f'{id}.svg'
        filename = f'{directory}/{name}'

        dwg = svgwrite.Drawing(filename, size=(width, height))

        # red
        fill_color = svgwrite.rgb(255, 0, 0)
        stroke_color = svgwrite.rgb(139, 100, 0)
        # green
        if c > o:
            stroke_color = svgwrite.rgb(0, 100, 0)
            fill_color = svgwrite.rgb(0, 128, 0, '%')

        # we rotate 180 because the screen y is inverted
        line = dwg.line((line_x, y1), (line_x, y2), stroke=stroke_color)
        line.rotate(180, center=(half_width, half_width))
        dwg.add(line)
        rect = dwg.rect(insert=(candle_body_x1, candle_body_y1), size=(
            candle_body_width, candle_body_height), stroke=stroke_color, fill=fill_color)
        rect.rotate(180, center=(half_width, half_width))
        dwg.add(rect)

        data.append({'id': id, 'name': name, 'label': '', 'features': {
                    'high': h, 'low': l, 'close': c, 'open': o}})
        dwg.save()

    with open(f'{directory}/image_data.json', 'w') as json_file:
        json.dump({'type': 'candlestick classifier', 'data': data,
                   'labels': candle_types}, json_file)
