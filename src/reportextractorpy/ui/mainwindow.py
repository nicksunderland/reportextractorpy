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

    def __init__(self):
        super(MainWindow, self).__init__()
        self.mode = "echocardiogram"
        self.data_processor = DataProcessing(mode=self.mode)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.plain_text_edit_input.setPlainText("""the descending aorta is non dilated.\n
the descending aorta is non dilated.

test. 

aortic root non-dilated (33mm at Sov level).

non-dilated aortic root (33mm Sov level).


Mildly dilated proximal aorta (3.9cm at sinus level....
        """)
        self.web_engine_view = QWebEngineView(self.ui.centralwidget)
        self.ui.html_widget_holder_layout.addWidget(self.web_engine_view)
        self.make_connections()

    def update_web_engine_view(self, doc: Document):
        html = CustomHtmlAnnViewerSerializer.convert_to_html(doc)
        self.web_engine_view.setHtml(html)

    def make_connections(self):
        self.ui.tool_button_load.clicked.connect(self.handle_load_button_click)
        self.data_processor.load_complete_signal.connect(self.update_gui_post_load)

        self.ui.push_button_next.clicked.connect(self.handle_run_buttons_click)
        self.ui.push_button_previous.clicked.connect(self.handle_run_buttons_click)
        self.ui.spin_box_report.valueChanged.connect(self.handle_run_buttons_click)

        self.data_processor.processing_complete_signal.connect(self.update_web_engine_view)

        self.ui.radio_button_echocardiogram.toggled.connect(self.handle_mode_change)


    def handle_load_button_click(self):
        if self.ui.radio_button_load_text.isChecked():
            input_str = self.ui.plain_text_edit_input.toPlainText()
            self.data_processor.load(input_str, "string")
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

    def handle_run_buttons_click(self):
        button = self.sender().objectName()
        current_spin_box_value = self.ui.spin_box_report.value()
        if button == "push_button_next":
            if current_spin_box_value + 1 > self.ui.spin_box_report.maximum():
                self.ui.spin_box_report.blockSignals(True)
                self.ui.spin_box_report.setValue(current_spin_box_value + 1)
                self.ui.spin_box_report.blockSignals(False)
        elif button == "push_button_previous":
            if current_spin_box_value - 1 > self.ui.spin_box_report.minimum():
                self.ui.spin_box_report.blockSignals(True)
                self.ui.spin_box_report.setValue(current_spin_box_value - 1)
                self.ui.spin_box_report.blockSignals(False)
        elif button == "spin_box_report":
            pass
        else:
            print("error")
        doc_index = self.ui.spin_box_report.value() - 1
        self.data_processor.run(doc_index)

    def update_gui_post_load(self, max_value):
        # update the spinbox without emitting signals
        self.ui.spin_box_report.blockSignals(True)
        self.ui.spin_box_report.setMaximum(max_value)
        if max_value > 0:
            self.ui.spin_box_report.setMinimum(1)
            self.ui.spin_box_report.setValue(1)
        self.ui.spin_box_report.blockSignals(False)

    def handle_mode_change(self):
        if self.ui.radio_button_echocardiogram.isChecked():
            self.mode = "echocardiogram"
            self.data_processor = DataProcessing(mode=self.mode)
        elif self.ui.radio_button_cardiac_mri.isChecked():
            self.mode = "cardiac_mri"
            self.data_processor = DataProcessing(mode=self.mode)
        else:
            exit("error handling programme mode radioButtons")
