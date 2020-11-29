# Author: Gabriel Dinse
# File: ProductInfoExtractor
# Date: 11/1/2020
# Made with PyCharm

# Standard Library
from threading import Thread
import time

# Third party modules
from skimage.morphology import convex_hull_image
import imutils
import numpy as np
import cv2

from skimage import img_as_ubyte

# Local application imports
from Vision.SyncedVideoStream import FramesReader
from Miscellaneous.Helper import (ProductType, SegmentationInfo, Product,
                                  datetime_now_str)
from Miscellaneous.Events import VideoInfoEvents


class VideoInfoExtractor:
    def __init__(self, frames_reader: FramesReader):
        self.events = VideoInfoEvents()

        self.frames_reader = frames_reader
        self.min_package_area = 50000
        self.max_package_area = 62000
        self.max_template_matching = 0.10
        self.scale_factor = 0.573
        self.new_package_delay = 1.0
        self.min_package_centroid_pos = int(self.frames_reader.width * 0.30)
        self.max_package_centroid_pos = int(self.frames_reader.width * 0.65)
        self.template_matching_method = cv2.TM_SQDIFF_NORMED

        self.running = False

    def bind(self, **kwargs):
        self.events.bind(**kwargs)

    def start(self, product_type : ProductType):
        if not self.running:
            self.template = product_type.template
            self.gaussian_kernel_size = product_type.segmentation_info.gaussian_filter_size
            self.lower_canny = product_type.segmentation_info.lower_canny
            self.upper_canny = product_type.segmentation_info.upper_canny
            self.current_capture_time = time.time() - self.new_package_delay
            self.running = True
            self.thread = Thread(target=self.run, args=())
            self.thread.start()

    def stop(self):
        if self.running:
            self.running = False
            self.thread.join()

    def run(self):
        while self.running:
            try:
                self.frame = self.frames_reader.read()
            except FrameReadingError:
                pass
            else:
                if self.capture_time_passed():
                    self.get_convex_package()  # Convex hull
                    self.calculate_package_centroid()
                    if self.is_package_centroid_in_place():
                        self.calculate_cover_centroid()  # Template matching
                        self.calculate_offset()

    def capture_time_passed(self):
        return time.time() - self.current_capture_time >= self.new_package_delay

    def reset_capture_timer(self):
        self.current_capture_time = time.time()

    def get_convex_package(self):
        self.gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
        blurred_gray_frame = cv2.GaussianBlur(
            self.gray_frame,
            (self.gaussian_kernel_size, self.gaussian_kernel_size), 0)

        canny_edges = cv2.Canny(
            blurred_gray_frame, self.lower_canny, self.upper_canny)
        self.convex_hull = img_as_ubyte(convex_hull_image(canny_edges))

    def calculate_package_centroid(self):
        package_area = (self.convex_hull == 255).sum()
        if self.min_package_area <= package_area <= self.max_package_area:
            _, self.package_centroid = \
                np.argwhere(self.convex_hull == 255).sum(0) / package_area
            self.reset_capture_timer()
        else:
            self.package_centroid = None

    def is_package_centroid_in_place(self):
        return (self.package_centroid is not None
                and self.min_package_centroid_pos < self.package_centroid
                and self.max_package_centroid_pos > self.package_centroid)

    def calculate_cover_centroid(self):
        best_match = None
        for scale in np.linspace(0.8, 1.2, 9):
            for orientation in ["0", "180"]:
                resized_template = imutils.resize(
                    self.template, width=int(self.template.shape[1] * scale))
                h, w = resized_template.shape
                if orientation == "180":
                    center = (w / 2, h / 2)
                    rotation = cv2.getRotationMatrix2D(center, 180, 1.0)
                    resized_template = cv2.warpAffine(
                        resized_template, rotation, (h, w))

                similarity = cv2.matchTemplate(
                    self.gray_frame, resized_template,
                    self.template_matching_method)
                min_value, _, min_location, _ = cv2.minMaxLoc(similarity)

                if best_match is None or min_value < best_match[0]:
                    best_match = (min_value, min_location, scale)

        if best_match[0] < self.max_template_matching:
            h, w = self.template.shape
            self.cover_centroid = best_match[1][0] + best_match[2] * w / 2
        else:
            self.cover_centroid = None

    def has_cover(self):
        return self.cover_centroid is not None

    def calculate_offset(self):
        if self.has_cover():
            offset = (self.cover_centroid - self.package_centroid) \
                         * self.scale_factor
        else:
            offset = 0.0
        self.events.emit("new_product",
                         Product(datetime_now_str(), offset, self.has_cover()))