"""
Helper Functions for Result generator
"""
import numpy as np


def scale_logos(logos, compression):
    n_logos = len(logos)
    logos_scaled = np.zeros((n_logos, 4, 1, 2), np.int32)
    for i in range(n_logos):
        logos_scaled[i] = logos[i] / compression

    return logos_scaled

