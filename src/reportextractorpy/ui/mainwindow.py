from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtCore
from reportextractorpy.ui.ui_converter import UiFileConverter
from reportextractorpy.ui.ui_mainwindow import Ui_MainWindow
from reportextractorpy.data_processing import DataProcessing
from reportextractorpy.ui.custom_htmlannviewer import CustomHtmlAnnViewerSerializer
from gatenlp.document import Document

UiFileConverter()  # update the UI .py files


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.mode = "echocardiogram"
        self.data_processor = DataProcessing(mode=self.mode)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.web_engine_view = QWebEngineView(self.ui.centralwidget)
        self.ui.html_widget_holder_layout.addWidget(self.web_engine_view)
        self.init_from_gui_state()
        self.make_connections()

        self.ui.pushButton.click()  # just for developing

    def update_web_engine_view(self, doc: Document):
        html = CustomHtmlAnnViewerSerializer.convert_to_html(doc)
        self.web_engine_view.setHtml(html)

    def make_connections(self):
        self.ui.pushButton.clicked.connect(self.button_pressed)
        self.ui.radioButton_echocardiogram.toggled.connect(self.handle_mode_change)
        self.data_processor.processing_complete_signal.connect(self.update_web_engine_view)

    def init_from_gui_state(self):
        self.handle_mode_change()

    def handle_mode_change(self):
        if self.ui.radioButton_echocardiogram.isChecked():
            self.mode = "echocardiogram"
        elif self.ui.radioButton_cardiac_mri.isChecked():
            self.mode = "cardiac_mri"
        else:
            exit("error handling programme mode radioButtons")
        # update
        self.data_processor = DataProcessing(mode=self.mode)



    def button_pressed(self):
        self.data_processor.run()
