# Author: Gabriel Dinse
# File: MainWindow.py
# Date: 11/2/2020
# Made with PyCharm

# Standard Library
from threading import Thread
from collections.abc import Iterable

# Third party modules
from PyQt5.QtWidgets import (QGraphicsPixmapItem, QGraphicsScene,
                             QMainWindow, QInputDialog, QLineEdit)
from PyQt5.QtCore import QDir
from PyQt5 import uic
import cv2

# Local application imports
from ApplicationWindows.SegmentationSettings import SegmentationSettings
from ApplicationWindows.TemplatePicking import TemplatePicking
from Helper import (WorkerQueue, MainWindowEvents, ProductType,
                    DatabaseProductType)
from ApplicationWindows.MainWindowUi import Ui_MainWindow



class MainWindow(QMainWindow):
    def __init__(self, application):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.events = MainWindowEvents()

        self.frames_shower = WorkerQueue(self.show_frames)
        self.products_adder = WorkerQueue(self.add_product)
        Thread(target=self.frames_shower.run, args=()).start()
        Thread(target=self.products_adder.run, args=()).start()

        # Visualizacao dos frames no framework do Qt
        self.scene = QGraphicsScene()
        self.ui.graphics_view.setScene(self.scene)
        self.pixmap = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap)

        # Coneccao dos signals e slots
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

    def bind(self, **kwargs):
        self.events.bind(**kwargs)

    def finish_vision(self):
        self.frames_shower.finish_works()
        self.products_adder.finish_works()

    def load_product_types(self, database_product_types):
        pass

    def show_frames(self, frame, mask):
        bytes_per_line = 3 * width

        gui_frame = QImage(self.frame.data, width, height,
                           bytes_per_line, QImage.Format_RGB888)
        gui_frame = gui_frame.scaleToWidth(470, Qt.KeepAspectRatio)
        self.pixmap.setPixmap(QPixmap.fromImage(gui_frame))

    def add_product(self, product_info):
        # Mostra na gui
        pass

    def closeEvent(self, event):
        """ Antes de encerrar o programa, salva os arquivos. """

        self.finish_vision()
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
            segmentation_dialog = SegmentationSettings(product_name, parent=self)
            segmentation_dialog.exec()

            if segmentation_dialog.closed_for_next_step:
                segmentation_info = segmentation_dialog.get_segmentation_info()

                template_dialog = TemplatePicking(product_name, parent=self)
                template_dialog.exec()

                if template_dialog.closed_for_next_step:
                    template = template_dialog.get_template()
                    cv2.imshow("test", template)

                    self.events.emit(
                        "new_product_type", ProductType(product_name, segmentation_info,
                                                        template))

    def add_product_types_to_list(self, items):
        if isinstance(items, DatabaseProductType):
            pass
        elif isinstance(items, Iterable):
            pass

    def edit_product_push_button_clicked(self):
        pass

    def test_push_button_clicked(self):
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