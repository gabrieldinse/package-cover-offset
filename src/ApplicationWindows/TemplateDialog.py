# Author: Gabriel Dinse
# File: TemplateDialog.py
# Date: 11/3/2020
# Made with PyCharm

# Standard Library

# Third party modules
from PyQt5.QtWidgets import (QGraphicsPixmapItem, QGraphicsScene,
                             QDialog, QApplication,  QGraphicsLineItem)
from PyQt5 import uic
from PyQt5.QtGui import QBrush
from PyQt5.Qt import QColor

# Local application imports


class TemplateConfigurationScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.upper_left_selected = False
        self.bottom_right_selected = False
        self.line_left = None
        self.line_top = None
        self.line_bot = None
        self.line_right = None

    def reset(self):
        self.removeItem(self.template_rect)
        self.upper_left_selected = False
        self.bottom_right_selected = False

    def mousePressEvent(self, event):
        if not self.upper_left_selected:
            self.upper_left_selected = True
            self.line_top = QGraphicsLineItem(
                0, event.scenePos().y(), self.sceneRect().width(),
                event.scenePos().y())
            self.line_left = QGraphicsLineItem(
                event.scenePos().x(), 0, event.scenePos().x(),
                self.sceneRect().height())
            self.addItem(self.line_top)
            self.addItem(self.line_left)
        else:
            self.bottom_right_selected = True
            self.line_bot = QGraphicsLineItem(
                0, event.scenePos().y(), self.sceneRect().width(),
                event.scenePos().y())
            self.line_right = QGraphicsLineItem(
                event.scenePos().x(), 0, event.scenePos().x(),
                self.sceneRect().height())
            self.addItem(self.line_bot)
            self.addItem(self.line_right)


class TemplateDialog(QDialog):
    def __init__(self, product_name, parent=None):
        super().__init__(parent)
        uic.loadUi("ApplicationWindows/template_dialog.ui", self)
        self.setWindowTitle(product_name)

        self.scene = TemplateConfigurationScene()
        self.graphics_view.setScene(self.scene)
        self.pixmap = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap)