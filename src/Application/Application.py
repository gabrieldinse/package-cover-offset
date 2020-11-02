# Author: Gabriel Dinse
# File: Application
# Date: 11/1/2020
# Made with PyCharm

# Standard Library
import sys
from threading import Thread

# Third party modules
from PyQt5.QtWidgets import (QGraphicsPixmapItem, QGraphicsScene,
                             QMainWindow, QApplication)


# Local application imports
from Database.Database import Database
from MainWindow import MainWindow
from SettingsDialog import SettingsDialog
from Visao.VideoInfoExtractor import VideoInfoExtractor
from Helper import WorkerQueue


class Application(QApplication):
    def __init__(self):
        super().__init__(sys.argv)

        self.database = Database()
        self.window = MainWindow(self)
        self.vision_system = VideoInfoExtractor(self)
        self.frames_shower = WorkerQueue(self.window.show_frames)
        self.products_adder = WorkerQueue(self.window.add_product)
        self.vision_system.events.bind(new_frame=self.frames_shower.put)
        self.vision_system.events.bind(new_product=self.products_adder.put)

        self.running = False

    def run(self):
        self.running = True
        Thread(target=self.frames_shower.run, args=()).start()
        Thread(target=self.products_adder.run, args=()).start()
        Thread(target=self.vision_system.run, args=()).start()

        self.window.show()
        sys.exit(self.exec_())   # Blocks

def main():
    app = Application()
    app.run()

if __name__ == '__main__':
    main()
