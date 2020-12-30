# Author: Gabriel Dinse
# File: ProductInfoExtractor
# Date: 11/1/2020
# Made with PyCharm


# Standard Library
import time
from threading import Thread

# Third party modules
import cv2
import imutils
import numpy as np
from skimage import img_as_ubyte
from skimage.morphology import convex_hull_image

# Local application imports
from Miscellaneous.Events import VideoInfoEvents
from Miscellaneous.Helper import (ProductType, Product,
                                  datetime_now_str)
from Vision.SyncedVideoStream import FramesReader


class VideoInfoExtractor:
    def __init__(self, frames_reader: FramesReader):
        self.events = VideoInfoEvents()

        self.frames_reader = frames_reader
        self.min_package_area = 50000
        self.max_package_area = 68000
        self.max_template_matching = 0.10
        self.scale_factor = 0.573
        self.new_package_delay = 1.0
        self.min_package_centroid_pos = int(self.frames_reader.width * 0.35)
        self.max_package_centroid_pos = int(self.frames_reader.width * 0.65)
        self.template_matching_method = cv2.TM_SQDIFF_NORMED

        self.running = False

    def bind(self, **kwargs) -> None:
        self.events.bind(**kwargs)

    def start(self, product_type: ProductType) -> None:
        if not self.running:
            self.template = product_type.template
            self.gaussian_kernel_size = product_type.segmentation_info.gaussian_filter_size
            self.lower_canny = product_type.segmentation_info.lower_canny
            self.upper_canny = product_type.segmentation_info.upper_canny
            self.current_capture_time = time.time() - self.new_package_delay
            self.running = True
            self.thread = Thread(target=self.run, args=())
            self.thread.start()

    def stop(self) -> None:
        if self.running:
            self.running = False
            self.thread.join()

    def run(self) -> None:
        while self.running:
            try:
                self.frame = self.frames_reader.read()
                self.frame = cv2.imr
            except FrameReadingError:
                pass
            else:
                if self._capture_time_passed():
                    self._produce_convex_package()  # Convex hull
                    self._calculate_package_centroid()
                    if self._is_package_centroid_in_place():
                        self._calculate_cover_centroid()  # Template matching
                        self._calculate_offset()

    def _capture_time_passed(self) -> bool:
        return time.time() - self.current_capture_time >= self.new_package_delay

    def _reset_capture_timer(self) -> None:
        self.current_capture_time = time.time()

    def _produce_convex_package(self) -> None:
        self.gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
        blurred_gray_frame = cv2.GaussianBlur(
            self.gray_frame,
            (self.gaussian_kernel_size, self.gaussian_kernel_size), 0)

        canny_edges = cv2.Canny(
            blurred_gray_frame, self.lower_canny, self.upper_canny)
        self.convex_hull = img_as_ubyte(convex_hull_image(canny_edges))

    def _calculate_package_centroid(self) -> None:
        package_area = (self.convex_hull == 255).sum()
        if self.min_package_area <= package_area <= self.max_package_area:
            _, self.package_centroid = \
                np.argwhere(self.convex_hull == 255).sum(0) / package_area
            self._reset_capture_timer()
        else:
            self.package_centroid = None

    def _is_package_centroid_in_place(self) -> None:
        return (self.package_centroid is not None
                and self.min_package_centroid_pos < self.package_centroid <
                self.max_package_centroid_pos)

    def _calculate_cover_centroid(self) -> None:
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

    def _has_cover(self) -> bool:
        return self.cover_centroid is not None

    def _calculate_offset(self) -> None:
        if self._has_cover():
            offset = int(
                (self.cover_centroid - self.package_centroid)
                * self.scale_factor)
        else:
            offset = 0
        self.events.emit("new_product",
                         Product(datetime_now_str(), offset, self._has_cover()))