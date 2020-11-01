# Author: Gabriel Dinse
# File: Application
# Date: 11/1/2020
# Made with PyCharm

# Standard Library
from threading import Thread

# Third party modules

# Local application imports
from Database import Database
from Window import Window
from Visao.VideoInfoExtractor import VideoInfoExtractor


class Application:
    def __init__(self):
        self.database = Database()
        self.vision_system = ProductInfoExtractor(
            application.window.product_added)
        self.window = Window(self.database, self.vision_system)
        self.application = QApplication(sys.argv)

    def run(self):
        self.window.show()
        Thread(target=self.vision_system.run, args=()).start()
        sys.exit(self.application.exec_())   # Blocks


def main():
    app = Application()
    app.run()

if __name__ == '__main__':
    main()
