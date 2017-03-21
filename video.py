from time import time, sleep
from glob import glob


class Video(object):
    """An emulated camera implementation that streams a repeated sequence of
    files at a rate of fps frames per second."""

    def __init__(self, dir_name, fps):
        self.dir_name = dir_name
        self.frames = [open(f, 'rb').read() for f in sorted(glob('{}/*.png'.format(self.dir_name)))]
        self.fps = fps
        self.next_frame = 0

    def get_frame(self):
        frame = self.frames[self.next_frame]
        self.next_frame += 1
        sleep(1.0 / self.fps)
        return frame
