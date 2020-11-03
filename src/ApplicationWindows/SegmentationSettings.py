# Author: Gabriel Dinse
# File: SegmentationSettings.py
# Date: 11/2/2020
# Made with PyCharm

# Standard Library
import sys

# Third party modules
from PyQt5.QtWidgets import (QGraphicsPixmapItem, QGraphicsScene,
                             QDialog, QApplication)
from PyQt5 import uic
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
import cv2

# Local application imports
from Visao.Camera import Camera
from Helper import SegmentationInfo, circular_kernel


class SegmentationSettings(QDialog):
    def __init__(self, product_name, parent=None):
        super().__init__(parent)
        uic.loadUi("ApplicationWindows/segmentation_settings_dialog.ui", self)

        self.product_name = product_name
        self.setWindowTitle(product_name)

        self.camera = Camera()

        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        self.pixmap = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap)

        # # Coneccao dos signals e slots
        self.min_h_slider.valueChanged.connect(
            self.min_h_slider_value_changed)
        self.max_h_slider.valueChanged.connect(
            self.max_h_slider_value_changed)
        self.min_s_slider.valueChanged.connect(
            self.min_s_slider_value_changed)
        self.max_s_slider.valueChanged.connect(
            self.max_s_slider_value_changed)
        self.min_v_slider.valueChanged.connect(
            self.min_v_slider_value_changed)
        self.max_v_slider.valueChanged.connect(
            self.max_v_slider_value_changed)

        self.gaussian_kernel_spin_box.valueChanged.connect(
            self.gaussian_kernel_spin_box_value_changed)
        self.opening_kernel_spin_box.valueChanged.connect(
            self.opening_kernel_spin_box_value_changed)

        self.next_push_button.clicked.connect(
            self.next_push_button_clicked)

        self.min_h = 0
        self.max_h = 255
        self.min_s = 0
        self.max_s = 255
        self.min_v = 0
        self.max_v = 255
        self.min_h_slider.setValue(self.min_h)
        self.max_h_slider.setValue(self.max_h)
        self.min_s_slider.setValue(self.min_s)
        self.max_s_slider.setValue(self.max_s)
        self.min_v_slider.setValue(self.min_v)
        self.max_v_slider.setValue(self.max_v)
        self.opening_kernel_size = 5
        self.gaussian_kernel_size = 5
        self.opening_kernel = circular_kernel(self.opening_kernel_size)
        self.opening_kernel_spin_box.setValue(self.opening_kernel_size)
        self.gaussian_kernel_spin_box.setValue(self.gaussian_kernel_size)

        self.frames_processor_timer = QTimer()
        self.frames_processor_timer.timeout.connect(
            self.segment_and_show_frame)
        self.frames_processor_timer.start(0)


    def segment_and_show_frame(self):
        grabbed, frame = self.camera.read()
        if grabbed:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Filtro gaussiano para suavizar ruidos na imagem
            blur = cv2.GaussianBlur(frame, (self.gaussian_kernel_size,
                                                    self.gaussian_kernel_size), 0)
            hsv = cv2.cvtColor(blur, cv2.COLOR_RGB2HSV)

            # Segmentacao de acordo com o invervalo de cores HSV
            in_range_mask = cv2.inRange(
                hsv, (self.min_h, self.min_s, self.min_v),
                (self.max_h, self.max_s, self.max_v))
            segment_mask = cv2.morphologyEx(in_range_mask, cv2.MORPH_OPEN,
                                                 self.opening_kernel)
            processed_frame = cv2.bitwise_and(frame, frame,
                                                   mask=segment_mask)
            height, width, _ = frame.shape
            bytes_per_line = 3 * width
            # Frame segmentado
            gui_frame = QImage(processed_frame.data, width, height,
                               bytes_per_line, QImage.Format_RGB888)
            gui_frame = gui_frame.scaled(470, 470, Qt.KeepAspectRatio)
            self.pixmap.setPixmap(QPixmap.fromImage(gui_frame))

    def get_segmentation_info(self):
        return SegmentationInfo(self.product_name, self.min_h, self.max_h, self.min_s,
                                self.max_s, self.min_v, self.max_v,
                                self.gaussian_kernel_size, self.opening_kernel_size)
    
    def min_h_slider_value_changed(self):
        self.min_h = self.min_h_slider.value()
        self.min_h_label.setText(str(self.min_h))

    def max_h_slider_value_changed(self):
        self.max_h = self.max_h_slider.value()
        self.max_h_label.setText(str(self.max_h))

    def min_s_slider_value_changed(self):
        self.min_s = self.min_s_slider.value()
        self.min_s_label.setText(str(self.min_s))

    def max_s_slider_value_changed(self):
        self.max_s = self.max_s_slider.value()
        self.max_s_label.setText(str(self.max_s))

    def min_v_slider_value_changed(self):
        self.min_v = self.min_v_slider.value()
        self.min_v_label.setText(str(self.min_v))

    def max_v_slider_value_changed(self):
        self.max_v = self.max_v_slider.value()
        self.max_v_label.setText(str(self.max_v))

    def opening_kernel_spin_box_value_changed(self):
        if self.opening_kernel_spin_box.value() % 2 == 0:
            self.opening_kernel_spin_box.setValue(
                self.opening_kernel_spin_box.value() + 1)
        self.opening_kernel_size = self.opening_kernel_spin_box.value()
        self.opening_kernel = circular_kernel(self.opening_kernel_size)

    def gaussian_kernel_spin_box_value_changed(self):
        if self.gaussian_kernel_spin_box.value() % 2 == 0:
            self.gaussian_kernel_spin_box.setValue(
                self.gaussian_kernel_spin_box.value() + 1)
        self.gaussian_kernel_size = self.gaussian_kernel_spin_box.value()

    def next_push_button_clicked(self):
        self.camera.release()
        self.closed_for_next_step = True
        self.close()