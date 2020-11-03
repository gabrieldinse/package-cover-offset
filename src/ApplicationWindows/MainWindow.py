# Author: Gabriel Dinse
# File: MainWindow.py
# Date: 11/2/2020
# Made with PyCharm

# Standard Library

# Third party modules
from PyQt5.QtWidgets import (QGraphicsPixmapItem, QGraphicsScene,
                             QMainWindow, QInputDialog, QLineEdit)
from PyQt5.QtCore import QDir
from PyQt5 import uic
import cv2

# Local application imports
from ApplicationWindows.SegmentationSettings import SegmentationSettings
from ApplicationWindows.TemplatePicking import TemplatePicking


class MainWindow(QMainWindow):
    def __init__(self, application):
        super().__init__()

        uic.loadUi("ApplicationWindows/main_window.ui", self)

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
        self.register_product_push_button.clicked.connect(
            self.register_product_push_button_clicked)
        self.edit_product_push_button.clicked.connect(
            self.edit_product_push_button_clicked)
        self.test_push_button.clicked.connect(
            self.test_push_button_clicked)

    def show_frames(self, frame, mask):
        bytes_per_line = 3 * width

        gui_frame = QImage(self.frame.data, width, height,
                           bytes_per_line, QImage.Format_RGB888)
        gui_frame = gui_frame.scaleToWidth(470, Qt.KeepAspectRatio)
        self.pixmap.setPixmap(QPixmap.fromImage(gui_frame))

    def add_product(self, product_info):
        self.database.add_product(product_info)
        # Faz mais coisas com a informação

    def closeEvent(self, event):
        """ Antes de encerrar o programa, salva os arquivos. """

        self.application.finish_works()
        event.accept()

    def start_push_button_clicked(self):
        self.state_label.setText('ON')
        self.state_label.setStyleSheet(
            'border-color: rgb(100, 100, 100);'
            'border-width: 2px;'
            'border-style: solid;'
            'color: rgb(0, 255, 0);')
        # Thread(target=self.vision_system.run, args=()).start()

    def stop_push_button_clicked(self):
        self.state_label.setText('OFF')
        self.state_label.setStyleSheet(
            'border-color: rgb(100, 100, 100);'
            'border-width: 2px;'
            'border-style: solid;'
            'color: rgb(255, 0, 0);')

    def register_product_push_button_clicked(self):
        product_name, ok = QInputDialog().getText(
            self, "QInputDialog().getText()", "Product name:",
            QLineEdit.Normal, "")
        if ok and product_name:
            segmentation_dialog = SegmentationSettings(product_name, parent=self)
            segmentation_dialog.exec()

            if segmentation_dialog.closed_for_next_step:
                segmentation_info = segmentation_dialog.get_segmentation_info()
                template_dialog = TemplatePicking(product_name, parent=self)
                template_dialog.exec()

                if template_dialog.close_for_next_step:
                    template = template_dialog.get_template()
                    cv2.imshow("test", template)

    def edit_product_push_button_clicked(self):
        pass

    def test_push_button_clicked(self):
        pass

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