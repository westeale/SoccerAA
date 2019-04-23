"""
Color Filtering to boost SIFT searching
"""

import cv2 as cv
import numpy as np



def color_filter(img, colors):
    """
    Filtering out cololors with largest distance of given colors
    :param img: image to filter
    :param colors: list of hsv colors to keep
    :return: img with filtered colors
    """
    if colors is None:
        return img

    bounds = {}
    i = 0
    for color in colors:
        hsv = create_bounds(color)
        bounds[i] = {"lower": hsv[0], "upper": hsv[1]}
        i += 1

    i = 0
    masks = []

    for _ in bounds:
        masks.append(create_mask(img, bounds[i]["lower"], bounds[i]["upper"]))
        i += 1

    masks.append(black_and_white_mask(img))

    res = []
    for mask in masks:
        res.append(cv.bitwise_and(img, img, mask=mask))

    result = res[0]
    for i in range(1, len(res)):
        result = cv.bitwise_or(result, res[i])

    return result


def black_and_white_mask(img):
    kernel = np.ones((50, 50))
    low = np.array([0, 0, 0])
    up = np.array([180, 80, 255])
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask = cv.inRange(img_hsv, low, up)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
    return mask


def create_mask(img, lower_bound, upper_bound):
    low = np.array(lower_bound)
    up = np.array(upper_bound)
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask = cv.inRange(img_hsv, low, up)
    return mask


def create_bounds(hsv):
    h = hsv[0] - 20
    if h < 0:
        h = 0

    lower_bound = [h, int(round(hsv[1] * 0.3)), int(round(hsv[2] * 0.6))]
    upper_bound = [hsv[0] + 20, 255, 255]
    return lower_bound, upper_bound