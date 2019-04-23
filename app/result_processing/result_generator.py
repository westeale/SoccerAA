"""
Generates Reports and tagged video or images
"""
import sys
import time

from termcolor import colored

import app.result_processing.helper as hlp
import numpy as np
import cv2 as cv

from app import config


class Out:
    def __init__(self):
        self._video_writer = None
        self._frame_counter = 0


    def init_video_writer(self, frame_size, frame_rate):
        fourcc = cv.VideoWriter_fourcc(*'DIVX')
        self._video_writer = cv.VideoWriter(config.DIR_OUT + config.VIDEO_OUT_NAME, fourcc, frame_rate, frame_size)

    def write(self, img):
        if config.INPUT_VIDEO:
            self._video_writer.write(img)
        else:
            cv.imwrite(config.DIR_OUT + config.IMAGE_OUT_NAME.format(self._frame_counter), img)
            self._frame_counter += 1

    def finalize(self):
        if config.INPUT_VIDEO:
            self._video_writer.release()


class Result:
    def __init__(self, compression_rate, frame_size, n_frames, frame_rate=0):
        self._compression_rate = compression_rate
        self._out = Out()
        self._frame_rate = frame_rate
        self._frame_size = (frame_size[1], frame_size[0])
        self._out.init_video_writer(self._frame_size, frame_rate)
        self._found_logos = list()
        self._n_frames = n_frames


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

        logos = dict()
        for logo in found_logos:
            cv.polylines(image, found_logos[logo], True, config.LOGO_BOX_COLOR, config.LOGO_BOX_THIKNESS, cv.LINE_AA)
            n_logos = 0
            for box in found_logos[logo]:
                position = (box[2][0][0] + config.LOGO_TEXT_VERTICAL_OFFSET, box[2][0][1] + config.LOGO_TEXT_HORIZONTAL_OFFSET)
                cv.putText(image, logo, position, cv.FONT_ITALIC, config.LOGO_TEXT_SIZE, config.LOGO_TEXT_COLOR, 2)
                n_logos += 1

            logos[logo] = n_logos

        self._found_logos.append(logos)


        if config.SHOW_PROCESS:
            cv.imshow('result', image)

            # press any key to pause, exc to exit
            k = cv.waitKey(1) & 0xff
            if k == 27:
                exit()
            elif k == 32:
                k = 255
                while k != 32:
                    time.sleep(0.1)
                    k = cv.waitKey(1) & 0xff


        self._out.write(image)

        sys.stdout.write('\r' + colored('{} out of {} frames processed', 'blue').format(len(self._found_logos), int(self._n_frames)))
        # print(str(len(self._found_logos)) + ' frames processed', end='\r')


    def finalize(self):
        self._out.finalize()








