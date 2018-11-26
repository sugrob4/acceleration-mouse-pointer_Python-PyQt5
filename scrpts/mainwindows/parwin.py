# Класс главного окна

from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QGridLayout, \
    QVBoxLayout, QSizePolicy, QAction, qApp, QWidgetAction
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QRect

from scrpts.supporting.projbutton import ProjButton, CloseButton
from scrpts.mainwindows.settwin import SettWin



class ParWin(QWidget):

    # Значения и названия левой стороны кнопок
    valBut = {'Button1': 1, 'Button2': 2, 'Button3': 3}

    # Значения и названия правой стороны кнопок
    valButR = {'Button4': 4, 'Button5': 5, 'Button6': 6}

    # Файлы изображений кнопок левой и правой сторон
    pth = ['reg_button_vol1.png', 'reg_button_vol2.png',
           'reg_button_vol1.png']

    # Файлы и названия круглых кнопок посередине
    roundBtns = {"Settings": "accessory/images/button_settings.png",
                 "About": "accessory/images/button_about.png"}

    def __init__(self, parent=None, *args, **kwargs):
        super(ParWin, self).__init__(parent, *args, **kwargs)
        self.setWindowTitle('ProgramName')
        self.setStyleSheet("background-color:#32353d;")
        ProjButton().dicts(self.roundBtns)
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()
        grid = QGridLayout()
        vbox = QVBoxLayout()

        # Левый блок с кнопками
        for value, but in zip(self.valBut.items(), self.pth):
            btn = ProjButton(value[0], self)
            btn.setStyleSheet('background-image:url(accessory/images/{});'
                              'border:none;'.format(but))
            btn.setMaximumSize(240, 67)
            btn.clicked[bool].connect(self.keyPressEvent)
            btn.pressed.connect(btn.on_press)
            btn.released.connect(btn.on_release)
            grid.addWidget(btn, value[1], 0, 1, 0)
        # grid.setContentsMargins(0, 0, 60, 0)

        # Изображение мышки
        lbl = QLabel()
        pixmap = QPixmap('accessory/images/mouse_background.png')
        lbl.setMaximumSize(pixmap.size())
        lbl.setMinimumSize(
            pixmap.rect().width() / 3, pixmap.rect().height() / 5)
        lbl.setScaledContents(True)
        lbl.setPixmap(pixmap)
        lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Блок посередине круглые кнопки + изображение
        self.lst = []
        for rounds in self.roundBtns.items():
            btnRound = ProjButton('', self)
            btnRound.setToolTip(rounds[0])
            roundImg = QPixmap(rounds[1])
            roundIcn = QIcon()
            roundIcn.addPixmap(roundImg, QIcon.Normal, QIcon.Off)
            btnRound.setIcon(roundIcn)
            btnRound.setIconSize(roundImg.rect().size())
            btnRound.setStyleSheet('background-color:#930300;border-radius:35px;'
                                   'border:0.12em solid #eeeff7;')
            btnRound.setMaximumSize(70, 70)
            btnRound.setMinimumSize(btnRound.rect().size() / 2.5)
            btnRound.clicked[bool].connect(self.keyPressEvent)
            btnRound.pressed.connect(btnRound.on_press)
            btnRound.released.connect(btnRound.on_release)
            self.lst.append(btnRound)

        htopBox = QHBoxLayout()
        hbottBox = QHBoxLayout()
        htopBox.addWidget(self.lst[0])
        hbottBox.addWidget(self.lst[1])
        vbox.addLayout(htopBox)
        vbox.addWidget(lbl)
        vbox.addLayout(hbottBox)

        # Правый блок с кнопками
        gridR = QGridLayout()
        for valuer, butr in zip(self.valButR.items(), self.pth):
            btnR = ProjButton(valuer[0], self)
            btnR.setStyleSheet('background-image:url(accessory/images/{});'
                               'border:none;'.format(butr))
            btnR.setMaximumSize(240, 67)
            btnR.clicked[bool].connect(self.keyPressEvent)
            btnR.pressed.connect(btnR.on_press)
            btnR.released.connect(btnR.on_release)
            gridR.addWidget(btnR, valuer[1], 0, 1, 0)
        # gridR.setContentsMargins(60, 0, 0, 0)

        hbox.addLayout(grid)
        hbox.addLayout(vbox)
        hbox.addLayout(gridR)
        self.setLayout(hbox)

    def keyPressEvent(self, event):
        source = self.sender()
        if source.text() != '':
            for a in self.merge_dicts(self.valBut, self.valButR).items():
                if source.text() == a[0]:
                    pass
                    # print(a[1])
        else:
            if source.toolTip() == 'Settings':
                self.parent().getChildElements(SettWin())

    # Функция для объединения словарей `dict()`.
    def merge_dicts(self, first, seconde):
        a = first.copy()
        a.update(seconde)
        return a

    def showEvent(self, showev):
        if self.parent().windowFlags() & Qt.FramelessWindowHint:
            closebut = CloseButton()
            closebut.setToolTip('Close')
            closebut.setParent(self)
            closebut.move(
                self.parent().width() / 1.05,
                self.parent().height() / 32)
            closebut.show()
            closebut.clicked.connect(self.closeEvent)
        super(ParWin, self).showEvent(showev)

    def closeEvent(self, closeEv):
        self.parent().close()
