import os
import sys


def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)


add_path(os.path.join(os.getcwd(), '..'))
