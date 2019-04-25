"""
Helper functions for feature detection
"""
import numpy as np
import cv2 as cv



def calc_rectangle(kp1, kp2, matches, template_height, template_width, shift):
    """
    Calculates the rectangle for the target based on the template
        :param kp1: Template Keypoints
        :param kp2: Target Keypoints
        :param matches: Reference matches
        :param template_height: height of tenplate
        :param template_width: width of tenplate
        :param shift: vertical shift of template
        :return: points for rectangle in target
    """
    destination_points = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    source_points = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    M, mask = cv.findHomography(source_points, destination_points, cv.RANSAC, 5.0)
    if shift > 0:
        pts = np.float32([[0, 0], [0, template_height - 1 - shift], [template_width - 1, template_height - 1],
                          [template_width - 1, shift]]).reshape(-1, 1, 2)
    else:
        pts = np.float32([[0, shift], [0, template_height - 1], [template_width - 1, template_height - 1 - shift],
                          [template_width - 1, 0]]).reshape(-1, 1, 2)


    dst = cv.perspectiveTransform(pts, M)

    return dst


def check_box(dst, ratio_check):
    """
    Tests ratio, position and size of the found matching box
        :param dst: points for rectangle in target
        :return: True if ratio, position and size is valid
    """

    position1 = dst[0][0][0] < dst[3][0][0]

    position2 = dst[0][0][1] < dst[1][0][1]

    position3 = dst[1][0][0] < dst[2][0][0]

    position4 = dst[3][0][1] < dst[2][0][1]

    positions = position1 and position2 and position3 and position4

    if not positions:
        return False

    r1 = (dst[3][0][0] - dst[0][0][0]) / (dst[1][0][0] - dst[2][0][0])
    r2 = (dst[1][0][1] - dst[0][0][1]) / (dst[2][0][1] - dst[3][0][1])
    ratio = abs(r1) < 1.3 and abs(r1) > 0.7 and abs(r2) < 1.3 and abs(r2) > 0.7
    r3 = abs((dst[1][0][0] - dst[2][0][0]) / (dst[1][0][1] - dst[0][0][1]))
    test_ratio = 0.3 < abs(ratio_check / r3) < 3



    # crossed points check:
    return ratio and test_ratio


def create_bars(dst, frame_height):
    """
    Sets points to fill out maximum bars
        :param dst: points for rectangle in target
        :param frame_height: height of frame
        :return: points vor filled bar
    """
    dst[0][0][1] = 0
    dst[0][0][0] = min(dst[0][0][0], dst[1][0][0])
    dst[1][0][0] = dst[0][0][0]
    dst[2][0][0] = max(dst[2][0][0], dst[3][0][0])
    dst[3][0][0] = dst[2][0][0]
    dst[1][0][1] = frame_height
    dst[2][0][1] = frame_height
    dst[3][0][1] = 0

    return dst
