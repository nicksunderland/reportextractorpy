from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtCore
from reportextractorpy.ui.ui_converter import UiFileConverter
from reportextractorpy.ui.ui_mainwindow import Ui_MainWindow
from reportextractorpy.data_processing import DataProcessing
from reportextractorpy.ui.custom_htmlannviewer import CustomHtmlAnnViewerSerializer
from gatenlp.document import Document
from typing import List

UiFileConverter()  # update the UI .py files


class MainWindow(QMainWindow):
    # signals
    load_data_signal = QtCore.pyqtSignal(str, str)  # data_processor.load(self, input_str: str, option: str):
    run_signal = QtCore.pyqtSignal(list)  # List[int]: list of report indices to run
    run_all_signal = QtCore.pyqtSignal()  # uses run()'s default parameter "all"

    def __init__(self):
        super(MainWindow, self).__init__()
        self.mode = "echocardiogram"
        self.data_processor = DataProcessing(mode=self.mode)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.plain_text_edit_input.setPlainText("""sov 3cm/m2 test. 11st. 6 feet 5. 8st. 7. 6 feet prox. asc. aorta tall. sov 3-4cm^2 test. Thie is 1/4 of. This is 30 by 23mm""")

        # 2020 / 10 / 10
        # 3 / 4 / 2019
        # 03 / 10
        # 10 - 2020
        # 34 / 40
        # weeks
        # 1 / 4
        # height
        # 123
        # cm.
        # height
        # 5
        # ' 6"
        # weight
        # 67
        # kg
        # weight
        # 5
        # stone
        # 6
        # pounds
        # sov
        # 3.1
        # cm.
        # testing
        # prox.asc.ao.
        # 3.5 - 4.5
        # cm, some
        # more
        # sentence.
        # sov
        # 3.5
        # 4.5
        # cm.sinus
        # of
        # valsalva.dog123.
        # 5.6, 66.56, 1 ^ 5, 4e5

        self.web_engine_view = QWebEngineView(self.ui.centralwidget)
        self.ui.html_widget_holder_layout.addWidget(self.web_engine_view)
        self.make_connections()

    def update_web_engine_view(self, doc: Document):
        html = CustomHtmlAnnViewerSerializer.convert_to_html(doc)
        self.web_engine_view.setHtml(html)

    def make_connections(self):
        self.ui.push_button_next.clicked.connect(self.handle_run_buttons_click)
        self.ui.push_button_previous.clicked.connect(self.handle_run_buttons_click)
        self.ui.spin_box_report.valueChanged.connect(self.handle_run_buttons_click)
        self.ui.push_button_all.clicked.connect(self.handle_run_all_button_click)
        self.ui.tool_button_load.clicked.connect(self.handle_load_button_click)
        self.ui.radio_button_echocardiogram.toggled.connect(self.handle_mode_change)
        self.data_processor.processing_complete_signal.connect(self.update_web_engine_view)
        self.load_data_signal.connect(self.data_processor.load)
        self.data_processor.load_complete_signal.connect(self.update_spin_box_post_load)
        self.run_signal.connect(self.data_processor.run)
        self.run_all_signal.connect(self.data_processor.run)

    def handle_run_buttons_click(self):
        button = self.sender().objectName()
        current_spin_box_value = self.ui.spin_box_report.value()
        if button == "push_button_next":
            self.ui.spin_box_report.setValue(current_spin_box_value + 1)
        elif button == "push_button_previous":
            self.ui.spin_box_report.setValue(current_spin_box_value - 1)
        elif button == "spin_box_report":
            self.run_signal.emit([current_spin_box_value - 1])  # indexed 0 values
        else:
            print("error")

    def update_spin_box_post_load(self, max_value):
        self.ui.spin_box_report.setMaximum(max_value)
        if max_value > 0:
            self.ui.spin_box_report.setMinimum(1)
            self.ui.spin_box_report.setValue(1)  # change will emit signal

    def handle_run_all_button_click(self):
        self.run_all_signal.emit()

    def handle_load_button_click(self):
        if self.ui.radio_button_load_text.isChecked():
            input_str = self.ui.plain_text_edit_input.toPlainText()
            self.load_data_signal.emit(input_str, "string")
        else:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                      "All Files (*);;Python Files (*.py)", options=options)
            if fileName:
                print(fileName)
        #     self.ui.radio_button_load_csv.isChecked():
        #     pass  # TODO: launch filedialogue
        # elif self.ui.radio_button_load_dir.isChecked():
        #     pass  # TODO: launch filedialogue

    def handle_mode_change(self):
        if self.ui.radio_button_echocardiogram.isChecked():
            self.mode = "echocardiogram"
            self.data_processor = DataProcessing(mode=self.mode)
        elif self.ui.radio_button_cardiac_mri.isChecked():
            self.mode = "cardiac_mri"
            self.data_processor = DataProcessing(mode=self.mode)
        else:
            exit("error handling programme mode radioButtons")
