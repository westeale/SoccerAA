"""
Helper Functions for Tracking
"""
import numpy as np

from app import config

np.seterr(divide='ignore')


def calc_rectangle(polygon):
    """
    Calculates a rectangle for th etracker from a polygon.
    Calculates also the offset to reconstruct the polygon later (out of the rectangle)
    :param polygon: points of the polygon
    :return: Rectangle Points, and offsets from polygon
    """
    left1 = min(polygon[0][0][0], polygon[1][0][0])
    left2 = max(polygon[2][0][0], polygon[3][0][0])

    up1 = min(polygon[0][0][1], polygon[3][0][1])
    up2 = max(polygon[1][0][1], polygon[2][0][1])
    up_range = up2 - up1

    if polygon[0][0][1] - up1 == 0:
        o1 = 0
        o3 = 0
        o2 = up_range / (up2 - polygon[1][0][1])
        o4 = up_range / (polygon[3][0][1] - up1)
    else:
        o2 = 0
        o4 = 0
        o1 = up_range / (polygon[0][0][1] - up1)
        o3 = up_range / (up2 - polygon[2][0][1])

    points = (left1, up1, left2 - left1 , up_range)
    offsets = (o1, o2, o3, o4)
    return points, offsets


def calc_polygon(rectangle, offsets):
    """
    Calculates a polygon out of the tracked rectangle
    to visualize in picture
    :param rectangle: Points of a rectangle
    :param offsets: Offsets from up and down, each for left and right
    :return: A polygon which can be prozessed by OpenCV
    """
    polygon = np.zeros((4, 1, 2), np.int32)
    point1 = rectangle[3] + rectangle[1]
    point2 = rectangle[2] + rectangle[0]

    if offsets[0] == 0:
        polygon[1][0][1] = point1 - (rectangle[3] / offsets[1])
        polygon[3][0][1] = rectangle[1] + (rectangle[3] / offsets[3])
        polygon[0][0][1] = rectangle[1]
        polygon[2][0][1] = point1
    else:
        polygon[0][0][1] = rectangle[1] + (rectangle[3] / offsets[0])
        polygon[2][0][1] = point1 - (rectangle[3] / offsets[2])
        polygon[1][0][1] = point1
        polygon[3][0][1] = rectangle[1]

    polygon[1][0][0] = rectangle[0]
    polygon[0][0][0] = rectangle[0]
    polygon[2][0][0] = point2
    polygon[3][0][0] = point2

    return polygon


def fill_bar(rectangle, frame_height):
    """
    Creating a rectangle over the frame, to fill the whole height
    :param rectangle: points of a rectangle
    :param frame_height: height of the frame
    :return: bar over the whole frame
    """
    bar = np.zeros((4, 1, 2), np.int32)
    of1 = rectangle[2] + rectangle[0]
    bar[0][0][1] = 0
    bar[0][0][0] = rectangle[0]
    bar[1][0][0] = rectangle[0]
    bar[2][0][0] = of1
    bar[3][0][0] = of1
    bar[1][0][1] = frame_height
    bar[2][0][1] = frame_height
    bar[3][0][1] = 0

    return bar


def fill_rectangle(rectangle):
    """
    Calculate a rectangle to fill black in order to reduce infomration in frame
    :param rectangle: points of a rectangle
    :return: box to fill black
    """
    bar = np.zeros((4, 1, 2), np.int32)
    of1 = rectangle[2] + rectangle[0]
    of2 = rectangle[3] + rectangle[1]
    bar[0][0][1] = rectangle[1]
    bar[0][0][0] = rectangle[0]
    bar[1][0][0] = rectangle[0]
    bar[2][0][0] = of1
    bar[3][0][0] = of1
    bar[1][0][1] = of2
    bar[2][0][1] = of2
    bar[3][0][1] = rectangle[1]

    return bar


def calc_frame_box(frame_height, frame_width, offset):
    """
    Calculates a Box for tracking over the whole frame
    :param frame_height: height of frame
    :param frame_width: width of frame
    :param offset: left, right bottom, up offset in relation to frame size
    :return: box for tracking
    """
    offset_vertical = round(frame_height * offset / 100)
    offset_horizontal = round(frame_width * offset / 100)
    points = (offset_horizontal, offset_vertical, frame_width - offset_horizontal*2, frame_height - offset_vertical*2)
    return points


def box_in_frame(frame_height, frame_width, box, threshold):
    """
    Checks if a given box is still in frame threshold (in %)
    :param frame_height: height of frame
    :param frame_width: width of frame
    :param box: box to check
    :param threshold: threshold in %
    :return: True or False
    """
    width_threshold = round(frame_width * threshold / 100)
    height_threshold = round(frame_height * threshold / 100)
    if box[0] > width_threshold:
        return False

    if box[1] > height_threshold:
        return False

    if box[2] + box[0] < width_threshold:
        return False

    if box[3] + box[1] < height_threshold:
        return False

    return True


def in_frame(frame_width, box):
    box_length_threshold = box[2]/config.TRACK_BOX_OUT_OF_FRAME

    if box[0] < -box_length_threshold:
        return False

    if box[0] + box[2] > frame_width + box_length_threshold:
        return False

    return True



