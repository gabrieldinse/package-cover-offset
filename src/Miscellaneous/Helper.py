# Author: Gabriel Dinse
# File: ProductInfo
# Date: 11/1/2020
# Made with PyCharm

# Standard Library
import datetime
from queue import Queue
from dataclasses import dataclass

# Third party modules
import numpy as np

# Local application imports

@dataclass
class ProductInfo:
    datetime_produced : str
    offset : float
    has_cover : bool


@dataclass
class SegmentationInfo:
    lower_canny : int
    upper_canny : int
    gaussian_filter_size : int


@dataclass
class ProductType:
    name : str
    segmentation_info : SegmentationInfo
    template : np.ndarray


@dataclass
class ProductTypeName:
    id : int
    name : str


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
                self.queue.task_done()  # Para o caso de multithreading


def datetime_now_str():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def circular_kernel(size):
    """ Cria um uma janela circular para aplicacao de convolucao. """

    kernel = np.ones((size, size), dtype=np.uint8)
    center = np.floor(size / 2)
    for i in range(size):
        for j in range(size):
            if np.hypot(i - center, j - center) > center:
                kernel[i, j] = 0
    return kernel