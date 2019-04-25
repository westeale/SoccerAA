"""
Provides stream of images based on input,
cashes previous images for backtracking
"""

import os
import cv2 as cv



class ImageProvider:
    def __init__(self, compression=False, compression_rate=0.5):
        self._video = False
        self._cap = None
        self._image_dir = None
        self._image_names = list()
        self._compression = compression
        self._compression_rate = compression_rate
        self._original_frame = None
        self._n_frames = 0
        self._fps = 0
        pass

    def set_video_source(self, video_dir):
        self._video = True
        self._cap = cv.VideoCapture(video_dir)
        self._fps = self._cap.get(cv.CAP_PROP_FPS)
        self._n_frames = self._cap.get(cv.CAP_PROP_FRAME_COUNT)

    def set_images_source(self, images_dir):
        self._image_dir = images_dir
        self._image_names = os.listdir(images_dir)
        self._n_frames = len(self._image_names)

    def next(self):
        if self._video:
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

        self._original_frame = img

        # Compress image
        if self._compression:
            img = cv.resize(img, None, fx=self._compression_rate, fy=self._compression_rate, interpolation=cv.INTER_CUBIC)
        else:
            img = img.copy()

        return True, img

    def finalize(self):
        if self._video:
            self._cap.release()

    @property
    def current_frame(self):
        return self._original_frame

    @property
    def fps(self):
        return self._fps

    @property
    def frame_size(self):
        return self._original_frame.shape[:2]

    @property
    def n_frames(self):
        return self._n_frames


