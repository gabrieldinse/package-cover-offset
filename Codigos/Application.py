# Author: Gabriel Dinse
# File: Application
# Date: 11/1/2020
# Made with PyCharm

# Standard Library

# Third party modules

# Local application imports
from Database import Database
from Window import Window


class Application:
    def __init__(self):
        self.database = Database()
        self.window = Window(self.database)

    def run(self):
        self.application = QApplication(sys.argv)
        self.window = MainWindow()
        self.window.show()
        sys.exit(application.exec_())


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
