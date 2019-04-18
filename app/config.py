"""
Configuration for the SoccerAA
"""

DIR_TEMPLATES = '../data/in/templates/'
DIR_TARGETS = '../data/in/targets/'
DIR_VIDEOS = '../data/in/videos/'
DIR_OUT = '../data/out/'
IMAGE_OUT_NAME = 'result_{}.png'
VIDEO_OUT_NAME = 'result.avi'

DEBUG = True
SHOW_PROCESS = False
INPUT_VIDEO = False
VIDEO_FILENAME = ''
SHOW_IGNORE_AREA = True

# Features:
ADD_ORIGINAL_TEMPLATE = True
ADD_DISTORTED_TEMPLATE = True
TARGET_COMPRESSION = True
FLANN_MATCHER = True
FAST_TRACKER = True
TRACK_EMPTY_AREA = True
DELAYED_TRACK_EMPTY_AREA = False
LAZY_SEARCH = False


# Prameters:
TEMPLATE_WIDTH_SCALE = 0.7
TEMPLATE_HEIGHT_SHIFT = 0.4
TARGET_COMPRESSION_RATE = 0.5
FLANN_ALGORITHM = 1
MATCHING_TOLERANCE = 0.7
MIN_MATCHING_COUNT = 10
TEMPLATE_RATIO_THRESHOLD = 4
EMPTY_BOX_OFFSET = 2
EMPTY_BOX_IN_FRAME = 40
EMPTY_TRACKER_DELAY = 0

#Drawing Parameters:
LOGO_BOX_COLOR = (0, 0, 255)
LOGO_BOX_THIKNESS = 2
LOGO_TEXT_VERTICAL_OFFSET = - 50
LOGO_TEXT_HORIZONTAL_OFFSET = 20
LOGO_TEXT_COLOR = (0, 255, 0)
LOGO_TEXT_SIZE = 0.75







