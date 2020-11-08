# Author: Gabriel Dinse
# File: ApplicationWindows
# Date: 11/1/2020
# Made with PyCharm

# Standard Library
import sys
from threading import Thread

# Third party modules
from PyQt5.QtWidgets import QApplication


# Local application imports
from Database.Database import Database
from ApplicationWindows.MainWindow import MainWindow
from Visao.VideoInfoExtractor import VideoInfoExtractor
from Helper import WorkerQueue


class Application:
    def __init__(self):
        self.application = QApplication(sys.argv)
        self.database = Database()
        self.window = MainWindow(self)
        self.vision_system = VideoInfoExtractor(self)

        # A aplicação lida com os eventos dos sistemas (observer)
        self.vision_system.bind(new_frame=self.add_frame)
        self.vision_system.bind(new_product=self.add_product)
        self.window.bind(new_product_type=self.add_product_type)
        self.window.bind(product_type_edited=self.edit_product_type)
        self.window.bind(vision_system_start=self.start_vision_system)
        self.window.bind(vision_system_stop=self.stop_vision_system)

        self.running = False

    def add_frame(self, frame, mask):
        self.window.frames_shower.put(frame, mask)

    def add_product(self, product_info):
        self.window.products_adder.put(product_info)
        # Poe na database

    def add_product_type(self, product_type):
        pass

    def edit_product_type(self, product_type_id, product_type):
        pass

    def start_vision_system(self):
        pass

    def stop_vision_system(self):
        self.window.finish_vision()

    def run(self):
        self.running = True

        self.window.show()
        sys.exit(self.application.exec_())   # Blocks

    def finish_works(self):


def main():
    app = Application()
    app.run()

if __name__ == '__main__':
    main()
