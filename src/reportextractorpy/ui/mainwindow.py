from PyQt5.QtWidgets import QMainWindow
from reportextractorpy.ui.ui_converter import UiFileConverter
from reportextractorpy.ui.ui_mainwindow import Ui_MainWindow
from reportextractorpy.data_processing import DataProcessing

UiFileConverter()  # update the UI .py files


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.make_connections()

    def make_connections(self):
        self.ui.pushButton.clicked.connect(self.button_pressed)

    @staticmethod
    def button_pressed():
        print("button pressed")
        DataProcessing().run()
