"""
Main application of the SoccerAA
"""

from termcolor import colored

from app import template_processor


def run():
    print('processing templates:\n')
    template_processor.process_templates()

    # Process templates



if __name__ == "__main__":
    run()