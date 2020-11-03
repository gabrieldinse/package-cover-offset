# Author: Gabriel Dinse
# File: TemplatePicking.py
# Date: 11/3/2020
# Made with PyCharm

# Standard Library

# Third party modules
from PyQt5.QtWidgets import (QGraphicsPixmapItem, QGraphicsScene,
                             QDialog, QApplication,  QGraphicsLineItem,
                             QMessageBox)
from PyQt5 import uic
from PyQt5.QtGui import QBrush, QImage, QPixmap, QPen
from PyQt5.Qt import QColor
from PyQt5.QtCore import QTimer, Qt
import cv2

# Local application imports
from Visao.Camera import Camera


class TemplateConfigurationScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.upper_left_selected = False
        self.bottom_right_selected = False
        self.line_left = None
        self.line_top = None
        self.line_bot = None
        self.line_right = None
        self.upper_left = None
        self.bottom_right = None
        self.pen = QPen()
        self.pen.setColor(Qt.green)
        self.pen.setWidth(3)

        self.scale = 640 / 480

    def reset(self):
        self.removeItem(self.line_left)
        self.removeItem(self.line_right)
        self.removeItem(self.line_top)
        self.removeItem(self.line_bot)
        self.upper_left_selected = False
        self.bottom_right_selected = False
        msg_box = QMessageBox()
        msg_box.setText("Selecione o ponto superior esquerdo do template")
        msg_box.exec()

    def mousePressEvent(self, event):
        if not self.upper_left_selected:
            self.upper_left_selected = True
            self.upper_left = event.scenePos() * self.scale
            self.line_top = QGraphicsLineItem(
                0, event.scenePos().y(), self.sceneRect().width(),
                event.scenePos().y())
            self.line_top.setPen(self.pen)
            self.line_left = QGraphicsLineItem(
                event.scenePos().x(), 0, event.scenePos().x(),
                self.sceneRect().height())
            self.line_top.setPen(self.pen)
            self.line_left.setPen(self.pen)
            self.addItem(self.line_top)
            self.addItem(self.line_left)

            msg_box = QMessageBox()
            msg_box.setText("Selecione o ponto inferior direito do template")
            msg_box.exec()

        elif not self.bottom_right_selected:
            self.bottom_right_selected = True
            self.bottom_right = event.scenePos() * self.scale
            self.line_bot = QGraphicsLineItem(
                0, event.scenePos().y(), self.sceneRect().width(),
                event.scenePos().y())
            self.line_right = QGraphicsLineItem(
                event.scenePos().x(), 0, event.scenePos().x(),
                self.sceneRect().height())
            self.line_bot.setPen(self.pen)
            self.line_right.setPen(self.pen)
            self.addItem(self.line_bot)
            self.addItem(self.line_right)


class TemplatePicking(QDialog):
    def __init__(self, product_name, parent=None):
        super().__init__(parent)
        uic.loadUi("ApplicationWindows/template_dialog.ui", self)
        self.setWindowTitle(product_name)
        self.product_name = product_name

        self.camera = Camera()

        self.scene = TemplateConfigurationScene()
        self.graphics_view.setScene(self.scene)
        self.pixmap = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap)

        self.finish_push_button.clicked.connect(self.finish_push_button_clicked)
        self.reset_push_button.clicked.connect(self.reset_push_button_clicked)

        self.frames_processor_timer = QTimer()
        self.frames_processor_timer.timeout.connect(
            self.show_frame)
        self.frames_processor_timer.start(0)

    def exec(self):
        self.show()
        msg_box = QMessageBox()
        msg_box.setText("Selecione o ponto superior esquerdo do template")
        msg_box.show()
        super().exec()

    def show_frame(self):
        grabbed, frame = self.camera.read()
        if grabbed:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, _ = frame.shape
            bytes_per_line = 3 * width

            # Frame segmentado
            gui_frame = QImage(frame.data, width, height,
                               bytes_per_line, QImage.Format_RGB888)
            gui_frame = gui_frame.scaled(480, 480, Qt.KeepAspectRatio)
            self.pixmap.setPixmap(QPixmap.fromImage(gui_frame))

    def get_template(self):
        return self.frame[
               int(self.scene.upper_left.y()):int(self.scene.bottom_right.y()),
               int(self.scene.upper_left.x()):int(self.scene.bottom_right.x())]

    def reset_push_button_clicked(self):
        self.scene.reset()

    def finish_push_button_clicked(self):
        grabbed, self.frame = self.camera.read()
        self.camera.release()
        self.close_for_next_step = True
        self.close()