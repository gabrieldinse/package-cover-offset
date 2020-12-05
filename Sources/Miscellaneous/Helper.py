# Author: Gabriel Dinse
# File: Product
# Date: 11/1/2020
# Made with PyCharm

# Standard Library
import datetime
from dataclasses import dataclass

# Third party modules
import numpy as np


# Local application imports

@dataclass
class Product:
    datetime_produced : str
    offset : int
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


class Production:
    def __init__(self):
        self.quantity = 0
        self.no_cover_quantity = 0
        self.total_offset = 0

    def add(self, product: Product):
        self.quantity += 1
        self.total_offset += product.offset
        if not product.has_cover:
            self.no_cover_quantity += 1

    def average_offset(self):
        if self.no_cover_quantity == self.quantity:
            return 0
        else:
            return self.total_offset \
                   / (self.quantity - self.no_cover_quantity)

    def reset(self):
        self.quantity = 0
        self.no_cover_quantity = 0
        self.total_offset = 0


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