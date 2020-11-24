# Author: Gabriel Dinse
# File: MainWindow.py
# Date: 11/2/2020
# Made with PyCharm

# Standard Library
import threading
from typing import Sequence

# Third party modules
from PyQt5.QtWidgets import (QGraphicsPixmapItem, QGraphicsScene,
                             QMainWindow, QApplication, QInputDialog, QLineEdit)
from PyQt5.QtCore import Qt, QTimer, QCoreApplication
from PyQt5.QtGui import QImage, QPixmap, QColor
import cv2

# Local application imports
from Windows.SegmentationSettings import SegmentationSettings
from Windows.TemplatePicking import TemplatePicking
from Windows.UI.MainWindowUi import Ui_MainWindow

from Data.DataStorager import DataStorager

from Vision.SyncedVideoStream import SyncedVideoStream
from Vision.VideoInfoExtractor import VideoInfoExtractor

from Miscellaneous.Helper import ProductType, ProductTypeName, Product, Production
from Miscellaneous.Errors import FrameReadingError, TemplateReadingError


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.camera = SyncedVideoStream.from_camera(3)
        self.data_storager = DataStorager()
        self.data_storager.open_database()
        self.vision_system = VideoInfoExtractor(
            self.camera.create_frames_reader())
        self.production = Production()

        # Conexao dos signals e slots
        self.ui.start_vision_push_button.clicked.connect(
            self.start_vision_push_button_clicked)
        self.ui.stop_vision_push_button.clicked.connect(
            self.stop_vision_push_button_clicked)
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

        self.vision_system.bind(new_product=self.add_product)
        self.running = False
        self.frames_reader = self.camera.create_frames_reader()

        # Visualizacao dos frames no framework do Qt
        self.scene = QGraphicsScene()
        self.ui.graphics_view.setScene(self.scene)
        self.pixmap = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap)

        # Configurações iniciais
        self.set_product_types_list(
            self.data_storager.get_product_types_names())

        self.show_frame_timer = QTimer()
        self.show_frame_timer.timeout.connect(
            self.show_frame)

    def stop(self):
        self.vision_system.stop()
        self.show_frame_timer.stop()
        self.camera.close()
        self.data_storager.close_database()

    def start_vision_system(self):
        segmentation_info = self.data_storager.get_product_type(
            self.current_product_type_id).segmentation_info
        self.vision_system.start(segmentation_info)

        self.ui.start_vision_push_button.setDisabled(True)
        self.ui.stop_vision_push_button.setEnabled(True)
        self.ui.vision_state_label.setText('ON')
        self.ui.vision_state_label.setStyleSheet(
            'border-color: rgb(100, 100, 100);'
            'border-width: 2px;'
            'border-style: solid;'
            'color: rgb(0, 255, 0);')

    def stop_vision_system(self):
        self.ui.start_vision_push_button.setEnabled(True)
        self.ui.stop_vision_push_button.setDisabled(True)
        self.ui.vision_state_label.setText('OFF')
        self.ui.vision_state_label.setStyleSheet(
            'border-color: rgb(100, 100, 100);'
            'border-width: 2px;'
            'border-style: solid;'
            'color: rgb(255, 0, 0);')
        self.vision_system.stop()

    def turn_on_camera(self):
        self.camera.open()
        self.ui.turn_on_camera_push_button.setDisabled(True)
        self.ui.turn_off_camera_push_button.setEnabled(True)
        self.ui.register_product_push_button.setEnabled(True)
        self.show_frame_timer.start(50)
        self.ui.camera_state_label.setText('ON')
        self.ui.camera_state_label.setStyleSheet(
            'border-color: rgb(100, 100, 100);'
            'border-width: 2px;'
            'border-style: solid;'
            'color: rgb(0, 255, 0);')

    def turn_off_camera(self):
        self.stop_vision_system()

        self.ui.turn_off_camera_push_button.setDisabled(True)
        self.ui.turn_on_camera_push_button.setEnabled(True)
        self.ui.register_product_push_button.setDisabled(True)
        self.ui.edit_product_push_button.setDisabled(True)
        self.ui.test_push_button.setDisabled(True)
        self.show_frame_timer.stop()

        white_image = QImage(
            470, int(470 / self.frames_reader.aspect_ratio),
            QImage.Format_RGB888)
        white_image.fill(QColor(Qt.white).rgb())
        self.pixmap.setPixmap(QPixmap.fromImage(white_image))

        self.ui.camera_state_label.setText('OFF')
        self.ui.camera_state_label.setStyleSheet(
            'border-color: rgb(100, 100, 100);'
            'border-width: 2px;'
            'border-style: solid;'
            'color: rgb(255, 0, 0);')
        self.camera.close()

    def add_product(self, product: Product):
        # Registrar no banco de dados
        self.production.add(product)
        self.update_offset_info_ui(product)

    def load_product_type(self, product_type_id):
        pass
        # product_type = self.data_storager.get_product_type(product_type_id)
        # self.vision_system.load_product_type()

    def edit_product_type(self, product_type_id, product_type):
        pass

    def register_product(self):
        product_name, ok_clicked = QInputDialog().getText(
            self, "Nome do produto", "Nome do produto",
            QLineEdit.Normal, "")
        if ok_clicked and product_name:
            segmentation_dialog = SegmentationSettings(
                product_name, self.camera.create_frames_reader(), parent=self)
            segmentation_dialog.exec()

            if segmentation_dialog.closed_for_next_step:
                segmentation_info = segmentation_dialog.get_segmentation_info()

                template_dialog = TemplatePicking(
                    product_name, self.camera.create_frames_reader(), parent=self)
                template_dialog.exec()

                if template_dialog.closed_for_next_step:
                    template = template_dialog.get_template()

                    product_type = ProductType(
                            product_name, segmentation_info, template)
                    product_type_id = self.data_storager.add_product_type(
                        product_type)
                    self.set_product_types_list(
                        self.data_storager.get_product_types_names())
                    self.set_product_type(product_type_id)

    def set_product_types_list(self, product_type_names: Sequence[ProductTypeName]):
        self.ui.product_type_combo_box.setDisabled(True)
        self.ui.product_type_combo_box.clear()
        for product_type in product_type_names:
            self.ui.product_type_combo_box.addItem(
                f"[{product_type.id:05d}] {product_type.name}", product_type.id)
        if self.ui.product_type_combo_box.count():
            self.ui.product_type_combo_box.setEnabled(True)
            self.ui.start_vision_push_button.setEnabled(True)

    def set_product_type(self, product_type_id):
        for i in range(self.ui.product_type_combo_box.count()):
            if self.ui.product_type_combo_box.itemData(i) == product_type_id:
                self.ui.product_type_combo_box.setCurrentIndex(i)

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

    def update_offset_info_ui(self, product: Product):
        if product.has_cover:
            self.ui.last_offset_label.setText(f'{product.offset:.2f}mm')
        else:
            self.ui.last_offset_label.setText('-')

        # Média
        self.ui.average_offset_label.setText(
            f'{self.production.average_offset():.2f}mm')

        self.ui.number_of_products_label.setText(
            str(self.production.quantity))
        self.ui.no_cover_products_label.setText(
            str(self.production.no_cover_quantity))

    def closeEvent(self, event):
        self.stop()
        event.accept()

    # Slots
    def register_product_push_button_clicked(self):
        self.register_product()

    def product_type_combo_box_index_changed(self, index):
        self.current_product_type_id = self.ui.product_type_combo_box.itemData(index)

    def edit_product_push_button_clicked(self):
        pass

    def test_push_button_clicked(self):
        pass

    def start_vision_push_button_clicked(self):
        self.start_vision_system()

    def stop_vision_push_button_clicked(self):
        self.stop_vision_system()

    def turn_on_camera_push_button_clicked(self):
        self.turn_on_camera()

    def turn_off_camera_push_button_clicked(self):
        self.turn_off_camera()


def main():
    import sys
    import subprocess
    subprocess.call([r'.\UI\generate_py_code_from_ui.bat'])

    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook

    application = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    try:
        application.exec_()
    except:
        print("Exiting program...")


if __name__ == '__main__':
    main()