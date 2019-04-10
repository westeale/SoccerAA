"""
Entry point for the Soccer Advertisment Analyser
"""

import argparse
from app import config, core

accuracies = {'low': 0, 'medium': 1, 'high': 2}

parser = argparse.ArgumentParser()

parser.add_argument('--input', help="Set to images or name of video. Default is: images", default='images')
parser.add_argument('--accuracy', help="Set accuracy of ad detection (low accuracy has highest performance)", default='high', choices=[key for key in accuracies.keys()])
parser.add_argument('-print', help="Print analysis in terminal during processing", action='store_true')
parser.add_argument('-out', help="Show real time image processing", action='store_true')



def init():
    args = parser.parse_args()

    config.PRINT_INFO = args.print
    config.SHOW_PROCESS = args.out

    if args.input != 'input':
        config.VIDEO_FILENAME = args.input
        config.INPUT_VIDEO = True

    config.ACCURACY = accuracies[args.accuracy]

    core.run()


if __name__ == "__main__":
    init()
