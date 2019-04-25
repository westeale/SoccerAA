"""
Entry point for the Soccer Advertisment Analyser
"""

import argparse
from app import config, core

accuracies = {'low': 0, 'medium': 1, 'high': 2}

parser = argparse.ArgumentParser()

parser.add_argument('--input', help="Set to images or name of video. Default is: images", default='images')
parser.add_argument('--accuracy', help="Set accuracy of ad detection (low accuracy has highest performance)", default='high', choices=[key for key in accuracies.keys()])
parser.add_argument('-debug', help="Show debug messages in console", action='store_true')
parser.add_argument('-out', help="Show real time image processing", action='store_true')
parser.add_argument('-tr', help="Shows areas to ignore", action='store_true')


def init():
    args = parser.parse_args()

    config.SHOW_PROCESS = args.out
    config.DEBUG = args.debug
    config.SHOW_IGNORE_AREA = args.tr

    if args.input != 'images':
        config.VIDEO_FILENAME = args.input
        config.INPUT_VIDEO = True

    set_accuracy(accuracies[args.accuracy])

    core.run()

def set_accuracy(accuracy):
    if accuracy == 0:
        # features for high perfmance
        config.TARGET_COMPRESSION = True
        config.FLANN_MATCHER = False
        config.LAZY_SEARCH = True
        config.FAST_TRACKER = True

    elif accuracy == 1:
        # features for medium perfmance
        config.TARGET_COMPRESSION = True
        config.FLANN_MATCHER = False


if __name__ == "__main__":
    init()
