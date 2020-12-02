# Author: Gabriel Dinse
# File: Errors.py
# Date: 11/14/2020
# Made with PyCharm

# Standard Library

# Third party modules

# Local application imports


class Error(Exception):
    pass


class FileError(Error):
    pass

class FileReadingError(FileError):
    pass

class TemplateReadingError(FileReadingError):
    pass

class FileWritingError(FileError):
    pass

class TemplateWritingError(FileWritingError):
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

class FrameReadingTimeout(FramesReaderError):
    pass

class FramesReaderNotStartedError(FramesReaderError):
    pass


class DataStoragerError(Error):
    pass

class NotLoggedInToFTPServerError(DataStoragerError):
    pass

class DatabaseNotOpenedError(DataStoragerError):
    pass

class ProductionNotStartedError(DataStoragerError):
    pass