"""
Main application of the SoccerAA
"""
import numpy as np

from termcolor import colored
from app.template_processing import template_processor
from app.image_handling import image_provider
from app.detection import detector as dt
from app.tracking import tracker as trck
from app import config
import cv2 as cv


def run():
    print('processing templates:\n')

    # Process templates
    templates = template_processor.process_templates()
    print(colored('-- {} templates processed!'.format(len(templates)), 'green'))

    # Init image provider
    stream = image_provider.ImageProvider(config.TARGET_COMPRESSION, config.TARGET_COMPRESSION_RATE, config.BACKTRACKNG)
    if config.INPUT_VIDEO:
        print("-- taking video input --")
        stream.set_video_source(config.DIR_VIDEOS + config.VIDEO_FILENAME)
    else:
        print("-- taking pictures input --")
        stream.set_images_source(config.DIR_TARGETS)

    # init advertisment detection
    detector = dt.Detector(templates)

    # init tracker
    tracker = trck.Tracker()

    check_frame, frame = stream.next()

    while check_frame:
        frame_plain = frame.copy()

        img1 = frame.copy()

        logos_tracked, frame = tracker.update(frame)

        logos, frame = detector.detect(frame)

        for key in logos:
            for logo in logos[key]:
                img1 = cv.polylines(img1, [logo], True, 255, 6, cv.LINE_AA)

        for key in logos_tracked:
            for logo in logos_tracked[key]:
                img1 = cv.polylines(img1, [logo], True, 255, 6, cv.LINE_AA)

        cv.imshow('deteckted logos', img1)
        cv.waitKey(0)
        cv.destroyAllWindows()

        tracker.add_objects(logos, frame_plain)
        check_frame, frame = stream.next()
        print("okk")




if __name__ == "__main__":
    run()