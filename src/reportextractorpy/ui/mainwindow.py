from PyQt5.QtWidgets import QMainWindow
from reportextractorpy.ui.ui_converter import UiFileConverter
from reportextractorpy.ui.ui_mainwindow import Ui_MainWindow
from reportextractorpy.data_processing import DataProcessing

UiFileConverter()  # update the UI .py files


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.mode = None  # will be initialised from GUI state
        self.data_processor = None  # will be initialised from GUI state
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.make_connections()
        self.init_from_gui_state()

    def make_connections(self):
        self.ui.pushButton.clicked.connect(self.button_pressed)
        self.ui.radioButton_echocardiogram.toggled.connect(self.handle_mode_change)

    def init_from_gui_state(self):
        self.handle_mode_change()

    def handle_mode_change(self):
        if self.ui.radioButton_echocardiogram.isChecked():
            self.mode = "echocardiogram"
        elif self.ui.radioButton_cardiac_mri.isChecked():
            self.mode = "cardiac_mri"
        else:
            exit("error handling programme mode radioButtons")

        self.data_processor = DataProcessing(mode=self.mode)

    def button_pressed(self):
        self.data_processor.run()
