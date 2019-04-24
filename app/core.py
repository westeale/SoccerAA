"""
Main application of the SoccerAA
"""
import os
import sys
import time
import psutil

from termcolor import colored
from app.template_processing import template_processor
from app.image_handling import image_provider
from app.detection import detector as dt
from app.tracking import tracker as trck
from app.result_processing import result_generator
from app import config
from app import helper as hlp

track_empty_space = config.TRACK_EMPTY_AREA or config.DELAYED_TRACK_EMPTY_AREA


def run():

    print('processing templates:\n')

    # Process templates
    templates = template_processor.process_templates()
    print(colored('-- {} templates processed!'.format(len(templates)), 'green'))

    # Init image provider
    stream = image_provider.ImageProvider(config.TARGET_COMPRESSION, config.TARGET_COMPRESSION_RATE)
    if config.INPUT_VIDEO:
        print("-- taking video input --\n")
        stream.set_video_source(config.DIR_VIDEOS + config.VIDEO_FILENAME)
    else:
        print("-- taking pictures input --\n")
        stream.set_images_source(config.DIR_TARGETS)

    # init advertisment detection
    detector = dt.Detector(templates)

    # init tracker
    tracker = trck.Tracker()

    # Read first frame
    check_frame, frame = stream.next()

    # init Result generator
    result = result_generator.Result(config.TARGET_COMPRESSION, config.TARGET_COMPRESSION_RATE, stream.frame_size, stream.n_frames, stream.fps)

    logos_detected = None

    n_logos_tracked = 0

    start_time = time.time()

    searching_time = list()

    while check_frame:
        frame_plain = frame.copy()

        logos_tracked, frame = tracker.update(frame)

        if hlp.search_logos(tracker.n_tracked_frames, n_logos_tracked):
            start_searching = time.time()
            logos_detected, frame = detector.search(frame)
            end_searching = time.time()
            searching_time.append(end_searching - start_searching)

        if track_empty_space and not logos_tracked and not logos_detected:
            tracker.add_empty_area(frame_plain)

        tracker.add_objects(logos_detected, frame_plain)

        result.process(stream.current_frame, logos_detected, logos_tracked)

        n_logos_tracked = tracker.n_tracked_frames
        check_frame, frame = stream.next()

    end_time = time.time()

    # Release video read
    stream.finalize()

    # Generate reports
    result.finalize()

    process_time = round(end_time - start_time)
    average_search_time = sum(searching_time) / len(searching_time)
    average_frame_time = process_time / result.n_frames

    print(colored('\n\n-- Finished processing', 'green'))
    print('\nTime for processing: {}'.format(process_time))
    print('Average time per frame: {}'.format(average_frame_time))
    print('Average time to search logos: {}'.format(average_search_time))


if __name__ == "__main__":
    run()