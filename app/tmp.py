import sys
import time

def countdown(n):
    for x in reversed(range(n)):

        time.sleep(1)

countdown(60)