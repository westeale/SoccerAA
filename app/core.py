"""
Main application of the SoccerAA
"""
import numpy as np

from termcolor import colored
from app.template_processing import template_processor
from app.image_handling import image_provider
from app.detection import detector as dt
from app.tracking import tracker as trck
from app.result_processing import result_generator
from app import config
from app import helper as hlp
import cv2 as cv

track_empty_space = config.TRACK_EMPTY_AREA or config.DELAYED_TRACK_EMPTY_AREA


def run():
    print('processing templates:\n')

    # Process templates
    templates = template_processor.process_templates()
    print(colored('-- {} templates processed!'.format(len(templates)), 'green'))

    # Init image provider
    stream = image_provider.ImageProvider(config.TARGET_COMPRESSION, config.TARGET_COMPRESSION_RATE)
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

    # init Result generator
    result = result_generator.Result(config.TARGET_COMPRESSION_RATE)

    logos_detected = None
    check_frame, frame = stream.next()
    n_logos_tracked = 0
    while check_frame:
        frame_plain = frame.copy()

        logos_tracked, frame = tracker.update(frame)

        if hlp.search_logos(tracker.n_tracked_frames, n_logos_tracked):
            logos_detected, frame = detector.detect(frame)

        if track_empty_space and not logos_tracked and not logos_detected:
            tracker.add_empty_area(frame_plain)

        tracker.add_objects(logos_detected, frame_plain)

        for key in logos_detected:
            for logo in logos_detected[key]:
                frame_plain = cv.polylines(frame_plain, [logo], True, 255, 6, cv.LINE_AA)

        for key in logos_tracked:
            for logo in logos_tracked[key]:
                frame_plain = cv.polylines(frame_plain, [logo], True, 255, 6, cv.LINE_AA)

        result.process(stream.current_frame, logos_detected, logos_tracked)

        # cv.imshow('deteckted logos', frame )
        # cv.waitKey(0)
        # cv.destroyAllWindows()

        n_logos_tracked = tracker.n_tracked_frames
        check_frame, frame = stream.next()


if __name__ == "__main__":
    run()