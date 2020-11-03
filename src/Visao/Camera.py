# Author: Gabriel Dinse
# File: Camera
# Date: 11/2/2020
# Made with PyCharm

# Standard Library

# Third party modules
import cv2

# Local application imports


class Camera:
    def __init__(self, video_source=0, camera_resolution=(640, 480)):
        self.stream = cv2.VideoCapture(video_source)
        self.width, self.height = camera_resolution
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def read(self):
        return self.stream.read()

    def release(self):
        self.stream.release()
