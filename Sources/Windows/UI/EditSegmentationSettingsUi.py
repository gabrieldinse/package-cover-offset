# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edit_segmentation_settings_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1000, 570)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(1000, 570))
        Dialog.setMaximumSize(QtCore.QSize(1000, 570))
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(14, 18, 972, 539))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_33 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_33.setFont(font)
        self.label_33.setStyleSheet("background-color: rgb(235, 235, 235);\n"
"color: rgb(50, 50, 50);\n"
"border-color: rgb(100, 100, 100);\n"
"border-width : 2px;\n"
"border-style:solid;")
        self.label_33.setAlignment(QtCore.Qt.AlignCenter)
        self.label_33.setObjectName("label_33")
        self.verticalLayout_4.addWidget(self.label_33)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_10 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setMinimumSize(QtCore.QSize(0, 30))
        self.label_10.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setAutoFillBackground(False)
        self.label_10.setStyleSheet("background-color: rgb(235, 235, 235);\n"
"color: rgb(50, 50, 50);\n"
"border-color: rgb(100, 100, 100);\n"
"border-width : 2px;\n"
"border-style:solid;")
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.verticalLayout.addWidget(self.label_10)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem)
        self.label_7 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(50, 50, 50);")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_11.addWidget(self.label_7)
        self.gaussian_kernel_spin_box = QtWidgets.QSpinBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gaussian_kernel_spin_box.sizePolicy().hasHeightForWidth())
        self.gaussian_kernel_spin_box.setSizePolicy(sizePolicy)
        self.gaussian_kernel_spin_box.setStyleSheet("color: rgb(50, 50, 50);\n"
"")
        self.gaussian_kernel_spin_box.setReadOnly(False)
        self.gaussian_kernel_spin_box.setMinimum(3)
        self.gaussian_kernel_spin_box.setMaximum(49)
        self.gaussian_kernel_spin_box.setSingleStep(2)
        self.gaussian_kernel_spin_box.setProperty("value", 5)
        self.gaussian_kernel_spin_box.setObjectName("gaussian_kernel_spin_box")
        self.horizontalLayout_11.addWidget(self.gaussian_kernel_spin_box)
        spacerItem1 = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_11)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout_7.addLayout(self.verticalLayout)
        self.line_2 = QtWidgets.QFrame(self.layoutWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_7.addWidget(self.line_2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_9 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QtCore.QSize(0, 30))
        self.label_9.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setAutoFillBackground(False)
        self.label_9.setStyleSheet("background-color: rgb(235, 235, 235);\n"
"color: rgb(50, 50, 50);\n"
"border-color: rgb(100, 100, 100);\n"
"border-width : 2px;\n"
"border-style:solid;")
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_2.addWidget(self.label_9)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem3 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.otsu_radio_button = QtWidgets.QRadioButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.otsu_radio_button.setFont(font)
        self.otsu_radio_button.setStyleSheet("color: rgb(50, 50, 50);")
        self.otsu_radio_button.setChecked(True)
        self.otsu_radio_button.setObjectName("otsu_radio_button")
        self.canny_threshold_button_group = QtWidgets.QButtonGroup(Dialog)
        self.canny_threshold_button_group.setObjectName("canny_threshold_button_group")
        self.canny_threshold_button_group.addButton(self.otsu_radio_button)
        self.horizontalLayout_5.addWidget(self.otsu_radio_button)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.line = QtWidgets.QFrame(self.layoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_4.addWidget(self.line)
        self.manual_radio_button = QtWidgets.QRadioButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.manual_radio_button.setFont(font)
        self.manual_radio_button.setStyleSheet("color: rgb(50, 50, 50);")
        self.manual_radio_button.setObjectName("manual_radio_button")
        self.canny_threshold_button_group.addButton(self.manual_radio_button)
        self.horizontalLayout_4.addWidget(self.manual_radio_button)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgb(235, 235, 235);\n"
"color: rgb(50, 50, 50);\n"
"border-color: rgb(100, 100, 100);\n"
"border-width : 2px;\n"
"border-style:solid;")
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.verticalLayout_5.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(7)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lower_canny_slider = QtWidgets.QSlider(self.layoutWidget)
        self.lower_canny_slider.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lower_canny_slider.sizePolicy().hasHeightForWidth())
        self.lower_canny_slider.setSizePolicy(sizePolicy)
        self.lower_canny_slider.setMinimumSize(QtCore.QSize(130, 0))
        self.lower_canny_slider.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lower_canny_slider.setStyleSheet("QSlider::handle:horizontal {\n"
"    background: rgb(245, 245, 245);\n"
"    border: 2px solid #565a5e;\n"
"    width: 24px;\n"
"    height: 8px;\n"
"    border-radius: 4px;\n"
"}")
        self.lower_canny_slider.setMaximum(255)
        self.lower_canny_slider.setSingleStep(1)
        self.lower_canny_slider.setPageStep(10)
        self.lower_canny_slider.setOrientation(QtCore.Qt.Horizontal)
        self.lower_canny_slider.setTickInterval(1)
        self.lower_canny_slider.setObjectName("lower_canny_slider")
        self.horizontalLayout.addWidget(self.lower_canny_slider)
        spacerItem4 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.lower_canny_label = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lower_canny_label.sizePolicy().hasHeightForWidth())
        self.lower_canny_label.setSizePolicy(sizePolicy)
        self.lower_canny_label.setMinimumSize(QtCore.QSize(35, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lower_canny_label.setFont(font)
        self.lower_canny_label.setStyleSheet("color: rgb(50, 50, 50);\n"
"")
        self.lower_canny_label.setObjectName("lower_canny_label")
        self.horizontalLayout.addWidget(self.lower_canny_label)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addLayout(self.verticalLayout_5)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: rgb(235, 235, 235);\n"
"color: rgb(50, 50, 50);\n"
"border-color: rgb(100, 100, 100);\n"
"border-width : 2px;\n"
"border-style:solid;")
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_6.addWidget(self.label_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.upper_canny_slider = QtWidgets.QSlider(self.layoutWidget)
        self.upper_canny_slider.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.upper_canny_slider.sizePolicy().hasHeightForWidth())
        self.upper_canny_slider.setSizePolicy(sizePolicy)
        self.upper_canny_slider.setMinimumSize(QtCore.QSize(130, 0))
        self.upper_canny_slider.setMaximumSize(QtCore.QSize(150, 16777215))
        self.upper_canny_slider.setStyleSheet("QSlider::handle:horizontal {\n"
"    background: rgb(245, 245, 245);\n"
"    border: 2px solid #565a5e;\n"
"    width: 24px;\n"
"    height: 8px;\n"
"    border-radius: 4px;\n"
"}")
        self.upper_canny_slider.setMaximum(255)
        self.upper_canny_slider.setOrientation(QtCore.Qt.Horizontal)
        self.upper_canny_slider.setTickInterval(1)
        self.upper_canny_slider.setObjectName("upper_canny_slider")
        self.horizontalLayout_2.addWidget(self.upper_canny_slider)
        spacerItem5 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.upper_canny_label = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.upper_canny_label.sizePolicy().hasHeightForWidth())
        self.upper_canny_label.setSizePolicy(sizePolicy)
        self.upper_canny_label.setMinimumSize(QtCore.QSize(35, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.upper_canny_label.setFont(font)
        self.upper_canny_label.setStyleSheet("color: rgb(50, 50, 50);\n"
"")
        self.upper_canny_label.setObjectName("upper_canny_label")
        self.horizontalLayout_2.addWidget(self.upper_canny_label)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_6)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.segmentation_graphics_view = QtWidgets.QGraphicsView(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.segmentation_graphics_view.sizePolicy().hasHeightForWidth())
        self.segmentation_graphics_view.setSizePolicy(sizePolicy)
        self.segmentation_graphics_view.setMinimumSize(QtCore.QSize(480, 360))
        self.segmentation_graphics_view.setMaximumSize(QtCore.QSize(480, 360))
        self.segmentation_graphics_view.setStyleSheet("border-color: rgb(100, 100, 100);\n"
"border-width : 2px;\n"
"border-style:solid;")
        self.segmentation_graphics_view.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.segmentation_graphics_view.setObjectName("segmentation_graphics_view")
        self.horizontalLayout_6.addWidget(self.segmentation_graphics_view)
        self.graphics_view = QtWidgets.QGraphicsView(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphics_view.sizePolicy().hasHeightForWidth())
        self.graphics_view.setSizePolicy(sizePolicy)
        self.graphics_view.setMinimumSize(QtCore.QSize(480, 360))
        self.graphics_view.setMaximumSize(QtCore.QSize(480, 360))
        self.graphics_view.setStyleSheet("border-color: rgb(100, 100, 100);\n"
"border-width : 2px;\n"
"border-style:solid;")
        self.graphics_view.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.graphics_view.setObjectName("graphics_view")
        self.horizontalLayout_6.addWidget(self.graphics_view)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem6)
        self.next_push_button = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.next_push_button.sizePolicy().hasHeightForWidth())
        self.next_push_button.setSizePolicy(sizePolicy)
        self.next_push_button.setMinimumSize(QtCore.QSize(200, 30))
        self.next_push_button.setMaximumSize(QtCore.QSize(200, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.next_push_button.setFont(font)
        self.next_push_button.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(255, 255, 255);\n"
"border-color: rgb(235, 235, 235);\n"
"border-width : 2px;\n"
"border-style:solid;")
        self.next_push_button.setObjectName("next_push_button")
        self.horizontalLayout_8.addWidget(self.next_push_button)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem7)
        self.conclude_push_button = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.conclude_push_button.sizePolicy().hasHeightForWidth())
        self.conclude_push_button.setSizePolicy(sizePolicy)
        self.conclude_push_button.setMinimumSize(QtCore.QSize(200, 30))
        self.conclude_push_button.setMaximumSize(QtCore.QSize(200, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.conclude_push_button.setFont(font)
        self.conclude_push_button.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(255, 255, 255);\n"
"border-color: rgb(235, 235, 235);\n"
"border-width : 2px;\n"
"border-style:solid;")
        self.conclude_push_button.setObjectName("conclude_push_button")
        self.horizontalLayout_8.addWidget(self.conclude_push_button)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem8)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_33.setText(_translate("Dialog", "Configurações de segmentação da embalagem"))
        self.label_10.setText(_translate("Dialog", "Dimensões de filtro"))
        self.label_7.setText(_translate("Dialog", "Máscara gaussiana"))
        self.label_9.setText(_translate("Dialog", "Limiares Canny"))
        self.otsu_radio_button.setText(_translate("Dialog", "Otsu (automático)"))
        self.manual_radio_button.setText(_translate("Dialog", "Manual"))
        self.label.setText(_translate("Dialog", "Inferior"))
        self.lower_canny_label.setText(_translate("Dialog", "0"))
        self.label_2.setText(_translate("Dialog", "Superior"))
        self.upper_canny_label.setText(_translate("Dialog", "0"))
        self.next_push_button.setText(_translate("Dialog", "Próximo"))
        self.conclude_push_button.setText(_translate("Dialog", "Concluir"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
