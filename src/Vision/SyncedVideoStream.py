# Author: Gabriel Dinse
# File: SyncedVideoStream
# Date: 11/2/2020
# Made with PyCharm

# Standard Library
import threading
import time
from contextlib import contextmanager

# Third party modules
import cv2

# Local application imports
from Miscellaneous.Errors import (VideoNotOpenedError, VideoNotInitializedError,
                                  FrameReadingError, FrameReadingTimeout)


@contextmanager
def acquire_timeout(frame_lock, timeout):
    result = frame_lock.acquire(timeout=timeout)
    yield result
    if result:
        frame_lock.release()


class VideoOutput:
    def __init__(self, resolution):
        self.stream = None
        self.width, self.height = resolution

    def open(self):
        raise NotImplementedError()

    def close(self):
        self.stream.release()

    def read(self):
        raise NotImplementedError()

    @property
    def fps(self):
        raise NotImplementedError()

    @fps.setter
    def fps(self, fps):
        raise NotImplementedError()

    @property
    def aspect_ratio(self):
        return self.width / self.height

    @property
    def resolution(self):
        return self.width, self.height


class FileVideoOutput(VideoOutput):
    def __init__(self, filepath, repeat, fps, resolution):
        super().__init__(resolution)
        self.filepath = filepath
        self.repeat = repeat
        self.fps = fps
        self.timer = time.time() + 1 / fps
        self.opened = False

    def open(self):
        self.stream = cv2.VideoCapture(self.filepath)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.frame_count = self.stream.get(cv2.CAP_PROP_FRAME_COUNT)

    def read(self):
        self.wait_for_next_frame()
        grabbed, frame = self.stream.read()
        self.reset_timer()
        if not grabbed:
            if self.stream.isOpened() and self.repeat:
                self.current_frame_pos = 0
                grabbed, frame = self.stream.read()
            else:
                raise FrameReadingError(
                    "Error when reading frame from video file stream")
        return frame

    def wait_for_next_frame(self):
        while not self.read_timer_passed():
            time.sleep(0.001)

    def read_timer_passed(self):
        return time.time() - self.timer >= 1 / self.fps

    def reset_timer(self):
        self.timer = time.time()

    @property
    def current_frame_pos(self):
        return self.stream.get(cv2.CAP_PROP_POS_FRAMES)

    @current_frame_pos.setter
    def current_frame_pos(self, value):
        self.stream.set(cv2.CAP_PROP_POS_FRAMES, value)

    @property
    def fps(self):
        return self._fps

    @fps.setter
    def fps(self, fps):
        self._fps = fps


class CameraVideoOutput(VideoOutput):
    def __init__(self, source_id, fps, resolution):
        super().__init__(resolution)
        self.source_id = source_id
        self.fps = fps

    def open(self):
        self.stream = cv2.VideoCapture(self.source_id, cv2.CAP_DSHOW)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def read(self):
        grabbed, frame = self.stream.read()
        if not grabbed:
            raise FrameReadingError(
                "Error when reading frame from raw camera stream")
        return frame

    @property
    def fps(self):
        return self.stream.get(cv2.CV_CAP_PROP_FPS)

    @fps.setter
    def fps(self, fps):
        self.stream.set(cv2.CV_CAP_PROP_FPS, fps)


class SyncedVideoStream:
    def __init__(self):
        self.stream = None
        self.initializd = False
        self.opened = False
        self.frame_lock = threading.Lock()
        self.frames_readers = []

    @classmethod
    def from_camera(cls, source_id, fps=30, resolution=(640, 480)):
        video_stream = cls()
        video_stream.stream = CameraVideoOutput(source_id, fps, resolution)
        video_stream.initialized = True
        return video_stream

    @classmethod
    def from_file(cls, filepath, repeat=True, fps=30, resolution=(640, 480)):
        video_stream = cls()
        video_stream.stream = FileVideoOutput(filepath, repeat, fps, resolution)
        video_stream.initialized = True
        return video_stream

    def open(self):
        if self.initialized:
            if not self.opened:
                self.stream.open()
                self.opened = True
                self.thread = threading.Thread(target=self.run, args=())
                self.thread.start()
        else:
            raise VideoNotInitializedError(
                "Error when trying to open camera. Video should be initialized "
                "first, using constructor methods: "
                "SyncedVideoStream.from_camera() or "
                "SyncedVideoStream.from_file()")

    def close(self):
        if self.opened:
            self.opened = False
            self.stream.close()
            self.thread.join()

    def run(self):
        while self.opened:
            try:
                frame = self.stream.read()
            except FrameReadingError:
                pass
            else:
                with acquire_timeout(self.frame_lock, timeout=1.0) as acquired:
                    if acquired:
                        for frames_reader in self.frames_readers:
                            frames_reader.frame = frame.copy()
                            frames_reader.can_get_frame.set()

    @property
    def width(self):
        return self.stream.width

    @property
    def height(self):
        return self.stream.height

    @property
    def aspect_ratio(self):
        return self.stream.aspect_ratio

    @property
    def resolution(self):
        return self.stream.resolution

    def create_frames_reader(self):
        frames_reader = FramesReader(self)
        self.frames_readers.append(frames_reader)
        return frames_reader


class FramesReader:
    def __init__(self, video_stream: SyncedVideoStream):
        self.video_stream = video_stream
        self.can_get_frame = threading.Event()
        self.running = False
        self.frame = None

    def copy(self):
        return self.video_stream.create_frames_reader()

    def read(self, timeout=1.0):
        if not self.video_stream.opened:
            raise VideoNotOpenedError(
                "Error: Video stream should bem opened first.")
        
        if self.can_get_frame.wait(timeout=timeout):
            with self.video_stream.frame_lock:
                self.can_get_frame.clear()
                return self.frame
        else:
            raise FrameReadingTimeout(
                f"Error: Timeout of {timeout} second"
                f"{'s' if timeout > 1.0 else ''} exceeded when trying to read"
                " frame.")

    @property
    def width(self):
        return self.video_stream.width

    @property
    def height(self):
        return self.video_stream.height

    @property
    def aspect_ratio(self):
        return self.video_stream.aspect_ratio

    @property
    def resolution(self):
        return self.video_stream.resolution
