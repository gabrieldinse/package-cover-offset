# Author: Gabriel Dinse
# File: Errors.py
# Date: 11/14/2020
# Made with PyCharm

# Standard Library

# Third party modules

# Local application imports


class Error(Exception):
    pass

class VideoError(Error):
    pass

class FrameReadingError(VideoError):
    pass


class SyncedVideoStreamError(VideoError):
    pass

class VideoNotOpenedError(SyncedVideoStreamError):
    pass

class VideoNotInitializedError(SyncedVideoStreamError):
    pass


class FramesReaderError(VideoError):
    pass

class FramesReaderNotStartedError(FramesReaderError):
    pass
