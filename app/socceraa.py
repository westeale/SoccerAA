"""
Entry point for the Soccer Advertisment Analyser
"""

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--input', help="Set to images or name of video. Default is: images", default='images')
parser.add_argument('--accuracy', help="Set accuracy of ad detection (low accuracy has highest performance)", default='high', choices=['low', 'medium', 'high'])
parser.add_argument('-out', help="Show analysis during processing", action='store_true')


def init():
    args = parser.parse_args()
    print(args.input)
    print(args.accuracy)
    print(args.out)


if __name__ == "__main__":
    init()
