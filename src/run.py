import sys
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon, QPixmap
from reportextractorpy.utils import Utils
from os import path
from PyQt5.QtWidgets import QApplication
from reportextractorpy.ui import mainwindow

if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(QPixmap(path.join(Utils.ui_resources_path(), "main_icon_512.png"))))
    w = mainwindow.MainWindow()
    w.show()
    app.exec()



