"""
preprocess and extracting template information
"""

import os
import cv2 as cv
import app.template_processing.helper as hlp

from app import config
from termcolor import colored

feature_detector = cv.xfeatures2d.SIFT_create()

class Feature:
    def __init__(self, img, vertical_shift=0):
        self._img = img
        self._vertical_shift = vertical_shift
        self._keypoints = None
        self._descriptors = None
        self.compute_features()


    def compute_features(self):
        img_gray = cv.cvtColor(self._img, cv.COLOR_BGR2GRAY)
        keypoints, descriptors = feature_detector.detectAndCompute(img_gray, None)
        self._keypoints = keypoints
        self._descriptors = descriptors

        if config.DEBUG:
            print("  {} Keypoints registered".format(len(keypoints)))

    @property
    def keypoints(self):
        return self._keypoints

    @property
    def descriptors(self):
        return self._descriptors

    @property
    def vertical_shift(self):
        return self._vertical_shift

    @property
    def img(self):
        return self._img


def extract_features(img):
    features = list()

    if config.ADD_ORIGINAL_TEMPLATE:
        features.append(Feature(img))

    img_scaled, _ = hlp.rescale(img, config.TEMPLATE_WIDTH_SCALE)
    features.append(Feature(img_scaled))

    if config.ADD_DISTORTED_TEMPLATE:
        img_shifted_up, shift_up = hlp.rescale(img_scaled, 1, config.TEMPLATE_HEIGHT_SHIFT)
        img_shifted_down, shift_down = hlp.rescale(img_scaled, 1, -config.TEMPLATE_HEIGHT_SHIFT)
        features.append(Feature(img_shifted_up, shift_up))
        features.append(Feature(img_shifted_down, shift_down))

    return features


class Template:
    def __init__(self, img, name, n_colors):
        self._img = img
        self._name = name
        self._average_color, self._dominant_colors = hlp.extract_dominant_colors(img, n_colors)
        self._features = extract_features(img)
        self._ratio = (img.shape[:2][1]/img.shape[:2][0])

    @property
    def features(self):
        return self._features

    @property
    def name(self):
        return self._name

    @property
    def ratio(self):
        return self._ratio

    @property
    def average_color(self):
        return self._average_color

    @property
    def dominant_colors(self):
        return self._dominant_colors


def process_templates():
    templates = []

    for file in os.listdir(config.DIR_TEMPLATES):
        img = cv.imread(config.DIR_TEMPLATES + file)
        template_attributes = file.split(".")
        template_name = template_attributes[0]
        print("processing template: {}".format(template_name))
        n_colors = 2
        if len(template_attributes) > 2:
            try:
                n_colors = int(str(template_attributes[1]).replace("-", ""))
                if config.DEBUG:
                    print("{} colors for {} set".format(n_colors, template_name))
            except:
                print(colored('Could not read out n colors from template. using: 2', 'magenta'))

        if img is None:
            raise Exception('{} is not an OpenCV compatible image!'.format(template_name))

        template = Template(img, template_name, n_colors)
        print(colored('\t-OK\n', 'green'))
        templates.append(template)

    return templates


if __name__ == "__main__":
    process_templates()