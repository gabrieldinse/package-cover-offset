# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\gabri\Desktop\projeto_especializado\Projeto_Especializado\src\Windows\UI\\main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(800, 800))
        MainWindow.setMaximumSize(QtCore.QSize(800, 800))
        MainWindow.setStyleSheet("background-color: rgb(245, 245, 245);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_33 = QtWidgets.QLabel(self.centralwidget)
        self.label_33.setGeometry(QtCore.QRect(20, 10, 711, 29))
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
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(100, 60, 300, 26))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setMinimumSize(QtCore.QSize(300, 0))
        self.label_12.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("background-color: rgb(235, 235, 235);\n"
"color: rgb(50, 50, 50);\n"
"border-color: rgb(100, 100, 100);\n"
"border-width : 2px;\n"
"border-style:solid;")
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.register_product_push_button = QtWidgets.QPushButton(self.centralwidget)
        self.register_product_push_button.setEnabled(False)
        self.register_product_push_button.setGeometry(QtCore.QRect(100, 140, 150, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.register_product_push_button.sizePolicy().hasHeightForWidth())
        self.register_product_push_button.setSizePolicy(sizePolicy)
        self.register_product_push_button.setMinimumSize(QtCore.QSize(150, 30))
        self.register_product_push_button.setMaximumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.register_product_push_button.setFont(font)
        self.register_product_push_button.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(255, 255, 255);\n"
"border-color: rgb(235, 235, 235);\n"
"border-width : 2px;\n"
"border-style:solid;")
        self.register_product_push_button.setObjectName("register_product_push_button")
        self.edit_product_push_button = QtWidgets.QPushButton(self.centralwidget)
        self.edit_product_push_button.setEnabled(False)
        self.edit_product_push_button.setGeometry(QtCore.QRect(250, 140, 150, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edit_product_push_button.sizePolicy().hasHeightForWidth())
        self.edit_product_push_button.setSizePolicy(sizePolicy)
        self.edit_product_push_button.setMinimumSize(QtCore.QSize(150, 30))
        self.edit_product_push_button.setMaximumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.edit_product_push_button.setFont(font)
        self.edit_product_push_button.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(255, 255, 255);\n"
"border-color: rgb(235, 235, 235);\n"
"border-width : 2px;\n"
"border-style:solid;")
        self.edit_product_push_button.setObjectName("edit_product_push_button")
        self.test_push_button = QtWidgets.QPushButton(self.centralwidget)
        self.test_push_button.setEnabled(False)
        self.test_push_button.setGeometry(QtCore.QRect(100, 180, 150, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.test_push_button.sizePolicy().hasHeightForWidth())
        self.test_push_button.setSizePolicy(sizePolicy)
        self.test_push_button.setMinimumSize(QtCore.QSize(150, 30))
        self.test_push_button.setMaximumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.test_push_button.setFont(font)
        self.test_push_button.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(255, 255, 255);\n"
"border-color: rgb(235, 235, 235);\n"
"border-width : 2px;\n"
"border-style:solid;")
        self.test_push_button.setObjectName("test_push_button")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 60, 71, 220))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_20.setSpacing(0)
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.label_31 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(30)
        sizePolicy.setHeightForWidth(self.label_31.sizePolicy().hasHeightForWidth())
        self.label_31.setSizePolicy(sizePolicy)
        self.label_31.setMinimumSize(QtCore.QSize(0, 30))
        self.label_31.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_31.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_31.setFont(font)
        self.label_31.setStyleSheet("background-color: rgb(235, 235, 235);\n"
"color: rgb(50, 50, 50);\n"
"border-color: rgb(100, 100, 100);\n"
"border-width : 2px;\n"
"border-style:solid;")
        self.label_31.setTextFormat(QtCore.Qt.AutoText)
        self.label_31.setScaledContents(False)
        self.label_31.setAlignment(QtCore.Qt.AlignCenter)
        self.label_31.setWordWrap(False)
        self.label_31.setObjectName("label_31")
        self.verticalLayout_20.addWidget(self.label_31)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_20.addItem(spacerItem)
        self.vision_state_label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.vision_state_label.setFont(font)
        self.vision_state_label.setStyleSheet("background-color: rgb(235, 235, 235);\n"
"color: rgb(50, 50, 50);\n"
"border-color: rgb(100, 100, 100);\n"
"border-width : 2px;\n"
"border-style:solid;")
        self.vision_state_label.setAlignment(QtCore.Qt.AlignCenter)
        self.vision_state_label.setObjectName("vision_state_label")
        self.verticalLayout_20.addWidget(self.vision_state_label)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_20.addItem(spacerItem1)
        self.stop_vision_push_button = QtWidgets.QPushButton(self.layoutWidget)
        self.stop_vision_push_button.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stop_vision_push_button.sizePolicy().hasHeightForWidth())
        self.stop_vision_push_button.setSizePolicy(sizePolicy)
        self.stop_vision_push_button.setMaximumSize(QtCore.QSize(999999, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.stop_vision_push_button.setFont(font)
        self.stop_vision_push_button.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(255, 255, 255);\n"
"border-color: rgb(235, 235, 235);\n"
"border-width : 2px;\n"
"border-style:solid;")
        self.stop_vision_push_button.setObjectName("stop_vision_push_button")
        self.verticalLayout_20.addWidget(self.stop_vision_push_button)
        self.start_vision_push_button = QtWidgets.QPushButton(self.layoutWidget)
        self.start_vision_push_button.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start_vision_push_button.sizePolicy().hasHeightForWidth())
        self.start_vision_push_button.setSizePolicy(sizePolicy)
        self.start_vision_push_button.setMaximumSize(QtCore.QSize(99999, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.start_vision_push_button.setFont(font)
        self.start_vision_push_button.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(255, 255, 255);\n"
"border-color: rgb(235, 235, 235);\n"
"border-width : 2px;\n"
"border-style:solid;")
        self.start_vision_push_button.setObjectName("start_vision_push_button")
        self.verticalLayout_20.addWidget(self.start_vision_push_button)
        spacerItem2 = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_20.addItem(spacerItem2)
        self.product_type_combo_box = QtWidgets.QComboBox(self.centralwidget)
        self.product_type_combo_box.setEnabled(False)
        self.product_type_combo_box.setGeometry(QtCore.QRect(100, 100, 300, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.product_type_combo_box.sizePolicy().hasHeightForWidth())
        self.product_type_combo_box.setSizePolicy(sizePolicy)
        self.product_type_combo_box.setMinimumSize(QtCore.QSize(300, 0))
        self.product_type_combo_box.setBaseSize(QtCore.QSize(0, 0))
        self.product_type_combo_box.setObjectName("product_type_combo_box")
        self.graphics_view = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphics_view.setGeometry(QtCore.QRect(250, 350, 480, 360))
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
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(410, 80, 366, 231))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_19 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.label_27 = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_27.setFont(font)
        self.label_27.setStyleSheet("color: rgb(50, 50, 50);")
        self.label_27.setAlignment(QtCore.Qt.AlignCenter)
        self.label_27.setObjectName("label_27")
        self.horizontalLayout_18.addWidget(self.label_27)
        self.last_offset_label = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.last_offset_label.sizePolicy().hasHeightForWidth())
        self.last_offset_label.setSizePolicy(sizePolicy)
        self.last_offset_label.setMinimumSize(QtCore.QSize(140, 0))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.last_offset_label.setFont(font)
        self.last_offset_label.setStyleSheet("color: rgb(50, 50, 50);\n"
"")
        self.last_offset_label.setObjectName("last_offset_label")
        self.horizontalLayout_18.addWidget(self.last_offset_label)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_18.addItem(spacerItem3)
        self.verticalLayout_15.addLayout(self.horizontalLayout_18)
        self.verticalLayout_17.addLayout(self.verticalLayout_15)
        self.horizontalLayout_21.addLayout(self.verticalLayout_17)
        self.verticalLayout_19.addLayout(self.horizontalLayout_21)
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout()
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout()
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.label_28 = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_28.setFont(font)
        self.label_28.setStyleSheet("color: rgb(50, 50, 50);")
        self.label_28.setAlignment(QtCore.Qt.AlignCenter)
        self.label_28.setObjectName("label_28")
        self.horizontalLayout_19.addWidget(self.label_28)
        self.average_offset_label = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.average_offset_label.sizePolicy().hasHeightForWidth())
        self.average_offset_label.setSizePolicy(sizePolicy)
        self.average_offset_label.setMinimumSize(QtCore.QSize(140, 0))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.average_offset_label.setFont(font)
        self.average_offset_label.setStyleSheet("color: rgb(50, 50, 50);\n"
"")
        self.average_offset_label.setObjectName("average_offset_label")
        self.horizontalLayout_19.addWidget(self.average_offset_label)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_19.addItem(spacerItem4)
        self.verticalLayout_16.addLayout(self.horizontalLayout_19)
        self.verticalLayout_18.addLayout(self.verticalLayout_16)
        self.horizontalLayout_22.addLayout(self.verticalLayout_18)
        self.verticalLayout_19.addLayout(self.horizontalLayout_22)
        self.label_15 = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setMinimumSize(QtCore.QSize(300, 0))
        self.label_15.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("background-color: rgb(235, 235, 235);\n"
"color: rgb(50, 50, 50);\n"
"border-color: rgb(100, 100, 100);\n"
"border-width : 2px;\n"
"border-style:solid;")
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.verticalLayout_19.addWidget(self.label_15)
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.label_30 = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_30.setFont(font)
        self.label_30.setStyleSheet("color: rgb(50, 50, 50);")
        self.label_30.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_30.setObjectName("label_30")
        self.horizontalLayout_23.addWidget(self.label_30)
        self.number_of_products_label = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.number_of_products_label.sizePolicy().hasHeightForWidth())
        self.number_of_products_label.setSizePolicy(sizePolicy)
        self.number_of_products_label.setMinimumSize(QtCore.QSize(60, 0))
        self.number_of_products_label.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.number_of_products_label.setFont(font)
        self.number_of_products_label.setStyleSheet("color: rgb(50, 50, 50);\n"
"")
        self.number_of_products_label.setText("")
        self.number_of_products_label.setObjectName("number_of_products_label")
        self.horizontalLayout_23.addWidget(self.number_of_products_label)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_23.addItem(spacerItem5)
        self.verticalLayout_19.addLayout(self.horizontalLayout_23)
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.label_32 = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_32.sizePolicy().hasHeightForWidth())
        self.label_32.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_32.setFont(font)
        self.label_32.setStyleSheet("color: rgb(50, 50, 50);")
        self.label_32.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_32.setObjectName("label_32")
        self.horizontalLayout_24.addWidget(self.label_32)
        self.no_cover_products_label = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.no_cover_products_label.sizePolicy().hasHeightForWidth())
        self.no_cover_products_label.setSizePolicy(sizePolicy)
        self.no_cover_products_label.setMinimumSize(QtCore.QSize(60, 0))
        self.no_cover_products_label.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.no_cover_products_label.setFont(font)
        self.no_cover_products_label.setStyleSheet("color: rgb(50, 50, 50);\n"
"")
        self.no_cover_products_label.setText("")
        self.no_cover_products_label.setObjectName("no_cover_products_label")
        self.horizontalLayout_24.addWidget(self.no_cover_products_label)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_24.addItem(spacerItem6)
        self.verticalLayout_19.addLayout(self.horizontalLayout_24)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_19.addItem(spacerItem7)
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(410, 50, 300, 26))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setMinimumSize(QtCore.QSize(300, 0))
        self.label_13.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("background-color: rgb(235, 235, 235);\n"
"color: rgb(50, 50, 50);\n"
"border-color: rgb(100, 100, 100);\n"
"border-width : 2px;\n"
"border-style:solid;")
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.turn_on_camera_push_button = QtWidgets.QPushButton(self.centralwidget)
        self.turn_on_camera_push_button.setGeometry(QtCore.QRect(70, 390, 150, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.turn_on_camera_push_button.sizePolicy().hasHeightForWidth())
        self.turn_on_camera_push_button.setSizePolicy(sizePolicy)
        self.turn_on_camera_push_button.setMinimumSize(QtCore.QSize(150, 30))
        self.turn_on_camera_push_button.setMaximumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.turn_on_camera_push_button.setFont(font)
        self.turn_on_camera_push_button.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(255, 255, 255);\n"
"border-color: rgb(235, 235, 235);\n"
"border-width : 2px;\n"
"border-style:solid;")
        self.turn_on_camera_push_button.setObjectName("turn_on_camera_push_button")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(70, 320, 150, 26))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setMinimumSize(QtCore.QSize(150, 0))
        self.label_14.setMaximumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setStyleSheet("background-color: rgb(235, 235, 235);\n"
"color: rgb(50, 50, 50);\n"
"border-color: rgb(100, 100, 100);\n"
"border-width : 2px;\n"
"border-style:solid;")
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.turn_off_camera_push_button = QtWidgets.QPushButton(self.centralwidget)
        self.turn_off_camera_push_button.setEnabled(False)
        self.turn_off_camera_push_button.setGeometry(QtCore.QRect(70, 430, 150, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.turn_off_camera_push_button.sizePolicy().hasHeightForWidth())
        self.turn_off_camera_push_button.setSizePolicy(sizePolicy)
        self.turn_off_camera_push_button.setMinimumSize(QtCore.QSize(150, 30))
        self.turn_off_camera_push_button.setMaximumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.turn_off_camera_push_button.setFont(font)
        self.turn_off_camera_push_button.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(255, 255, 255);\n"
"border-color: rgb(235, 235, 235);\n"
"border-width : 2px;\n"
"border-style:solid;")
        self.turn_off_camera_push_button.setObjectName("turn_off_camera_push_button")
        self.camera_state_label = QtWidgets.QLabel(self.centralwidget)
        self.camera_state_label.setGeometry(QtCore.QRect(110, 360, 69, 22))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.camera_state_label.setFont(font)
        self.camera_state_label.setStyleSheet("background-color: rgb(235, 235, 235);\n"
"color: rgb(50, 50, 50);\n"
"border-color: rgb(100, 100, 100);\n"
"border-width : 2px;\n"
"border-style:solid;")
        self.camera_state_label.setAlignment(QtCore.Qt.AlignCenter)
        self.camera_state_label.setObjectName("camera_state_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_33.setText(_translate("MainWindow", "Produção de embalagens"))
        self.label_12.setText(_translate("MainWindow", "Tipo do produto"))
        self.register_product_push_button.setText(_translate("MainWindow", "Registrar novo"))
        self.edit_product_push_button.setText(_translate("MainWindow", "Editar"))
        self.test_push_button.setText(_translate("MainWindow", "Testar"))
        self.label_31.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Sistema</p></body></html>"))
        self.vision_state_label.setText(_translate("MainWindow", "OFF"))
        self.stop_vision_push_button.setText(_translate("MainWindow", "Parar"))
        self.start_vision_push_button.setText(_translate("MainWindow", "Iniciar"))
        self.label_27.setText(_translate("MainWindow", "Último (mm):"))
        self.last_offset_label.setText(_translate("MainWindow", "0"))
        self.label_28.setText(_translate("MainWindow", "Média (mm):"))
        self.average_offset_label.setText(_translate("MainWindow", "-"))
        self.label_15.setText(_translate("MainWindow", "Produtos registrados"))
        self.label_30.setText(_translate("MainWindow", "Quantidade:"))
        self.label_32.setText(_translate("MainWindow", "Sem tampa:"))
        self.label_13.setText(_translate("MainWindow", "Deslocamento da tampa"))
        self.turn_on_camera_push_button.setText(_translate("MainWindow", "Ligar"))
        self.label_14.setText(_translate("MainWindow", "Câmera"))
        self.turn_off_camera_push_button.setText(_translate("MainWindow", "Desligar"))
        self.camera_state_label.setText(_translate("MainWindow", "OFF"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
