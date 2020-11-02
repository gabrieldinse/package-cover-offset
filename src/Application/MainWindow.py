# Author: Gabriel Dinse
# File: MainWindow.py
# Date: 11/2/2020
# Made with PyCharm

# Standard Library
import sys
from threading import Thread

# Third party modules
from PyQt5.QtWidgets import (QGraphicsPixmapItem, QGraphicsScene,
                             QMainWindow, QApplication)
from PyQt5 import uic

# Local application imports
from Database.Database import Database
from Visao.VideoInfoExtractor import VideoInfoExtractor
from Helper import WorkerQueue


class MainWindow(QMainWindow):
    def __init__(self, application):
        super().__init__()
        uic.loadUi("main_window.ui", self)

        self.application = application

        # Visualizacao dos frames no framework do Qt
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        self.pixmap = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap)

        # Coneccao dos signals e slots
        self.start_push_button.clicked.connect(
            self.start_push_button_clicked)
        self.stop_push_button.clicked.connect(
            self.stop_push_button_clicked)

    def show_frames(self, frame, mask):
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
        self.pixmap.setPixmap(QPixmap.fromImage(gui_frame))

    def add_product(self, product_info):
        self.database.add_product(product)
        # Faz mais coisas como a informação

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
            self.min_h_slider.setValue(self.min_h)
            self.max_h_slider.setValue(self.max_h)
            self.min_s_slider.setValue(self.min_s)
            self.max_s_slider.setValue(self.max_s)
            self.min_v_slider.setValue(self.min_v)
            self.max_v_slider.setValue(self.max_v)

            # Configuracao do tamanho do Kernel
            kernel_size = config['kernel_size']
            self.gaussian_kernel_size = kernel_size['gaussian']
            self.opening_kernel_size = kernel_size['opening']
            self.opening_kernel = circular_kernel(self.opening_kernel_size)
            self.opening_kernel_spin_box.setValue(self.opening_kernel_size)
            self.gaussian_kernel_spin_box.setValue(self.gaussian_kernel_size)

            # Configuracao da area de interesse do frame
            frame_dimension_range = config['frame_dimension_range']
            self.min_frame_width = frame_dimension_range['min_width']
            self.max_frame_width = frame_dimension_range['max_width']
            self.min_frame_height = frame_dimension_range['min_height']
            self.max_frame_height = frame_dimension_range['max_height']
            self.min_frame_width_spin_box.setValue(self.min_frame_width)
            self.max_frame_width_spin_box.setValue(self.max_frame_width)
            self.min_frame_height_spin_box.setValue(self.min_frame_height)
            self.max_frame_height_spin_box.setValue(self.max_frame_height)

            # Configuracao da linha de captura
            capture_line = config['capture_line']
            self.capture_line_position = capture_line['position']
            self.capture_box_left_width = capture_line['left_width']
            self.capture_box_left_position = capture_line['position'] \
                                             - capture_line['left_width']
            self.capture_box_right_width = capture_line['right_width']
            self.capture_box_right_position = capture_line['position'] \
                                              - capture_line['right_width']
            self.capture_box_left_width_spin_box.setValue(
                self.capture_box_left_width)
            self.capture_box_right_width_spin_box.setValue(
                self.capture_box_right_width)
            self.capture_line_position_slider.setValue(
                self.capture_line_position)

        # Reinplementacao do metodo closeEvent

    def closeEvent(self, event):
        """ Antes de encerrar o programa, salva os arquivos. """

        self.save_config()
        self.data_writer.stop()
        self.conveyor.stop()
        self.camera.release()
        event.accept()

    def start_push_button_clicked(self):
        self.identifier_state_label.setText('ON')
        self.identifier_state_label.setStyleSheet(
            'border-color: rgb(147, 103, 53);'
            'border-width: 2px;'
            'border-style: solid;'
            'color: rgb(0, 255, 0);')
        self.capture_timer = time.time() - self.capture_timer_delay
        self.identifier_running = True

    def stop_push_button_clicked(self):
        self.identifier_state_label.setText('OFF')
        self.identifier_state_label.setStyleSheet(
            'border-color: rgb(147, 103, 53);'
            'border-width: 2px;'
            'border-style: solid;'
            'color: rgb(255, 0, 0);')
        self.data_writer.stop()
        self.identifier_running = False

    def update_ui_oranges_info(self):
        # Ultima laranja
        formatted_diameter_text = '{:.2f}mm'.format(
            self.data_writer.oranges[-1].diameter)
        self.last_diameter_label.setText(formatted_diameter_text)
        self.last_color_label.setText(str(
            self.data_writer.oranges[-1].color.value))
        color = self.data_writer.oranges[-1].rgb
        frame_color = QColor(int(color[0]), int(color[1]), int(color[2]))
        self.last_color_frame.setStyleSheet(
            'border-color: rgb(147, 103, 53);'
            'border-width : 2px;'
            'border-style:solid;'
            'background-color: {};'.format(frame_color.name()))

        # Media de todas as laranjas
        formatted_diameter_text = '{:.2f}mm'.format(
            self.data_writer.average_diameter)
        self.average_color_label.setText(str(
            self.data_writer.average_color.value))
        self.average_diameter_label.setText(formatted_diameter_text)
        color = self.data_writer.average_rgb
        frame_color = QColor(int(color[0]), int(color[1]), int(color[2]))
        self.average_color_frame.setStyleSheet(
            'border-color: rgb(147, 103, 53);'
            'border-width : 2px;'
            'border-style:solid;'
            'background-color: {};'.format(frame_color.name()))

        # Numero total de laranjas
        self.number_of_oranges_label.setText(
            str(self.data_writer.quantity))