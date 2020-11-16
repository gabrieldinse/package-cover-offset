# Author: Gabriel Dinse
# File: MainWindow.py
# Date: 11/2/2020
# Made with PyCharm

# Standard Library
import threading
from collections.abc import Iterable
import time

# Third party modules
from PyQt5.QtWidgets import (QGraphicsPixmapItem, QGraphicsScene,
                             QMainWindow, QInputDialog, QLineEdit)
from PyQt5.QtCore import QDir, Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5 import uic
import cv2

# Local application imports
from ApplicationWindows.SegmentationSettings import SegmentationSettings
from ApplicationWindows.TemplatePicking import TemplatePicking
from Helper import WorkerQueue, ProductType, ProductTypeName
from Events import MainWindowEvents
from ApplicationWindows.MainWindowUi import Ui_MainWindow
from Vision.SyncedVideoStream import SyncedVideoStream
from Errors import FrameReadingError



class MainWindow(QMainWindow):
    def __init__(self, frames_reader):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.events = MainWindowEvents()

        self.frames_reader = frames_reader
        self.products_adder = WorkerQueue(self.add_product)
        threading.Thread(target=self.products_adder.run, args=()).start()

        # Visualizacao dos frames no framework do Qt
        self.scene = QGraphicsScene()
        self.ui.graphics_view.setScene(self.scene)
        self.pixmap = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap)

        # Conexao dos signals e slots
        self.ui.start_push_button.clicked.connect(
            self.start_push_button_clicked)
        self.ui.stop_push_button.clicked.connect(
            self.stop_push_button_clicked)
        self.ui.register_product_push_button.clicked.connect(
            self.register_product_push_button_clicked)
        self.ui.edit_product_push_button.clicked.connect(
            self.edit_product_push_button_clicked)
        self.ui.test_push_button.clicked.connect(
            self.test_push_button_clicked)
        self.ui.product_type_combo_box.currentIndexChanged.connect(
            self.product_type_combo_box_index_changed)
        self.ui.turn_on_camera_push_button.clicked.connect(
            self.turn_on_camera_push_button_clicked)
        self.ui.turn_off_camera_push_button.clicked.connect(
            self.turn_off_camera_push_button_clicked)

        self.show_frame_timer = QTimer()
        self.show_frame_timer.timeout.connect(
            self.show_frame)

    def bind(self, **kwargs):
        self.events.bind(**kwargs)

    def finish_vision(self):
        self.products_adder.finish_works()

    def load_product_types_to_list(self, database_product_types):
        pass

    def show_frame(self):
        try:
            frame = self.frames_reader.read()
        except FrameReadingError:
            raise
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, _ = frame.shape
            bytes_per_line = 3 * width

            gui_frame = QImage(frame.data, width, height,
                               bytes_per_line, QImage.Format_RGB888)
            gui_frame = gui_frame.scaled(470, 470, Qt.KeepAspectRatio)
            self.pixmap.setPixmap(QPixmap.fromImage(gui_frame))

    def add_product(self, product_info):
        # Mostra na gui
        pass

    def add_product_types_to_list(self, items):
        self.ui.product_type_combo_box.setDisabled(True)
        if isinstance(items, DatabaseProductType):
            pass
        elif isinstance(items, Iterable):
            pass

    def update_ui_oranges_info(self):
        # Ultima laranja
        formatted_diameter_text = '{:.2f}mm'.format(
            self.data_writer.oranges[-1].diameter)
        self.ui.last_diameter_label.setText(formatted_diameter_text)

        # Media de todas as laranjas
        formatted_diameter_text = '{:.2f}mm'.format(
            self.data_writer.average_diameter)
        self.average_color_label.setText(str(
            self.data_writer.average_color.value))
        self.average_diameter_label.setText(formatted_diameter_text)

        # Numero total de laranjas
        self.number_of_oranges_label.setText(
            str(self.data_writer.quantity))

    def closeEvent(self, event):
        """ Antes de encerrar o programa, salva os arquivos. """

        self.finish_vision()
        self.show_frame_timer.stop()
        self.events.emit("close")
        event.accept()

    def start_push_button_clicked(self):
        self.events.emit("vision_system_start")
        self.ui.state_label.setText('ON')
        self.ui.state_label.setStyleSheet(
            'border-color: rgb(100, 100, 100);'
            'border-width: 2px;'
            'border-style: solid;'
            'color: rgb(0, 255, 0);')

    def stop_push_button_clicked(self):
        self.events.emit("vision_system_stop")
        self.ui.state_label.setText('OFF')
        self.ui.state_label.setStyleSheet(
            'border-color: rgb(100, 100, 100);'
            'border-width: 2px;'
            'border-style: solid;'
            'color: rgb(255, 0, 0);')

    def register_product_push_button_clicked(self):
        product_name, ok = QInputDialog().getText(
            self, "Nome do produto", "Nome do produto",
            QLineEdit.Normal, "")
        if ok and product_name:
            segmentation_dialog = SegmentationSettings(
                product_name, self.frames_reader.copy(), parent=self)
            segmentation_dialog.exec()

            if segmentation_dialog.closed_for_next_step:
                segmentation_info = segmentation_dialog.get_segmentation_info()

                template_dialog = TemplatePicking(
                    product_name, self.frames_reader.copy(), parent=self)
                template_dialog.exec()

                if template_dialog.closed_for_next_step:
                    template = template_dialog.get_template()
                    self.events.emit(
                        "new_product_type", ProductType(product_name, segmentation_info,
                                                        template))

    def product_type_combo_box_index_changed(self):
        pass

    def edit_product_push_button_clicked(self):
        pass

    def test_push_button_clicked(self):
        pass

    def turn_on_camera_push_button_clicked(self):
        self.events.emit("turn_on_camera")
        self.ui.turn_on_camera_push_button.setDisabled(True)
        self.ui.turn_off_camera_push_button.setEnabled(True)
        self.ui.register_product_push_button.setEnabled(True)
        self.show_frame_timer.start(50)

    def turn_off_camera_push_button_clicked(self):
        self.events.emit("turn_off_camera")
        self.ui.turn_off_camera_push_button.setDisabled(True)
        self.ui.turn_on_camera_push_button.setEnabled(True)
        self.ui.register_product_push_button.setDisabled(True)
        self.ui.edit_product_push_button.setDisabled(True)
        self.ui.test_push_button.setDisabled(True)
        self.show_frame_timer.stop()
        white_image = QImage(
            470, 470 / self.frames_reader.aspect_ratio, QImage.Format_RGB888)
        white_image.fill(QColor(Qt.white).rgb())
        self.pixmap.setPixmap(QPixmap.fromImage(white_image))





