"""
Provides stream of images based on input
cashes previous images for backtracking
"""

import os
import cv2 as cv

from app import config


class ImageProvider():
    def __init__(self, compression=False, compression_rate=0.5, backtracking=False):
        self._video = False
        self._cap = None
        self._image_dir = None
        self._image_names = list()
        self._compression = compression
        self._compression_rate = compression_rate
        self._original_frame = None
        self._backtracking = backtracking
        self._tracked_frames = list()
        self._n_frames = 0
        self._n_tracked_frame = 0
        pass

    def set_video_source(self, video_dir):
        self._video = True
        self._cap = cv.VideoCapture(video_dir)

    def set_images_source(self, images_dir):
        self._image_dir = images_dir
        self._image_names = os.listdir(images_dir)

    def next(self):
        if self._video:
            if config.SKIP_FRAMES:
                for _ in range(config.SKIPPING_FRAMES):
                    self._cap.read()
            check, img = self._cap.read()
        else:
            if len(self._image_names) <= 0:
                img = None
                check = False
            else:
                img_name = self._image_names.pop()
                img = cv.imread(self._image_dir + img_name)
                if img is None:
                    raise Exception('{} is not an OpenCV compatible image!'.format(img_name))

                check = True
        if not check:
            return False, None

        self._n_frames += 1
        self._original_frame = img

        if self._backtracking:
            self._n_tracked_frame = self._n_frames
            self._tracked_frames.append(img)

        # Compress image
        if self._compression:
            img = cv.resize(img, None, fx=self._compression_rate, fy=self._compression_rate, interpolation=cv.INTER_CUBIC)

        return True, img

    def previous(self):
        if len(self._tracked_frames) <= 0:
            return False, None
        else:
            self._n_tracked_frame -= 1
            if self._n_tracked_frame < 0:
                return False, None

            img = self._tracked_frames[self._n_tracked_frame]

        return True, img






