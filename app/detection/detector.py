"""
Detects features and matches them
with templates.

Already found advertisments are not going to be searched again
"""
import time

import numpy as np

import cv2 as cv

from app import config
from app.detection import helper


def get_matcher():
    if config.FLANN_MATCHER:
        index_params = dict(algorithm=config.FLANN_ALGORITHM, trees=5)
        search_params = dict(checks=50)
        matcher = cv.FlannBasedMatcher(index_params, search_params)
    else:
        matcher = cv.BFMatcher()

    return matcher

class Detector():
    def __init__(self, templates):
        self._templates = templates
        self._detector = cv.xfeatures2d.SIFT_create()
        self._matcher = get_matcher()

    def detect(self, frame):

        frame_height, frame_width = frame.shape[:2]

        logos = {}
        for template in self._templates:
            # TODO: frame_filtered = Filter out colors
            frame_filtered = frame.copy()
            frame_filtered = cv.cvtColor(frame_filtered, cv.COLOR_BGR2GRAY)
            ratio = template.ratio

            found_logos = list()
            for feature in template.features:

                kp1 = feature.keypoints
                des1 = feature.descriptors
                template_height, template_width = feature.img.shape[:2]
                shift = feature.vertical_shift
                logo_found = True

                while logo_found:

                    kp2, des2 = self._detector.detectAndCompute(frame_filtered, None)

                    matches = self._matcher.knnMatch(des1, des2, k=2)

                    good = []
                    for m, n in matches:
                        if m.distance < config.MATCHING_TOLERANCE * n.distance:
                            good.append(m)

                    if len(good) >= config.MIN_MATCHING_COUNT:
                        try:
                            dst = helper.calc_rectangle(kp1, kp2, good, template_height, template_width, shift)
                        except:
                            logo_found = False
                            continue

                        if not helper.check_box(dst, ratio):
                            logo_found = False
                            continue

                        found_logos.append(np.int32(dst))

                        # fill target with space (less to search):
                        dst = helper.create_bars(dst, frame_height)

                        frame = cv.fillPoly(frame, [np.int32(dst)], 0)
                        frame_filtered = cv.fillPoly(frame, [np.int32(dst)], 0)


                    else:
                        logo_found = False

            logos[template.name] = found_logos

        return logos, frame







