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
        frame_copy = frame.copy()
        logos = detector.detect(frame)

        for name, boxes in logos.items():
            frame = cv.polylines(frame_copy, boxes, True, 255, 6, cv.LINE_AA)
            cv.imshow(name, frame_copy)
            cv.waitKey(0)
            cv.destroyAllWindows()

        check_frame, frame = stream.next()




if __name__ == "__main__":
    run()