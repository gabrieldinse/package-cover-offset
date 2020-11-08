# Author: Gabriel Dinse
# File: ProductInfo
# Date: 11/1/2020
# Made with PyCharm

# Standard Library
import datetime
from queue import Queue
from dataclasses import dataclass

# Third party modules
import pydispatch
import numpy as np

# Local application imports

@dataclass
class ProductInfo:
    datetime_produced : str
    offset : float
    has_cover : bool


@dataclass
class SegmentationInfo:
    min_h : int
    max_h : int
    min_s : int
    max_s : int
    min_v : int
    max_v : int
    gaussian_filter_size : int
    openning_filter_size : int


@dataclass
class ProductType:
    name : str
    segmentation_info : SegmentationInfo
    template : np.ndarray


@dataclass
class DatabaseProductType:
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


class VideoInfoEvents(pydispatch.Dispatcher):
    _events_ =  ['new_product', 'new_frame']

class MainWindowEvents(pydispatch.Dispatcher):
    _events_ = ['vision_system_start', 'vision_system_stop', 'new_product_type',
                'product_type_edited']


def datetime_now():
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