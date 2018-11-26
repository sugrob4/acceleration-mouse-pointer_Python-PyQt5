import os

from PyQt5 import sip

from PyQt5.QtWidgets import QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSettings

from scrpts.mainwindows.parwin import ParWin
from scrpts.supporting.projproperty import ProjSignal


class Prog(QMainWindow):

    defaultBackground = "background-color:#32353d;"

    set_path = '{}/accessory/configfile.ini'.format(os.getcwd())

    def __init__(self, parent=None, *args, **kwargs):
        super(Prog, self).__init__(parent, *args, **kwargs)
        self.progFunc()

    def progFunc(self):
        self.resize(900, 650)
        self.setBaseSize(900, 650)
        self.setMinimumSize(600, 415)
        self.setWindowIcon(QIcon('accessory/images/icon_win.png'))

        self.getChildElements(ParWin())

        self.settings = QSettings(self.set_path, QSettings.IniFormat)

        if os.path.exists(self.set_path):
            self.readSettings()

        # self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setWindowFlags(Qt.WindowSystemMenuHint|Qt.CustomizeWindowHint)


    def getChildElements(self, *args):
        for cl in args:
            self.setCentralWidget(cl)
            self.setWindowTitle(cl.windowTitle())
            if not cl.styleSheet():
                self.setStyleSheet(self.defaultBackground)
            else:
                self.setStyleSheet("%s" % format(cl.styleSheet()))

        prevwin = self.children()[1:]
        if len(prevwin) > 1:
            sip.delete(prevwin[0])

    def getPrevious(self, args):
        self.setCentralWidget(ParWin())
        self.setWindowTitle(ParWin().windowTitle())
        sip.delete(args)

    def closeEvent(self, event):
        if self.close():
            self.writeSettings()
            event.accept()
        else:
            event.ignore()
        super(Prog, self).closeEvent(event)

    def writeSettings(self):
        self.settings.beginGroup('WindowValues')
        self.settings.setValue('geometry', self.saveGeometry())
        self.settings.setValue('state', self.windowState())
        self.settings.endGroup()

    def readSettings(self):
        geometry = self.settings.value('WindowValues/geometry')
        state = self.settings.value('WindowValues/state')
        checkstate = self.settings.value('checkstate')

        if checkstate == str(0):
            self.setWindowFlags(Qt.FramelessWindowHint)

        if state == str(2):
            self.setWindowState(Qt.WindowMaximized)

        if not geometry:
            self.resize(self.baseSize())
        else:
            self.restoreGeometry(geometry)

    def clickBox(self, state):
        if state == 0:
            self.setWindowFlags(Qt.FramelessWindowHint)
        else:
            self.setWindowFlags(Qt.Window)
        self.show()
        self.settings.setValue('checkstate', state)

    def mousePressEvent(self, evmouse):
        if self.windowFlags() & Qt.FramelessWindowHint:
            if evmouse.buttons() == Qt.LeftButton:
                self.dragPos = evmouse.globalPos()
                evmouse.accept()

    def mouseMoveEvent(self, evmouse):
        if self.windowFlags() & Qt.FramelessWindowHint:
            if evmouse.buttons() == Qt.LeftButton:
                self.move(self.pos() + evmouse.globalPos() - self.dragPos)
                self.dragPos = evmouse.globalPos()
                evmouse.accept()
