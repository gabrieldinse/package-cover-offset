# Author: Gabriel Dinse
# File: TemplatePicking.py
# Date: 11/3/2020
# Made with PyCharm

# Standard Library

# Third party modules
from PyQt5.QtWidgets import (QGraphicsPixmapItem, QGraphicsScene,
                             QDialog, QGraphicsLineItem,
                             QMessageBox)
from PyQt5.QtGui import QImage, QPixmap, QPen
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
import cv2

# Local application imports
from Windows.UI.TemplatePickingUi import Ui_Dialog


class TemplateConfigurationScene(QGraphicsScene):
    first_point_added = pyqtSignal()
    second_point_added = pyqtSignal()

    def __init__(self, camera_width):
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
        self.pen.setWidth(2)

        self.first_mouse_move = True
        self.scale = camera_width / 470

        self.mouse_hori_line = QGraphicsLineItem(0, 0, 0, 0)
        self.mouse_vert_line = QGraphicsLineItem(0, 0, 0, 0)
        self.mouse_hori_line.setPen(self.pen)
        self.mouse_vert_line.setPen(self.pen)

    def reset(self):
        self.removeItem(self.line_left)
        self.removeItem(self.line_right)
        self.removeItem(self.line_top)
        self.removeItem(self.line_bot)
        self.upper_left_selected = False
        self.bottom_right_selected = False
        self.first_mouse_move = True

    def is_mouse_on_scene(self, position):
        return (position.x() < self.sceneRect().width() - self.pen.width()) \
               and (position.y() < self.sceneRect().height() - self.pen.width())

    def mouseMoveEvent(self, event):
        if self.is_mouse_on_scene(event.scenePos()):
            self.mouse_hori_line.setLine(
                0, event.scenePos().y(), self.sceneRect().width() - self.pen.width(),
                event.scenePos().y())
            self.mouse_vert_line.setLine(
                event.scenePos().x(), 0, event.scenePos().x(),
                self.sceneRect().height() - self.pen.width())
            if self.first_mouse_move:
                self.first_mouse_move = False
                self.addItem(self.mouse_hori_line)
                self.addItem(self.mouse_vert_line)

    def mousePressEvent(self, event):
        if self.is_mouse_on_scene(event.scenePos()):
            if not self.upper_left_selected:
                self.upper_left_selected = True
                self.upper_left = event.scenePos() * self.scale
                self.line_top = QGraphicsLineItem(
                    0, event.scenePos().y(), self.sceneRect().width() - self.pen.width(),
                    event.scenePos().y())
                self.line_left = QGraphicsLineItem(
                    event.scenePos().x(), 0, event.scenePos().x(),
                    self.sceneRect().height() - self.pen.width())
                self.line_top.setPen(self.pen)
                self.line_left.setPen(self.pen)
                self.addItem(self.line_top)
                self.addItem(self.line_left)
                self.first_point_added.emit()

            elif not self.bottom_right_selected:
                self.bottom_right_selected = True
                self.bottom_right = event.scenePos() * self.scale
                self.line_bot = QGraphicsLineItem(
                    0, event.scenePos().y(), self.sceneRect().width() - self.pen.width(),
                    event.scenePos().y())
                self.line_right = QGraphicsLineItem(
                    event.scenePos().x(), 0, event.scenePos().x(),
                    self.sceneRect().height() - self.pen.width())
                self.line_bot.setPen(self.pen)
                self.line_right.setPen(self.pen)
                self.addItem(self.line_bot)
                self.addItem(self.line_right)
                self.removeItem(self.mouse_vert_line)
                self.removeItem(self.mouse_hori_line)
                self.second_point_added.emit()


class TemplatePicking(QDialog):
    def __init__(self, window_name, frames_reader, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.window_name = window_name
        self.frames_reader = frames_reader

        self.setWindowTitle(self.window_name)
        self.closed_for_next_step = False

        self.scene = TemplateConfigurationScene(self.frames_reader.resolution[0])
        self.ui.graphics_view.setScene(self.scene)
        self.pixmap = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap)
        self.ui.graphics_view.setMouseTracking(True)

        self.scene.first_point_added.connect(self.first_point_added)
        self.scene.second_point_added.connect(self.second_point_added)
        self.ui.finish_push_button.clicked.connect(self.finish_push_button_clicked)
        self.ui.reset_push_button.clicked.connect(self.reset_push_button_clicked)

        self.show_frame_timer = QTimer()
        self.show_frame_timer.timeout.connect(
            self.show_frame)
        self.show_frame_timer.start(50)

    def exec(self):
        self.show()
        self.show_first_point_message()
        super().exec()

    @staticmethod
    def show_first_point_message():
        msg_box = QMessageBox()
        msg_box.setText("Selecione o ponto superior esquerdo do template")
        msg_box.exec()

    @staticmethod
    def show_second_point_message():
        msg_box = QMessageBox()
        msg_box.setText("Selecione o ponto inferior direito do template")
        msg_box.exec()

    def show_frame(self):
        try:
            frame = self.frames_reader.read()
        except FrameReadingError:
            raise
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, _ = frame.shape
            bytes_per_line = 3 * width

            # Frame segmentado
            gui_frame = QImage(frame.data, width, height,
                               bytes_per_line, QImage.Format_RGB888)
            gui_frame = gui_frame.scaled(470, 470, Qt.KeepAspectRatio)
            self.pixmap.setPixmap(QPixmap.fromImage(gui_frame))

    def get_template(self):
        return self.frame[
               int(self.scene.upper_left.y()):int(self.scene.bottom_right.y()),
               int(self.scene.upper_left.x()):int(self.scene.bottom_right.x())]

    def first_point_added(self):
        self.show_second_point_message()

    def second_point_added(self):
        self.ui.finish_push_button.setEnabled(True)

    def reset_push_button_clicked(self):
        self.scene.reset()
        self.show_first_point_message()
        self.ui.finish_push_button.setDisabled(True)

    def finish_push_button_clicked(self):
        self.show_frame_timer.stop()
        try:
            self.frame = self.frames_reader.read()
        except FrameReadingError:
            raise
        else:
            self.closed_for_next_step = True
            self.close()