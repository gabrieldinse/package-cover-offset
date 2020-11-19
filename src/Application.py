# Author: Gabriel Dinse
# File: ApplicationWindows
# Date: 11/1/2020
# Made with PyCharm

# Standard Library
import sys
from threading import Thread
import subprocess

# Third party modules
from PyQt5.QtWidgets import QApplication

# Local application imports
from Data.DataStorager import DataStorager
from ApplicationWindows.MainWindow import MainWindow
from Vision.VideoInfoExtractor import VideoInfoExtractor
from Helper import WorkerQueue, ProductType, ProductInfo, SegmentationInfo
from Vision.SyncedVideoStream import SyncedVideoStream, FramesReader


class Application:
    def __init__(self):
        self.application = QApplication(sys.argv)
        self.camera = SyncedVideoStream().from_camera(3)
        self.data_storager = DataStorager()
        self.data_storager.open_database()
        self.window = MainWindow(self.camera.create_frames_reader())
        self.vision_system = VideoInfoExtractor(self.camera.create_frames_reader())

        # Configurações iniciais
        self.window.set_product_types_list(
            self.data_storager.get_product_types_names())

        # A aplicação lida com os eventos dos sistemas (observer)
        self.vision_system.bind(new_product=self.add_product)
        self.window.bind(new_product_type=self.add_product_type)
        self.window.bind(product_type_edited=self.edit_product_type)
        self.window.bind(vision_start=self.start_vision_system)
        self.window.bind(vision_stop=self.stop_vision_system)
        self.window.bind(close=self.stop)
        self.window.bind(turn_on_camera=self.turn_on_camera)
        self.window.bind(turn_off_camera=self.turn_off_camera)

        self.running = False

    def add_product(self, product_info : ProductInfo):
        # Registrar no banco de dados
        self.window.products_adder.put(product_info)

    def add_product_type(self, product_type : ProductType):
        product_type_id = self.data_storager.add_product_type(product_type)
        self.window.set_product_types_list(
            self.data_storager.get_product_types_names())
        self.window.set_product_type(product_type_id)

    def load_product_type(self, product_type_id):
        pass
        # product_type = self.data_storager.get_product_type(product_type_id)
        # self.vision_system.load_product_type()

    def edit_product_type(self, product_type_id, product_type):
        pass

    def start_vision_system(self, product_type_id):
        self.vision_system.start(
            self.data_storager.get_product_type(product_type_id).segmentation_info)

    def stop_vision_system(self):
        self.vision_system.stop()

    def turn_on_camera(self):
        self.camera.open()

    def turn_off_camera(self):
        self.camera.close()

    def run(self):
        self.running = True
        self.window.show()
        sys.exit(self.application.exec_())   # Blocks

    def stop(self):
        self.vision_system.stop()
        self.camera.close()
        self.data_storager.close_database()
        self.running = False


def main():
    subprocess.call([r'.\ApplicationWindows\generate_py_code_from_ui.bat'])
    app = Application()
    app.run()


if __name__ == '__main__':
    main()
