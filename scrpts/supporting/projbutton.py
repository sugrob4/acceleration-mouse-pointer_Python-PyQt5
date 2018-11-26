import re

from PyQt5.QtWidgets import QPushButton, QSizePolicy
from PyQt5.QtCore import Qt, QLine, QPoint, pyqtSlot
from PyQt5.QtGui import QIcon, QPainter, QPen, QColor


class ProjButton(QPushButton):

    buttonsRound = dict()

    def __init__(self, *args):
        super(ProjButton, self).__init__(*args)
        self.setCursor(Qt.PointingHandCursor)
        self.setFlat(True)
        self.setToolTip(self.text())

    def dicts(self, val):
        if val != {}:
            self.buttonsRound.update(val)

    def on_press(self):
        toolTip = self.sender().toolTip()
        if toolTip not in self.buttonsRound:
            res = self.srch(self.sender().styleSheet())
            if res in self.sender().styleSheet():
                self.setStyleSheet(
                    'background-image:url(accessory/images/{}_Active.png);'
                    'border:none;'.format(res))
            else:
                self.setStyleSheet(
                    'background-image:url(accessory/images/{}_Active.png);'
                    'border:none;'.format(res))
        else:
            self.setStyleSheet(
                'background-color:#6d1203;border:0.12em solid #747682;'
                'border-radius:35px;')
            if toolTip in self.buttonsRound:
                if toolTip == 'Settings':
                    active = self.buttonsRound['Settings'].split('.')[0]
                    self.setIcon(QIcon(active + '_Active.png'))
                else:
                    active = self.buttonsRound['About'].split('.')[0]
                    self.setIcon(QIcon(active + '_Active.png'))

    def on_release(self):
        toolTip = self.sender().toolTip()
        if toolTip not in self.buttonsRound:
            res = self.srch(self.sender().styleSheet())
            if res in self.sender().styleSheet():
                self.setStyleSheet(
                    'background-image:url(accessory/images/{}.png);'
                    'border:none;'.format(res[0:-7]))
            else:
                self.setStyleSheet(
                    'background-image:url(accessory/images/{}.png);'
                    'border:none;'.format(res[0:-7]))
        else:
            self.setStyleSheet('background-color:#930300;border-radius:35px;'
                               'border:0.12em solid #eeeff7;')
            for icn in self.buttonsRound.items():
                if toolTip == icn[0]:
                    self.setIcon(QIcon(icn[1]))

    def srch(self, value):
        res = re.search('/(.*).png', value).group(1)[7:]
        return res


class CloseButton(ProjButton):

    color = "#eeeff7"

    def __init__(self, *args):
        super(CloseButton, self).__init__(*args)
        self.resize(self.sizeHint())
        self.setMinimumSize(self.size())
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.draw_line()

    def draw_line(self):
        self.line = QLine(self.width() / 1.7, self.height() / 1.25,
                          self.width() / 6.26, self.height() / 4.5)
        self.line2 = QLine(self.width() / 1.7, self.height() / 4.5,
                           self.width() / 6.26, self.height() / 1.25)
        # self.line = QLine(QPoint(self.width() / 1.7, self.height() / 1.25),
        #                   QPoint(self.width() / 6.26, self.height() / 4.5))
        # self.line2 = QLine(QPoint(self.width() / 1.7, self.height() / 4.5),
        #                    QPoint(self.width() / 6.26, self.height() / 1.25))
        self.update()

    def enterEvent(self, enter):
        self.color = "#ab1203"

    def leaveEvent(self, leave):
        self.color = "#eeeff7"

    def paintEvent(self, ev):
        qp = QPainter()
        qp.begin(self)
        self.drawDagger(qp)
        qp.end()

    def drawDagger(self, qp):
        pen = QPen(QColor(self.color), 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLines(self.line, self.line2)

    # @pyqtSlot()
    # def on_press(self):
    #     print('button pressed')


