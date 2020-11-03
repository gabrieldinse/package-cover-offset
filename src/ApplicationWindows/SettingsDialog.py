# Author: Gabriel Dinse
# File: SettingsDialog.py
# Date: 11/2/2020
# Made with PyCharm

# Standard Library
import sys

# Third party modules
from PyQt5.QtWidgets import (QGraphicsPixmapItem, QGraphicsScene,
                             QDialog, QApplication)
from PyQt5 import uic

# Local application imports
from ApplicationWindows.TemplateDialog import TemplateDialog


class SettingsDialog(QDialog):
    def __init__(self, product_name, parent=None):
        super().__init__(parent)
        uic.loadUi("ApplicationWindows/settings_dialog.ui", self)

        self.window_name = product_name
        self.setWindowTitle(product_name)

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
        template_dialog = TemplateDialog(self.window_name, self)
        template_dialog.exec()
