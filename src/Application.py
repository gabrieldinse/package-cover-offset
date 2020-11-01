# Author: Gabriel Dinse
# File: Application
# Date: 11/1/2020
# Made with PyCharm

# Standard Library

# Third party modules

# Local application imports
from Database import Database
from Window import Window
from CameraStream import CameraStream
from Visao.ProductInfoExtractor import ProductInfoExtractor


class Application:
    def __init__(self):
        self.database = Database()
        self.vision_system = ProductInfoExtractor()
        self.window = Window(self.database, self.vision_system)
        self.application = QApplication(sys.argv)

    def run(self):
        self.window.show()
        sys.exit(self.application.exec_())   # Blocks


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
