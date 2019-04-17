"""
Generates Reports and tagged video or images
"""

import app.result_processing.helper as hlp
import numpy as np
import cv2 as cv

class Result:
    def __init__(self, compression_rate):
        self._compression_rate = compression_rate

    def process(self, image, logos_detected, logos_tracked):
        found_logos = dict()
        for logo in logos_tracked:
            logos_scaled = hlp.scale_logos(logos_tracked[logo], self._compression_rate)
            found_logos[logo] = logos_scaled

        for logo in logos_detected:
            logos_scaled = hlp.scale_logos(logos_detected[logo], self._compression_rate)
            if logo in found_logos:
                # Todo: test if other way possible
                found_logos[logo] = np.concatenate((found_logos[logo], logos_scaled))
            else:
                found_logos[logo] = logos_scaled

        # Print whole image
        for logo in found_logos:
            image = cv.polylines(image, found_logos[logo], True, 255, 3, cv.LINE_AA)

        cv.imshow('result', image)

        # press any key to pause, exc to exit
        k = cv.waitKey(1) & 0xff
        if k == 27:
            exit()