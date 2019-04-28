"""
Tracking already found advertisements
"""
import numpy as np

from app import config
import app.tracking.helper as hlp
from termcolor import colored
import cv2 as cv


def create_tracker(fast_tracker):
    if fast_tracker:
        return cv.TrackerKCF_create()
    else:
        return cv.TrackerMedianFlow_create()


class ObjectTracker:
    def __init__(self, frame, rectangle, fast_tracker=False, offsets=None,  logo_name=None):
        self.name = logo_name
        self.tracking = create_tracker(fast_tracker)
        self.tracking.init(frame, rectangle)
        self.offsets = offsets
        self.current_box_position = None


class Tracker:
    def __init__(self):
        self._object_trackers = list()
        self._empyt_tracker = None
        self._n_tracked_frames = 0
        self._n_empty_frames = 0


    def add_objects(self, logos, frame):
        #(abstand links, abstand oben, abstand links, abstand oben)
        for name in logos:
            boxes = logos[name]
            for box in boxes:
                rectangle, offsets = hlp.calc_rectangle(box)
                # self._object_trackers.append(ObjectTracker(frame, rectangle, config.FAST_TRACKER, offsets, name))
                try:
                    self._object_trackers.append(ObjectTracker(frame, rectangle, config.FAST_TRACKER, offsets, name))
                except:
                    print(colored(' Failed to register tracker with rectangle: {}'.format(rectangle), 'red'))



    def update(self, frame):
        frame_height, frame_width = frame.shape[:2]
        self._n_tracked_frames = 0
        # Track logos
        keep_trackers = list()
        original_frame = frame.copy()
        logos = dict()
        for object_tracker in self._object_trackers:
            check_tracker, rectangle = object_tracker.tracking.update(original_frame)

            if not check_tracker:
                # Object lost
                continue

            if not hlp.in_frame(frame_width, rectangle):
                continue


            self._n_tracked_frames += 1
            black_bar = hlp.fill_bar(rectangle, frame_height)
            frame = cv.fillPoly(frame, [black_bar], 0)
            offsets = object_tracker.offsets
            try:
                destination_polygon = hlp.calc_polygon(rectangle, offsets)
            except:
                print(colored(' Failed to calculate polygon with rectangle {} and offset {}'.format(rectangle, offsets), 'red'))
                continue

            keep_trackers.append(object_tracker)

            dst = destination_polygon

            if object_tracker.name in logos:
                logos[object_tracker.name].append(dst)
            else:
                self._n_empty_frames = 0
                logos[object_tracker.name] = [dst]

        self._object_trackers = keep_trackers

        # Track empty frame
        if self._empyt_tracker:
            check_tracker, rectangle = self._empyt_tracker.tracking.update(original_frame)

            if not check_tracker:
                # Object lost
                self._empyt_tracker = None
            else:
                if not hlp.box_in_frame(frame_height, frame_width, rectangle, config.EMPTY_BOX_IN_FRAME):
                    self._empyt_tracker = None

                black_bar = hlp.fill_rectangle(rectangle)
                frame = cv.fillPoly(frame, [black_bar], 0)

        return logos, frame



    def add_empty_area(self, frame):
        if not self._empyt_tracker:
            if self._n_empty_frames < config.EMPTY_TRACKER_DELAY:
                self._n_empty_frames += 1
                return
            else:
                self._n_empty_frames = 0

            frame_height, frame_width = frame.shape[:2]
            box = hlp.calc_frame_box(frame_height, frame_width, config.EMPTY_BOX_OFFSET)
            self._empyt_tracker = ObjectTracker(frame, box, True)


    @property
    def n_tracked_frames(self):
        return self._n_tracked_frames






