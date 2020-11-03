# Author: Gabriel Dinse
# File: ProductInfo
# Date: 11/1/2020
# Made with PyCharm

# Standard Library
import datetime
from queue import Queue

# Third party modules
import pydispatch
import numpy as np

# Local application imports


class ProductInfo:
    def __init__(self, offset, has_cover):
        self.datetime_produced = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.offset = offset
        self.has_cover = has_cover


class SegmentationInfo:
    def __init__(self, name, min_h, max_h, min_s, max_s, min_v, max_v,
                 gaussian_filter_size, openning_filter_size):
        self.name = name
        self.min_h = min_h
        self.max_h = max_h
        self.min_s = min_s
        self.max_s = max_s
        self.min_v = min_v
        self.max_v = max_v
        self.gaussian_filter_size = gaussian_filter_size
        self.openning_filter_size = openning_filter_size




class WorkerQueue:
    def __init__(self, callback, max_workers=0):
        self.sentinel = object()
        self.callback = callback
        self.queue = Queue(maxsize=max_workers)

    def put(self, *args, **kwargs):
        self.queue.put((args, kwargs))

    def finish_works(self):
        self.queue.put(self.sentinel)

    def run(self):
        while True:
            try:
                item = self.queue.get()
                if item is self.sentinel:
                    return
                args, kwargs = item
                self.callback(*args, **kwargs)
            finally:
                # Importante para o caso de multithreading para quando der
                # join na fila
                self.queue.task_done()


class VideoInfoEvents(pydispatch.Dispatcher):
    _events_ =  ['new_product', 'new_frame']

class MainWindowEvents(pydispatch.Dispatcher):
    _events_ = ['vision_system_start', 'vision_system_stop']


def circular_kernel(size):
    """ Cria um uma janela circular para aplicacao de convolucao. """

    kernel = np.ones((size, size), dtype=np.uint8)
    center = np.floor(size / 2)
    for i in range(size):
        for j in range(size):
            if np.hypot(i - center, j - center) > center:
                kernel[i, j] = 0
    return kernel