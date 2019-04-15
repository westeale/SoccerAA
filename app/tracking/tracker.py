"""
Tracking already found advertisements
"""
import numpy as np

from app import config
import app.tracking.helper as hlp
import cv2 as cv

def create_tracker():
    if config.FAST_TRACKER:
        return cv.TrackerMOSSE_create()
    else:
        return cv.TrackerMedianFlow_create()


class ObjectTracker:
    def __init__(self, frame, rectangle, offsets,  logo_name):
        self.name = logo_name
        self.tracking = create_tracker()
        self.tracking.init(frame, rectangle)
        self.offsets = offsets



class Tracker:
    def __init__(self):
        self._object_trackers = list()


    def add_objects(self, logos, frame):
        #(abstand links, abstand oben, abstand links, abstand oben)
        for name in logos:
            boxes = logos[name]
            for box in boxes:
                rectangle, offsets = hlp.calc_rectangle(box)

                self._object_trackers.append(ObjectTracker(frame, rectangle, offsets, name))

                original_frame = frame.copy()
                p1 = (int(rectangle[0]), int(rectangle[1]))
                p2 = (int(rectangle[0] + rectangle[2]), int(rectangle[1] + rectangle[3]))
                cv.rectangle(original_frame, p1, p2, (255, 255, 255), 2, 1)


    def update(self, frame):
        frame_height, _ = frame.shape[:2]

        original_frame = frame.copy()
        logos = dict()
        for object_tracker in self._object_trackers:
            check_tracker, rectangle = object_tracker.tracking.update(original_frame)

            if not check_tracker:
                # Object lost
                self._object_trackers.remove(object_tracker)
                continue

            black_bar = hlp.fill_rectangle(rectangle, frame_height)
            frame = cv.fillPoly(frame, [black_bar], 0)
            offsets = object_tracker.offsets
            destination_polygon = hlp.calc_polygon(rectangle, offsets)
            dst = destination_polygon

            if object_tracker.name in logos:
                logos[object_tracker.name].append(dst)
            else:
                logos[object_tracker.name] = [dst]


        return logos, frame







