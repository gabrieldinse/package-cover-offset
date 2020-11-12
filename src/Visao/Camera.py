# Author: Gabriel Dinse
# File: Camera
# Date: 11/2/2020
# Made with PyCharm

# Standard Library
import threading

# Third party modules
import cv2

# Local application imports
from Helper import CameraEvents


class Camera:
    def __init__(self, source_id=0, camera_resolution=(640, 480)):
        self.source_id = source_id
        self.width, self.height = camera_resolution
        self.running = False
        self.new_frame_condition = threading.Condition()

    def turn_on(self):
        if not self.running:
            self.stream = cv2.VideoCapture(self.source_id)
            self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.running = True
            self.thread = threading.Thread(target=self._run, args=())
            self.thread.start()
        return self

    def _run(self):
        while self.running:
            grabbed, frame = self.stream.read()
            with self.new_frame_condition:
                self.grabbed, self.frame = grabbed, frame
                self.new_frame_condition.notify_all()

    def turn_off(self):
        if self.running:
            self.running = False
            self.thread.join()
            self.stream.release()

    def create_frames_stream(self):
        return FramesStream(self)


class FramesStream:
    def __init__(self, camera: Camera):
        self.camera = camera
        self.events = CameraEvents()
        self.can_get_frame = threading.Event()
        self.running = False

    def copy(self):
        return self.camera.create_frames_stream()

    def read(self, timeout=1.0):
        if self.running and self.can_get_frame.wait(timeout=timeout):
            with self.camera.new_frame_condition:
                self.can_get_frame.clear()
                return self.grabbed, self.frame

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run, args=())
            self.thread.start()
        return self
    
    def stop(self):
        if self.running:
            self.running = False
            self.thread.join()

    def bind(self, **kwargs):
        self.events.bind(**kwargs)

    def _run(self):
        while self.camera.running and self.running:
            with self.camera.new_frame_condition:
                if self.camera.new_frame_condition.wait(timeout=1.0):
                    if self.camera.grabbed:
                        self.grabbed = self.camera.grabbed
                        self.frame = self.camera.frame.copy()
                        self.can_get_frame.set()
                        self.events.emit("new_frame")