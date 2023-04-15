import os


class UiFileConverter:

    def __init__(self):
        print("(re-)converting all QtCreator .ui files to .py files")

        os.system("pyuic5 ReportExtractor/ui/ui_mainwindow.ui > ReportExtractor/ui/ui_mainwindow.py")
