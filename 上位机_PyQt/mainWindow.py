# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(724, 728)
        font = QtGui.QFont()
        font.setPointSize(12)
        Form.setFont(font)
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(270, 10, 221, 51))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.line = QtWidgets.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(370, 100, 20, 601))
        self.line.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line.setLineWidth(1)
        self.line.setMidLineWidth(1)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setObjectName("line")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(30, 110, 320, 240))
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap(":/res/res/load_camera.jpg"))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(30, 400, 320, 240))
        self.label_8.setText("")
        self.label_8.setPixmap(QtGui.QPixmap(":/res/res/load_camera.jpg"))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(420, 100, 270, 360))
        self.label_9.setText("")
        self.label_9.setPixmap(QtGui.QPixmap(":/res/res/draw_cube.jpg"))
        self.label_9.setObjectName("label_9")
        self.toolButton = QtWidgets.QToolButton(Form)
        self.toolButton.setGeometry(QtCore.QRect(660, 20, 37, 18))
        self.toolButton.setObjectName("toolButton")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(42, 670, 285, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.comboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout_3.addWidget(self.comboBox)
        self.pushButton_7 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_7.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setIconSize(QtCore.QSize(16, 16))
        self.pushButton_7.setObjectName("pushButton_7")
        self.horizontalLayout_3.addWidget(self.pushButton_7)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.pushButton_8 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_8.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setIconSize(QtCore.QSize(16, 16))
        self.pushButton_8.setObjectName("pushButton_8")
        self.horizontalLayout_3.addWidget(self.pushButton_8)
        self.layoutWidget1 = QtWidgets.QWidget(Form)
        self.layoutWidget1.setGeometry(QtCore.QRect(30, 80, 166, 26))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.splitter = QtWidgets.QSplitter(self.layoutWidget1)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.comboBox_2 = QtWidgets.QComboBox(self.splitter)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.horizontalLayout_7.addWidget(self.splitter)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_7.addWidget(self.pushButton)
        self.layoutWidget2 = QtWidgets.QWidget(Form)
        self.layoutWidget2.setGeometry(QtCore.QRect(31, 370, 166, 26))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.splitter_2 = QtWidgets.QSplitter(self.layoutWidget2)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.comboBox_3 = QtWidgets.QComboBox(self.splitter_2)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.horizontalLayout_8.addWidget(self.splitter_2)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_8.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(500, 660, 101, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(430, 600, 167, 22))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(603, 599, 75, 24))
        self.pushButton_4.setObjectName("pushButton_4")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(420, 490, 270, 85))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/res/res/bug.jpg"))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        self.comboBox_3.setCurrentIndex(1)
        self.pushButton_8.clicked.connect(Form.button_setpos_clicked)
        self.pushButton_7.clicked.connect(Form.button_sethsv_clicked)
        self.toolButton.clicked.connect(Form.button_tools_clicked)
        self.pushButton.clicked.connect(Form.button_loadcam1_clicked)
        self.pushButton_2.clicked.connect(Form.button_loadcam2_clicked)
        self.pushButton_3.clicked.connect(Form.button_run_clicked)
        self.pushButton_4.clicked.connect(Form.button_debug_clicked)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Rubik\'s cube Robot"))
        self.label_6.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:36pt; vertical-align:sub;\">解魔方机器人</span></p></body></html>"))
        self.toolButton.setText(_translate("Form", "..."))
        self.comboBox.setItemText(0, _translate("Form", "blue"))
        self.comboBox.setItemText(1, _translate("Form", "white"))
        self.comboBox.setItemText(2, _translate("Form", "orange"))
        self.comboBox.setItemText(3, _translate("Form", "green"))
        self.comboBox.setItemText(4, _translate("Form", "yellow"))
        self.pushButton_7.setText(_translate("Form", "set hsv"))
        self.pushButton_8.setText(_translate("Form", "set pos"))
        self.comboBox_2.setCurrentText(_translate("Form", "cam0"))
        self.comboBox_2.setItemText(0, _translate("Form", "cam0"))
        self.comboBox_2.setItemText(1, _translate("Form", "cam1"))
        self.comboBox_2.setItemText(2, _translate("Form", "cam2"))
        self.comboBox_2.setItemText(3, _translate("Form", "cam3"))
        self.comboBox_2.setItemText(4, _translate("Form", "cam4"))
        self.pushButton.setText(_translate("Form", "load cam"))
        self.comboBox_3.setItemText(0, _translate("Form", "cam0"))
        self.comboBox_3.setItemText(1, _translate("Form", "cam1"))
        self.comboBox_3.setItemText(2, _translate("Form", "cam2"))
        self.comboBox_3.setItemText(3, _translate("Form", "cam3"))
        self.comboBox_3.setItemText(4, _translate("Form", "cam4"))
        self.pushButton_2.setText(_translate("Form", "load cam"))
        self.pushButton_3.setText(_translate("Form", "run"))
        self.pushButton_4.setText(_translate("Form", "debug"))

import qrc_image_rc
