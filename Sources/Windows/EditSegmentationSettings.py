# Author: Gabriel Dinse
# File: EditSegmentationSettings.py
# Date: 12/6/2020
# Made with PyCharm

# Standard Library


# Third party modules
import cv2
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QGraphicsPixmapItem, QGraphicsScene,
                             QDialog)
from skimage import img_as_ubyte
from skimage.morphology import convex_hull_image

# Local application imports
from Miscellaneous.Helper import SegmentationInfo
from Windows.UI.EditSegmentationSettingsUi import Ui_Dialog
from Vision.SyncedVideoStream import FramesReader


class EditSegmentationSettings(QDialog):
    def __init__(self, window_name: str, frames_reader: FramesReader,
                 segmentation_info, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.window_name = window_name
        self.frames_reader = frames_reader

        self.setWindowTitle(self.window_name)
        self.manually_closed = True
        self.finished_editing = False

        # Configurações dos QGraphicsView
        self.scene = QGraphicsScene()
        self.ui.graphics_view.setScene(self.scene)
        self.pixmap = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap)

        self.segmentation_scene = QGraphicsScene()
        self.ui.segmentation_graphics_view.setScene(self.segmentation_scene)
        self.segmentation_pixmap = QGraphicsPixmapItem()
        self.segmentation_scene.addItem(self.segmentation_pixmap)

        # # Coneccao dos signals e slots
        self.ui.lower_canny_slider.valueChanged.connect(
            self.lower_canny_slider_value_changed)
        self.ui.upper_canny_slider.valueChanged.connect(
            self.upper_canny_slider_value_changed)
        self.ui.gaussian_kernel_spin_box.valueChanged.connect(
            self.gaussian_kernel_spin_box_value_changed)
        self.ui.otsu_radio_button.toggled.connect(
            self.otsu_radio_button_toggled)
        self.ui.manual_radio_button.toggled.connect(
            self.manual_radio_button_toggled)
        self.ui.next_push_button.clicked.connect(
            self.next_push_button_clicked)
        self.ui.conclude_push_button.clicked.connect(
            self.conclude_push_button_clicked)

        self.lower_canny = segmentation_info.lower_canny
        self.upper_canny = segmentation_info.upper_canny
        self.gaussian_kernel_size = segmentation_info.gaussian_filter_size
        self.ui.manual_radio_button.setChecked(True)
        self.ui.lower_canny_slider.setValue(self.lower_canny)
        self.ui.upper_canny_slider.setValue(self.upper_canny)
        self.ui.gaussian_kernel_spin_box.setValue(self.gaussian_kernel_size)

        self.show_frame_timer = QTimer()
        self.show_frame_timer.timeout.connect(
            self._segment_and_show_frame)
        self.show_frame_timer.start(50)

    def _segment_and_show_frame(self) -> None:
        frame = self.frames_reader.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, _ = frame.shape
        bytes_per_line = 3 * width

        # Segmentação por Canny e Convex hull
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        blurred_gray_frame = cv2.GaussianBlur(
            gray_frame,
            (self.gaussian_kernel_size, self.gaussian_kernel_size), 0)

        self._calculate_canny_threshold(blurred_gray_frame)
        canny_edges = cv2.Canny(
            blurred_gray_frame, self.lower_canny, self.upper_canny)
        convex_hull = img_as_ubyte(convex_hull_image(canny_edges))

        contours, _ = cv2.findContours(convex_hull, cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            contour = contours[0]
            cv2.drawContours(frame, [contour], 0, (0, 255, 0), 2)

        # Mostra o frame original com o contorno  da embalagem
        gui_frame = QImage(frame.data, width, height,
                           bytes_per_line, QImage.Format_RGB888)
        gui_frame = gui_frame.scaled(470, 470, Qt.KeepAspectRatio)
        self.pixmap.setPixmap(QPixmap.fromImage(gui_frame))

        # Mostra o frame segmentado
        segmented_gui_frame = QImage(
            convex_hull.data, width, height, QImage.Format_Grayscale8)
        segmented_gui_frame = segmented_gui_frame.scaled(
            470, 470, Qt.KeepAspectRatio)
        self.segmentation_pixmap.setPixmap(
            QPixmap.fromImage(segmented_gui_frame))

    def _calculate_canny_threshold(self, gray_frame: np.ndarray) -> None:
        if self.ui.otsu_radio_button.isChecked():
            self.upper_canny, thresh_image = cv2.threshold(
                gray_frame, 0, 255,
                cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            self.lower_canny = 0.5 * self.upper_canny
        else:
            self.lower_canny = self.ui.lower_canny_slider.value()
            self.upper_canny = self.ui.upper_canny_slider.value()

    def get_segmentation_info(self) -> SegmentationInfo:
        return SegmentationInfo(self.lower_canny, self.upper_canny,
                                self.gaussian_kernel_size)

    def otsu_radio_button_toggled(self) -> None:
        self.ui.upper_canny_slider.setDisabled(True)
        self.ui.lower_canny_slider.setDisabled(True)

    def manual_radio_button_toggled(self) -> None:
        self.ui.upper_canny_slider.setEnabled(True)
        self.ui.lower_canny_slider.setEnabled(True)

    def lower_canny_slider_value_changed(self) -> None:
        self.lower_canny = self.ui.lower_canny_slider.value()
        self.ui.lower_canny_label.setText(str(self.lower_canny))

    def upper_canny_slider_value_changed(self) -> None:
        self.upper_canny = self.ui.upper_canny_slider.value()
        self.ui.upper_canny_label.setText(str(self.upper_canny))

    def gaussian_kernel_spin_box_value_changed(self) -> None:
        if self.ui.gaussian_kernel_spin_box.value() % 2 == 0:
            self.ui.gaussian_kernel_spin_box.setValue(
                self.ui.gaussian_kernel_spin_box.value() + 1)
        self.gaussian_kernel_size = self.ui.gaussian_kernel_spin_box.value()

    def next_push_button_clicked(self) -> None:
        self.show_frame_timer.stop()
        self.manually_closed = False
        self.close()

    def conclude_push_button_clicked(self) -> None:
        self.show_frame_timer.stop()
        self.finished_editing = True
        self.close()