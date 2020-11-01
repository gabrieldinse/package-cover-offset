# Author: Gabriel Dinse
# File: Window
# Date: 11/1/2020
# Made with PyCharm

# Standard Library

# Third party modules

# Local application imports


# Standard modules
from math import floor, hypot
import time
import sys
import os
import json

# Third party modules
from PyQt5.QtWidgets import (QGraphicsPixmapItem, QGraphicsScene,
                             QMainWindow, QApplication)
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from numpy import sqrt, pi
import cv2
import numpy as np
import imutils

# Local modules
from main_window import Ui_MainWindow
from CameraStream import CameraStream
from Database import Database
from Helper import ProductInfo, ProducInfoQueue
from Visao.VideoInfoExtractor import VideoInfoExtractor



class Window(QMainWindow):
    """ Classe que representa a janela principal do programa. """

    storage_updated = pyqtSignal()

    def __init__(self, database : Database, vision_system : VideoInfoExtractor):
        # Configuracoes principais da janela/Window
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Sistema de visao funcionando ou nao
        self.identifier_running = False

        self.database = database
        self.vision_system = vision_system

        # Visualizacao dos frames no framework do Qt
        self.main_scene = QGraphicsScene()
        self.ui.main_graphics_view.setScene(self.main_scene)
        self.main_pixmap = QGraphicsPixmapItem()
        self.main_scene.addItem(self.main_pixmap)
        self.segmentation_scene = QGraphicsScene()
        self.ui.segmentation_graphics_view.setScene(self.segmentation_scene)
        self.segmentation_pixmap = QGraphicsPixmapItem()
        self.segmentation_scene.addItem(self.segmentation_pixmap)

        # Coneccao dos signals e slots
        self.ui.min_h_slider.valueChanged.connect(
            self.min_h_slider_value_changed)
        self.ui.max_h_slider.valueChanged.connect(
            self.max_h_slider_value_changed)
        self.ui.min_s_slider.valueChanged.connect(
            self.min_s_slider_value_changed)
        self.ui.max_s_slider.valueChanged.connect(
            self.max_s_slider_value_changed)
        self.ui.min_v_slider.valueChanged.connect(
            self.min_v_slider_value_changed)
        self.ui.max_v_slider.valueChanged.connect(
            self.max_v_slider_value_changed)

        self.ui.gaussian_kernel_spin_box.valueChanged.connect(
            self.gaussian_kernel_spin_box_value_changed)
        self.ui.opening_kernel_spin_box.valueChanged.connect(
            self.opening_kernel_spin_box_value_changed)

        self.ui.min_frame_width_spin_box.valueChanged.connect(
            self.min_frame_width_spin_box_value_changed)
        self.ui.max_frame_width_spin_box.valueChanged.connect(
            self.max_frame_width_spin_box_value_changed)
        self.ui.min_frame_height_spin_box.valueChanged.connect(
            self.min_frame_height_spin_box_value_changed)
        self.ui.max_frame_height_spin_box.valueChanged.connect(
            self.max_frame_height_spin_box_value_changed)

        self.ui.start_conveyor_push_button.clicked.connect(
            self.start_conveyor_push_button_clicked)
        self.ui.stop_conveyor_push_button.clicked.connect(
            self.stop_conveyor_push_button_clicked)
        self.ui.start_identifier_push_button.clicked.connect(
            self.start_identifier_push_button_clicked)
        self.ui.stop_identifier_push_button.clicked.connect(
            self.stop_identifier_push_button_clicked)

        self.ui.capture_line_position_slider.valueChanged.connect(
            self.capture_line_position_slider_value_changed)
        self.ui.capture_box_left_width_spin_box.valueChanged.connect(
            self.capture_box_left_width_spin_box_value_changed)
        self.ui.capture_box_right_width_spin_box.valueChanged.connect(
            self.capture_box_right_width_spin_box_value_changed)

        self.storage_updated.connect(self.update_ui_oranges_info)

        # Configuracoes da gui (importante realizar as coneccoes antes)
        self.load_config()

        # Timer para capturar frames e processa-los
        self.fps_max = 25
        self.frames_processor_timer = QTimer()
        self.frames_processor_timer.timeout.connect(self.show_frames)
        self.frames_processor_timer.start(1000 / self.fps_max)

    def load_config(self):
        """ Carrega as confiurações da gui no formato JSON. """

        with open(self.gui_config_filename) as config_file:
            config = json.load(config_file)

            # Configuracao dos sliders hsv
            hsv_sliders = config['color_range']
            self.min_h = hsv_sliders['min_h']
            self.max_h = hsv_sliders['max_h']
            self.min_s = hsv_sliders['min_s']
            self.max_s = hsv_sliders['max_s']
            self.min_v = hsv_sliders['min_v']
            self.max_v = hsv_sliders['max_v']
            self.ui.min_h_slider.setValue(self.min_h)
            self.ui.max_h_slider.setValue(self.max_h)
            self.ui.min_s_slider.setValue(self.min_s)
            self.ui.max_s_slider.setValue(self.max_s)
            self.ui.min_v_slider.setValue(self.min_v)
            self.ui.max_v_slider.setValue(self.max_v)

            # Configuracao do tamanho do Kernel
            kernel_size = config['kernel_size']
            self.gaussian_kernel_size = kernel_size['gaussian']
            self.opening_kernel_size = kernel_size['opening']
            self.opening_kernel = circular_kernel(self.opening_kernel_size)
            self.ui.opening_kernel_spin_box.setValue(self.opening_kernel_size)
            self.ui.gaussian_kernel_spin_box.setValue(self.gaussian_kernel_size)

            # Configuracao da area de interesse do frame
            frame_dimension_range = config['frame_dimension_range']
            self.min_frame_width = frame_dimension_range['min_width']
            self.max_frame_width = frame_dimension_range['max_width']
            self.min_frame_height = frame_dimension_range['min_height']
            self.max_frame_height = frame_dimension_range['max_height']
            self.ui.min_frame_width_spin_box.setValue(self.min_frame_width)
            self.ui.max_frame_width_spin_box.setValue(self.max_frame_width)
            self.ui.min_frame_height_spin_box.setValue(self.min_frame_height)
            self.ui.max_frame_height_spin_box.setValue(self.max_frame_height)

            # Configuracao da linha de captura
            capture_line = config['capture_line']
            self.capture_line_position = capture_line['position']
            self.capture_box_left_width = capture_line['left_width']
            self.capture_box_left_position = capture_line['position'] \
                                             - capture_line['left_width']
            self.capture_box_right_width = capture_line['right_width']
            self.capture_box_right_position = capture_line['position'] \
                                              - capture_line['right_width']
            self.ui.capture_box_left_width_spin_box.setValue(
                self.capture_box_left_width)
            self.ui.capture_box_right_width_spin_box.setValue(
                self.capture_box_right_width)
            self.ui.capture_line_position_slider.setValue(
                self.capture_line_position)

    # Reinplementacao do metodo closeEvent
    def closeEvent(self, event):
        """ Antes de encerrar o programa, salva os arquivos. """

        self.save_config()
        self.data_writer.stop()
        self.conveyor.stop()
        self.camera.release()
        event.accept()

    # Callbacks
    def product_added(self, product_info):
        pass

    def show_frames(self):
        self.grabbed, self.frame = self.vision_system.get_frame()
        self.mask = self.vision_system.get_mask()
        bytes_per_line = 3 * width

        # Frame segmentado
        gui_frame = QImage(self.processed_frame.data, width, height,
                           bytes_per_line, QImage.Format_RGB888)
        gui_frame = gui_frame.scaled(355, 355, Qt.KeepAspectRatio)
        self.segmentation_pixmap.setPixmap(QPixmap.fromImage(gui_frame))

        # Frame original com realidade aumentada
        gui_frame = QImage(self.frame.data, width, height,
                           bytes_per_line, QImage.Format_RGB888)
        gui_frame = gui_frame.scaled(470, 470, Qt.KeepAspectRatio)
        self.main_pixmap.setPixmap(QPixmap.fromImage(gui_frame))

    def min_h_slider_value_changed(self):
        self.min_h = self.ui.min_h_slider.value()
        self.ui.min_h_label.setText(str(self.min_h))

    def max_h_slider_value_changed(self):
        self.max_h = self.ui.max_h_slider.value()
        self.ui.max_h_label.setText(str(self.max_h))

    def min_s_slider_value_changed(self):
        self.min_s = self.ui.min_s_slider.value()
        self.ui.min_s_label.setText(str(self.min_s))

    def max_s_slider_value_changed(self):
        self.max_s = self.ui.max_s_slider.value()
        self.ui.max_s_label.setText(str(self.max_s))

    def min_v_slider_value_changed(self):
        self.min_v = self.ui.min_v_slider.value()
        self.ui.min_v_label.setText(str(self.min_v))

    def max_v_slider_value_changed(self):
        self.max_v = self.ui.max_v_slider.value()
        self.ui.max_v_label.setText(str(self.max_v))

    def opening_kernel_spin_box_value_changed(self):
        if self.ui.opening_kernel_spin_box.value() % 2 == 0:
            self.ui.opening_kernel_spin_box.setValue(
                self.ui.opening_kernel_spin_box.value() + 1)
        self.opening_kernel_size = self.ui.opening_kernel_spin_box.value()
        self.opening_kernel = circular_kernel(self.opening_kernel_size)

    def gaussian_kernel_spin_box_value_changed(self):
        if self.ui.gaussian_kernel_spin_box.value() % 2 == 0:
            self.ui.gaussian_kernel_spin_box.setValue(
                self.ui.gaussian_kernel_spin_box.value() + 1)
        self.gaussian_kernel_size = self.ui.gaussian_kernel_spin_box.value()

    def min_frame_width_spin_box_value_changed(self):
        if (self.ui.min_frame_width_spin_box.value() >=
                self.ui.max_frame_width_spin_box.value()):
            self.ui.min_frame_width_spin_box.setValue(
                self.ui.min_frame_width_spin_box.minimum())
        self.min_frame_width = self.ui.min_frame_width_spin_box.value()

    def max_frame_width_spin_box_value_changed(self):
        if (self.ui.max_frame_width_spin_box.value() <=
                self.ui.min_frame_width_spin_box.value()):
            self.ui.max_frame_width_spin_box.setValue(
                self.ui.max_frame_width_spin_box.maximum())
        self.max_frame_width = self.ui.max_frame_width_spin_box.value()

    def min_frame_height_spin_box_value_changed(self):
        if (self.ui.min_frame_height_spin_box.value() >=
                self.ui.max_frame_height_spin_box.value()):
            self.ui.min_frame_height_spin_box.setValue(
                self.ui.min_frame_height_spin_box.minimum())
        self.min_frame_height = self.ui.min_frame_height_spin_box.value()

    def max_frame_height_spin_box_value_changed(self):
        if (self.ui.max_frame_height_spin_box.value() <=
                self.ui.min_frame_height_spin_box.value()):
            self.ui.max_frame_height_spin_box.setValue(
                self.ui.max_frame_height_spin_box.maximum())
        self.max_frame_height = self.ui.max_frame_height_spin_box.value()

    def start_conveyor_push_button_clicked(self):
        self.ui.conveyor_state_label.setText('ON')
        self.ui.conveyor_state_label.setStyleSheet(
            'border-color: rgb(147, 103, 53);'
            'border-width: 2px;'
            'border-style: solid;'
            'color: rgb(0, 255, 0);')
        self.conveyor.start()

    def stop_conveyor_push_button_clicked(self):
        self.ui.conveyor_state_label.setText('OFF')
        self.ui.conveyor_state_label.setStyleSheet(
            'border-color: rgb(147, 103, 53);'
            'border-width: 2px;'
            'border-style: solid;'
            'color: rgb(255, 0, 0);')
        self.conveyor.stop()

    def start_identifier_push_button_clicked(self):
        self.ui.identifier_state_label.setText('ON')
        self.ui.identifier_state_label.setStyleSheet(
            'border-color: rgb(147, 103, 53);'
            'border-width: 2px;'
            'border-style: solid;'
            'color: rgb(0, 255, 0);')
        self.capture_timer = time.time() - self.capture_timer_delay
        self.identifier_running = True

    def stop_identifier_push_button_clicked(self):
        self.ui.identifier_state_label.setText('OFF')
        self.ui.identifier_state_label.setStyleSheet(
            'border-color: rgb(147, 103, 53);'
            'border-width: 2px;'
            'border-style: solid;'
            'color: rgb(255, 0, 0);')
        self.data_writer.stop()
        self.identifier_running = False

    def capture_line_position_slider_value_changed(self):
        self.capture_line_position = \
            self.ui.capture_line_position_slider.value()
        if self.capture_line_position - self.capture_box_left_width < 0:
            self.ui.capture_box_left_width_spin_box.setValue(
                self.capture_line_position)
        else:
            self.capture_box_left_position = self.capture_line_position \
                                             - self.capture_box_left_width

        if (self.capture_line_position + self.capture_box_right_width >
                self.camera_resolution[0] - 1):
            self.capture_box_right_width_spin_box.setValue(
                self.camera_resolution[0] - 1 - self.capture_line_position)
        else:
            self.capture_box_right_position = self.capture_line_position \
                                              + self.capture_box_right_width

    def capture_box_left_width_spin_box_value_changed(self):
        if (self.capture_line_position -
                self.ui.capture_box_left_width_spin_box.value() < 0):
            self.capture_box_left_width = self.capture_line_position
        else:
            self.capture_box_left_width = \
                self.ui.capture_box_left_width_spin_box.value()
        self.capture_box_left_position = self.capture_line_position \
                                         - self.capture_box_left_width

    def capture_box_right_width_spin_box_value_changed(self):
        if (self.capture_line_position +
                self.ui.capture_box_right_width_spin_box.value() >
                self.camera_resolution[0] - 1):
            self.capture_box_right_width = self.camera_resolution[0] - 1
        else:
            self.capture_box_right_width = \
                self.ui.capture_box_right_width_spin_box.value()
        self.capture_box_right_position = self.capture_line_position \
                                          + self.capture_box_right_width

    def update_ui_oranges_info(self):
        # Ultima laranja
        formatted_diameter_text = '{:.2f}mm'.format(
            self.data_writer.oranges[-1].diameter)
        self.ui.last_diameter_label.setText(formatted_diameter_text)
        self.ui.last_color_label.setText(str(
            self.data_writer.oranges[-1].color.value))
        color = self.data_writer.oranges[-1].rgb
        frame_color = QColor(int(color[0]), int(color[1]), int(color[2]))
        self.ui.last_color_frame.setStyleSheet(
            'border-color: rgb(147, 103, 53);'
            'border-width : 2px;'
            'border-style:solid;'
            'background-color: {};'.format(frame_color.name()))

        # Media de todas as laranjas
        formatted_diameter_text = '{:.2f}mm'.format(
            self.data_writer.average_diameter)
        self.ui.average_color_label.setText(str(
            self.data_writer.average_color.value))
        self.ui.average_diameter_label.setText(formatted_diameter_text)
        color = self.data_writer.average_rgb
        frame_color = QColor(int(color[0]), int(color[1]), int(color[2]))
        self.ui.average_color_frame.setStyleSheet(
            'border-color: rgb(147, 103, 53);'
            'border-width : 2px;'
            'border-style:solid;'
            'background-color: {};'.format(frame_color.name()))

        # Numero total de laranjas
        self.ui.number_of_oranges_label.setText(
            str(self.data_writer.quantity))

