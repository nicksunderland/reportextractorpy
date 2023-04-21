# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reportextractorpy/ui/ui_mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 650)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.html_widget_holder = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.html_widget_holder.sizePolicy().hasHeightForWidth())
        self.html_widget_holder.setSizePolicy(sizePolicy)
        self.html_widget_holder.setObjectName("html_widget_holder")
        self.html_widget_holder_layout = QtWidgets.QVBoxLayout(self.html_widget_holder)
        self.html_widget_holder_layout.setContentsMargins(0, 0, 0, 0)
        self.html_widget_holder_layout.setObjectName("html_widget_holder_layout")
        self.verticalLayout_4.addWidget(self.html_widget_holder)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_4.addWidget(self.line)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_report_spin_box = QtWidgets.QLabel(self.centralwidget)
        self.label_report_spin_box.setObjectName("label_report_spin_box")
        self.horizontalLayout.addWidget(self.label_report_spin_box)
        self.spin_box_report = QtWidgets.QSpinBox(self.centralwidget)
        self.spin_box_report.setMaximum(0)
        self.spin_box_report.setObjectName("spin_box_report")
        self.horizontalLayout.addWidget(self.spin_box_report)
        self.push_button_previous = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_previous.setObjectName("push_button_previous")
        self.horizontalLayout.addWidget(self.push_button_previous)
        self.push_button_next = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_next.setObjectName("push_button_next")
        self.horizontalLayout.addWidget(self.push_button_next)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.push_button_all = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_all.setObjectName("push_button_all")
        self.horizontalLayout.addWidget(self.push_button_all)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout.addWidget(self.line_3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_mode = QtWidgets.QLabel(self.centralwidget)
        self.label_mode.setObjectName("label_mode")
        self.horizontalLayout_3.addWidget(self.label_mode)
        self.groupbox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupbox.sizePolicy().hasHeightForWidth())
        self.groupbox.setSizePolicy(sizePolicy)
        self.groupbox.setObjectName("groupbox")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupbox)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.radio_button_echocardiogram = QtWidgets.QRadioButton(self.groupbox)
        self.radio_button_echocardiogram.setChecked(True)
        self.radio_button_echocardiogram.setObjectName("radio_button_echocardiogram")
        self.horizontalLayout_6.addWidget(self.radio_button_echocardiogram)
        self.radio_button_cardiac_mri = QtWidgets.QRadioButton(self.groupbox)
        self.radio_button_cardiac_mri.setEnabled(False)
        self.radio_button_cardiac_mri.setObjectName("radio_button_cardiac_mri")
        self.horizontalLayout_6.addWidget(self.radio_button_cardiac_mri)
        self.horizontalLayout_3.addWidget(self.groupbox)
        self.push_button_settings = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_settings.setObjectName("push_button_settings")
        self.horizontalLayout_3.addWidget(self.push_button_settings)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_messages = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_messages.setFont(font)
        self.label_messages.setObjectName("label_messages")
        self.horizontalLayout_2.addWidget(self.label_messages)
        self.label_message_output = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_message_output.sizePolicy().hasHeightForWidth())
        self.label_message_output.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_message_output.setFont(font)
        self.label_message_output.setText("")
        self.label_message_output.setObjectName("label_message_output")
        self.horizontalLayout_2.addWidget(self.label_message_output)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_input = QtWidgets.QLabel(self.centralwidget)
        self.label_input.setObjectName("label_input")
        self.verticalLayout.addWidget(self.label_input)
        self.input_radio_button_group = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_radio_button_group.sizePolicy().hasHeightForWidth())
        self.input_radio_button_group.setSizePolicy(sizePolicy)
        self.input_radio_button_group.setObjectName("input_radio_button_group")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.input_radio_button_group)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.radio_button_load_text = QtWidgets.QRadioButton(self.input_radio_button_group)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.radio_button_load_text.setFont(font)
        self.radio_button_load_text.setChecked(True)
        self.radio_button_load_text.setObjectName("radio_button_load_text")
        self.verticalLayout_3.addWidget(self.radio_button_load_text)
        self.radio_button_load_csv = QtWidgets.QRadioButton(self.input_radio_button_group)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.radio_button_load_csv.setFont(font)
        self.radio_button_load_csv.setObjectName("radio_button_load_csv")
        self.verticalLayout_3.addWidget(self.radio_button_load_csv)
        self.radio_button_load_dir = QtWidgets.QRadioButton(self.input_radio_button_group)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.radio_button_load_dir.setFont(font)
        self.radio_button_load_dir.setObjectName("radio_button_load_dir")
        self.verticalLayout_3.addWidget(self.radio_button_load_dir)
        self.verticalLayout.addWidget(self.input_radio_button_group)
        self.tool_button_load = QtWidgets.QToolButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.tool_button_load.setFont(font)
        self.tool_button_load.setObjectName("tool_button_load")
        self.verticalLayout.addWidget(self.tool_button_load, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.plain_text_edit_input = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plain_text_edit_input.sizePolicy().hasHeightForWidth())
        self.plain_text_edit_input.setSizePolicy(sizePolicy)
        self.plain_text_edit_input.setMinimumSize(QtCore.QSize(0, 0))
        self.plain_text_edit_input.setMaximumSize(QtCore.QSize(16777215, 130))
        self.plain_text_edit_input.setObjectName("plain_text_edit_input")
        self.horizontalLayout_4.addWidget(self.plain_text_edit_input)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ReportExtractorPy"))
        self.label_report_spin_box.setText(_translate("MainWindow", "Report:"))
        self.push_button_previous.setText(_translate("MainWindow", "Previous"))
        self.push_button_next.setText(_translate("MainWindow", "Next"))
        self.push_button_all.setText(_translate("MainWindow", "All"))
        self.label_mode.setText(_translate("MainWindow", "Mode:"))
        self.radio_button_echocardiogram.setText(_translate("MainWindow", "Echocardiogram"))
        self.radio_button_cardiac_mri.setText(_translate("MainWindow", "Cardiac MRI"))
        self.push_button_settings.setText(_translate("MainWindow", "Settings"))
        self.label_messages.setText(_translate("MainWindow", "Messages:"))
        self.label_input.setText(_translate("MainWindow", "Input:"))
        self.radio_button_load_text.setText(_translate("MainWindow", "text"))
        self.radio_button_load_csv.setText(_translate("MainWindow", "file.cvs"))
        self.radio_button_load_dir.setText(_translate("MainWindow", "dir"))
        self.tool_button_load.setText(_translate("MainWindow", "Load"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
