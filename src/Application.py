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
from Helper import WorkerQueue, ProductType, ProductInfo
from Vision.SyncedVideoStream import SyncedVideoStream, FramesReader


class Application:
    def __init__(self):
        self.application = QApplication(sys.argv)
        self.camera = SyncedVideoStream().from_camera(1)
        self.data_storager = DataStorager()
        self.window = MainWindow(self.camera.create_frames_reader())
        self.vision_system = VideoInfoExtractor(self)

        # A aplicação lida com os eventos dos sistemas (observer)
        self.vision_system.bind(new_product=self.register_product)
        self.window.bind(new_product_type=self.register_product_type)
        self.window.bind(product_type_edited=self.edit_product_type)
        self.window.bind(vision_system_start=self.start_vision_system)
        self.window.bind(vision_system_stop=self.stop_vision_system)
        self.window.bind(close=self.stop)
        self.window.bind(turn_on_camera=self.turn_on_camera)
        self.window.bind(turn_off_camera=self.turn_off_camera)

        self.running = False

    def register_product(self, product_info : ProductInfo):
        # self.database.register_product(product_info)
        self.window.products_adder.put(product_info)

    def register_product_type(self, product_type : ProductType):
        pass
        # product_type_id = self.data_storager.register_product_type(product_type)

    def load_product_type(self, product_type_id):
        pass
        # product_type = self.data_storager.get_product_type(product_type_id)
        # self.vision_system.load_product_type()

    def edit_product_type(self, product_type_id, product_type):
        pass

    def start_vision_system(self):
        pass

    def stop_vision_system(self):
        self.window.finish_vision()

    def turn_on_camera(self):
        self.camera.open()

    def turn_off_camera(self):
        self.camera.close()

    def run(self):
        self.running = True
        self.window.show()
        sys.exit(self.application.exec_())   # Blocks

    def stop(self):
        self.camera.close()
        self.running = False

def main():
    subprocess.call([r'.\ApplicationWindows\generate_py_code_from_ui.bat'])
    app = Application()
    app.run()

if __name__ == '__main__':
    main()
