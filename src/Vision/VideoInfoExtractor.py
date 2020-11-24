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
from Miscellaneous.Helper import (ProductType, SegmentationInfo, Product,
                                  datetime_now_str)
from Miscellaneous.Events import VideoInfoEvents


class VideoInfoExtractor:
    def __init__(self, frames_reader):
        self.events = VideoInfoEvents()
        self.frames_reader = frames_reader
        self.min_package_area = 200
        self.max_package_area = 5000000
        self.max_template_value = 0.25
        self.scale_factor = 1
        self.threshold_position = 0
        self.template_matching_method = cv2.TM_SQDIFF_NORMED

        # TEMPORARIO SUPER
        self.frame = cv2.imread("../Images/pc1.jpg", 1)
        height, width, _ = self.frame.shape
        scale_x = 480 / width
        scale_y = 640 / height
        self.frame = imutils.resize(self.frame, width=int(self.frame.shape[1] * scale_x),
                                    height=int(self.frame.shape[0] * scale_y))
        self.template = cv2.imread("../Images/template.jpg", 0)
        self.template = imutils.resize(self.template, width=int(self.template.shape[1] * scale_x),
                                    height=int(self.template.shape[0] * scale_y))
        self.gaussian_kernel_size = 5
        self.lower_canny = 100
        self.upper_canny = 200

        self.running = False

    def bind(self, **kwargs):
        self.events.bind(**kwargs)

    def load_product_type(self, product_type : ProductType):
        pass

    # def verify_frame(self):
    #     if self.identifier_running:
    #         if (time.time() - self.capture_timer) >= self.capture_timer_delay:
    #             for diameter, centroid in zip(self.diameters, self.centroids):
    #                 if (self.capture_line_position <= centroid[0]
    #                         <= self.capture_box_right_position):
    #                     self.create_capture_mask()
    #
    #                     # cv2.mean retorna np.ndarray([R, G, B, alpha]), onde
    #                     # alpha eh a transparencia, nao utilizada neste caso
    #                     rgb_mean = np.array(cv2.mean(
    #                         self.processed_frame, mask=self.capture_mask)[0:3],
    #                                         dtype=np.uint8)
    #                     self.data_writer.add(
    #                         diameter * self.diameter_prop, rgb_mean)
    #                     self.capture_timer = time.time()
    #                     return

    def start(self, segmentation_info: SegmentationInfo):
        if not self.running:
            self.segmentation_info = segmentation_info
            self.running = True
            self.thread = Thread(target=self.run, args=())
            self.thread.start()

    def stop(self):
        if self.running:
            self.running = False
            self.thread.join()

    def run(self):
        while self.running:
            # try:
            #     self.frame = self.frames_reader.read()
            # except FrameReadingError:
            #     pass
            # else:
            #     self.get_convex_package()  # Convex hull
            #     self.calculate_package_centroid()
            #     self.calculate_cover_centroid()  # Template matching
            #     self.calculate_offset()

            # start = time.time()
            self.get_convex_package()  # Convex hull
            self.calculate_package_centroid()
            self.calculate_cover_centroid()  # Template matching
            self.calculate_offset()
            # print(time.time() - start)

    def get_convex_package(self):
        self.gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
        blurred_gray_frame = cv2.GaussianBlur(
            self.gray_frame,
            (self.gaussian_kernel_size, self.gaussian_kernel_size), 0)

        canny_edges = cv2.Canny(
            blurred_gray_frame, self.lower_canny, self.upper_canny)
        self.convex_hull = img_as_ubyte(convex_hull_image(canny_edges))
        contours, _ = cv2.findContours(self.convex_hull, cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            contour = contours[0]
            self.x, self.y, self.w, self.h = cv2.boundingRect(contour)
        # cv2.imshow("test", convex_hull)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     return
        # self.convex_hull = self.convex_hull[self.y:self.y+self.h,self.x:self.x+self.w]
        # cv2.imshow("test kkk", gray_frame[self.y:self.y+self.h,self.x:self.x+self.w])
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     return

    def calculate_package_centroid(self):
        package_area = (self.convex_hull == 255).sum()
        if self.min_package_area <= package_area <= self.max_package_area:
            self.package_centroid, _ = \
                np.argwhere(self.convex_hull == 255).sum(0) / package_area
        else:
            self.package_centroid = None

    def package_centroid_is_valid(self):
        return (self.package_centroid is not None
                and self.package_centroid >= self.threshold_position)

    def calculate_cover_centroid(self):
        if self.package_centroid_is_valid():
            found = None
            for scale in np.linspace(0.9, 1.1, 5):
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
                        self.gray_frame[self.y:self.y+self.h,self.x:self.x+self.w],
                        resized_template, self.template_matching_method)
                    min_value, _, min_location, _ = cv2.minMaxLoc(similarity)

                    if found is None or min_value < found[0]:
                        found = (min_value, min_location, scale)

            if found[0] < self.max_template_value:
                h, w = self.template.shape
                self.cover_centroid = found[1][1] + found[2] * h / 2  # TEMP
                return

        self.cover_centroid = None

    def has_cover(self):
        return self.cover_centroid is not None

    def can_calculate_offset(self):
        return (self.package_centroid_is_valid() and
                self.has_cover())

    def calculate_offset(self):
        if self.can_calculate_offset():
            offset = (self.cover_centroid - self.package_centroid) \
                         * self.scale_factor
        else:
            offset = 0.0
        print(offset)
        self.events.emit("new_product",
                         Product(datetime_now_str(), offset, self.has_cover()))