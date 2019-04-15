"""
Helper Functions for core.py
"""
from app import config


def search_logos(tracked, last_tracked):
    if not config.LAZY_SEARCH:
        return True

    if tracked == 0:
        return True

    if tracked == last_tracked:
        return False

    return True