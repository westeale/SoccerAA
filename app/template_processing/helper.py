"""
Helper functions for template processing
"""

import numpy as np
import cv2 as cv


def rescale(img, scale_width, shift_height=0):
    height, width = img.shape[:2]

    width_new = round(width * scale_width)
    shift_height = round(shift_height * width)

    points1 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    if shift_height > 0:
        points2 = np.float32([[0, 0], [width_new, shift_height], [0, height], [width_new, height + shift_height]])
    else:
        points2 = np.float32([[0, -shift_height], [width_new, 0], [0, height - shift_height], [width_new, height]])

    transformation_matrix = cv.getPerspectiveTransform(points1, points2)
    img_rescaled = cv.warpPerspective(img, transformation_matrix, (width_new, height + abs(shift_height)))

    return img_rescaled, shift_height


def extract_dominant_colors(img, n_colors=2):
    """
    Extracts the most n dominant colors from image
    :param img: opencv-image (bgr)
    :param n_colors: number of dominant colors (bgr)
    :return: average color and list of dominant colors (bgr)
    """
    img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    average_color = img.mean(axis=0).mean(axis=0)
    pixels = np.float32(img.reshape(-1, 3))

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 200, .1)

    flags = cv.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv.kmeans(pixels, n_colors, None, criteria, 10, flags)

    return average_color, palette


# -----------------Tests--------------------------------
def __test_extract_dominant_colors():
    test_img = cv.imread('../../data/tests/adidas.png')
    average_color, palette = extract_dominant_colors(test_img)

    assert np.around(average_color).tolist() == [73, 210, 100]
    assert np.around(palette).tolist() == [[32, 231, 246], [100, 197, 7]]


def __test_scale_image():
    test_img = cv.imread('../../data/tests/wanda.png')
    _, height_shift = rescale(test_img, 0.7, 0.3)
    assert height_shift == 489


if __name__ == "__main__":
    __test_extract_dominant_colors()
    __test_scale_image()
