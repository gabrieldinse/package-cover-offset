# Author: Gabriel Dinse
# File: MainWindow.py
# Date: 11/2/2020
# Made with PyCharm

# Standard Library
from typing import Sequence

# Third party modules
import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtWidgets import (QGraphicsPixmapItem, QGraphicsScene,
                             QMainWindow, QApplication, QInputDialog, QLineEdit)

# Local application imports
from Windows.SegmentationSettings import SegmentationSettings
from Windows.EditSegmentationSettings import EditSegmentationSettings
from Windows.TemplatePicking import TemplatePicking
from Windows.UI.MainWindowUi import Ui_MainWindow
from Data.DataStorager import DataStorager
from Miscellaneous.Helper import (ProductType, ProductTypeName, Product,
                                  Production, SegmentationInfo)
from Modbus.ModbusConnector import ModbusConnector
from Vision.SyncedVideoStream import SyncedVideoStream
from Vision.VideoInfoExtractor import VideoInfoExtractor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Systemas principais da aplicação
        self.camera = SyncedVideoStream.from_file(
            "../Vision/Resources/video_loop.mp4", resolution=(640, 360))
        self.data_storager = DataStorager()
        self.data_storager.open_database()
        self.data_storager.login_to_ftp_server()
        self.vision_system = VideoInfoExtractor(
            self.camera.create_frames_reader())
        self.modbus_connector = ModbusConnector()

        # Sistema auxiliar
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
        self.update_product_types_list()

        self.show_frame_timer = QTimer()
        self.show_frame_timer.timeout.connect(
            self.show_frame)
        self.show_frame_timeout = 70

    def stop(self):
        self.vision_system.stop()
        self.show_frame_timer.stop()
        self.camera.close()
        self.data_storager.close_database()
        self.data_storager.logout_from_ftp_server()

    def start_vision_system(self):
        product_type = self.data_storager.get_product_type(
            self.current_product_type_id)
        self.data_storager.start_production(self.current_product_type_id)
        self.vision_system.start(product_type)

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
        self.data_storager.stop_production()

    def turn_on_camera(self):
        self.camera.open()
        self.ui.turn_on_camera_push_button.setDisabled(True)
        self.ui.turn_off_camera_push_button.setEnabled(True)
        self.ui.register_product_push_button.setEnabled(True)
        self.ui.edit_product_push_button.setEnabled(True)
        self.show_frame_timer.start(self.show_frame_timeout)
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
        self.modbus_connector.send_offset(product.offset)
        self.data_storager.add_product(product)
        self.production.add(product)
        self.update_offset_info_ui(product)

    def add_product_type(self):
        product_name, ok_clicked = QInputDialog().getText(
            self, "Nome do produto", "Nome do produto",
            QLineEdit.Normal, "")

        if ok_clicked and product_name:
            product_type = self.setup_vision_settings(product_name)

            if product_type is not None:
                product_type_id = self.data_storager.add_product_type(
                    product_type)
                self.update_product_types_list()
                self.select_product_type(product_type_id)

    def edit_product_type(self):
        product_type = self.data_storager.get_product_type(
            self.current_product_type_id)
        product_type_id = self.current_product_type_id
        product_name, ok_clicked = QInputDialog().getText(
            self, "Nome do produto", "Nome do produto",
            QLineEdit.Normal, product_type.name)

        if ok_clicked and product_name:
            new_product_type = self.edit_vision_settings(
                product_name, product_type.segmentation_info)

            if new_product_type is not None:
                self.data_storager.edit_product_type(
                    self.current_product_type_id, new_product_type,
                    edit_template=False)
                self.update_product_types_list()
                self.select_product_type(product_type_id)

    def setup_vision_settings(self, product_name):
        segmentation_dialog = SegmentationSettings(
            product_name, self.camera.create_frames_reader())
        segmentation_dialog.exec()

        if not segmentation_dialog.manually_closed:
            segmentation_info = segmentation_dialog.get_segmentation_info()
            template_dialog = TemplatePicking(
                product_name, self.camera.create_frames_reader())
            template_dialog.exec()

            if not template_dialog.manually_closed:
                template = template_dialog.get_template()

                return ProductType(product_name, segmentation_info, template)

        return None

    def edit_vision_settings(self, product_name,
                             segmentation_info: SegmentationInfo):
        segmentation_dialog = EditSegmentationSettings(
            product_name, self.camera.create_frames_reader(), segmentation_info)
        segmentation_dialog.exec()

        if not segmentation_dialog.manually_closed:
            new_segmentation_info = segmentation_dialog.get_segmentation_info()
            template_dialog = TemplatePicking(
                product_name, self.camera.create_frames_reader())
            template_dialog.exec()

            if not template_dialog.manually_closed:
                template = template_dialog.get_template()

                return ProductType(
                    product_name, new_segmentation_info, template)

        elif segmentation_dialog.finished_editing:
            new_segmentation_info = segmentation_dialog.get_segmentation_info()

            return ProductType(product_name, new_segmentation_info)

        return None

    def update_product_types_list(self):
        self.ui.product_type_combo_box.setDisabled(True)
        self.ui.product_type_combo_box.clear()
        for product_type in self.data_storager.get_product_types_names():
            self.ui.product_type_combo_box.addItem(
                f"[{product_type.id:05d}] {product_type.name}", product_type.id)
        if self.ui.product_type_combo_box.count():
            self.ui.product_type_combo_box.setEnabled(True)
            self.ui.start_vision_push_button.setEnabled(True)

    def select_product_type(self, product_type_id):
        for i in range(self.ui.product_type_combo_box.count()):
            if self.ui.product_type_combo_box.itemData(i) == product_type_id:
                self.ui.product_type_combo_box.setCurrentIndex(i)

    def show_frame(self):
        frame = self.frames_reader.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, _ = frame.shape
        bytes_per_line = 3 * width

        gui_frame = QImage(frame.data, width, height,
                           bytes_per_line, QImage.Format_RGB888)
        gui_frame = gui_frame.scaled(470, 470, Qt.KeepAspectRatio)
        self.pixmap.setPixmap(QPixmap.fromImage(gui_frame))

    def update_offset_info_ui(self, product: Product):
        if product.has_cover:
            self.ui.last_offset_label.setText(f'{product.offset:.1f}mm')
        else:
            self.ui.last_offset_label.setText('Sem tampa')

        # Média
        self.ui.average_offset_label.setText(
            f'{self.production.average_offset():.1f}mm')

        self.ui.number_of_products_label.setText(
            str(self.production.quantity))
        self.ui.no_cover_products_label.setText(
            str(self.production.no_cover_quantity))

    def closeEvent(self, event):
        self.stop()
        event.accept()

    # Slots
    def register_product_push_button_clicked(self):
        self.add_product_type()

    def product_type_combo_box_index_changed(self, index):
        self.current_product_type_id = self.ui.product_type_combo_box.itemData(index)

    def edit_product_push_button_clicked(self):
        self.edit_product_type()

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