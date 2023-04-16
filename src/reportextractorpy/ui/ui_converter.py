import os


class UiFileConverter:

    def __init__(self):
        print("(re-)converting all QtCreator .ui files to .py files")

        os.system("pyuic5 reportextractorpy/ui/ui_mainwindow.ui > reportextractorpy/ui/ui_mainwindow.py")
