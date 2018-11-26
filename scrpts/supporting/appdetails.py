from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl

from scrpts import prog


def getPar():
    topWidget = QApplication.topLevelWidgets()
    for p in topWidget:
        if type(p) is prog.Prog:
            return p

def launch_webbrowser(url):
    QDesktopServices.openUrl(
        QUrl(url))
