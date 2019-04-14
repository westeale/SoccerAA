"""
Helper Functions for Tracking
"""
import numpy as np

def calc_rectangle(polygon):
    """
    Calculates an Rectangle over tho polygon
    :param polygon: points of the polygon
    :return: Rectangle
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




def fill_rectangle(rectangle, frame_height):
    """
    Creating a rectangle over the frame, to fill the whole height
    :param rectangle: points of a rectangle
    :param frame_height: height of the frame
    :return: bar over the whole frame
    """
    bar = np.zeros((4, 1, 2), np.int32)
    bar[0][0][1] = 0
    bar[0][0][0] = rectangle[0]
    bar[1][0][0] = rectangle[0]
    bar[2][0][0] = rectangle[2] + rectangle[0]
    bar[3][0][0] = rectangle[2] + rectangle[0]
    bar[1][0][1] = frame_height
    bar[2][0][1] = frame_height
    bar[3][0][1] = 0

    return bar
