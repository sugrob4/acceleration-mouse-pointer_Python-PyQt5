#!/usr/bin/python3
#-*- coding: utf-8 -*-

import sys
import traceback

from PyQt5.QtWidgets import QApplication, QDesktopWidget, QErrorMessage
from PyQt5.QtCore import Qt

from scrpts.prog import Prog

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setApplicationName('Program name')
    app.setOrganizationName('pcompstart')
    app.setOrganizationDomain('pcompstart.com')
    prg = Prog()
    try:
        prg.show()
        app.exec_()
    except Exception as err:
        QErrorMessage.showMessage(
            traceback.format_exc(*sys.exc_info()), err)
        sys.exit(1)
