import os

from functools import partial

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, \
    QCheckBox, QSizePolicy, qApp, QDialog, QDialogButtonBox, QLabel
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from PyQt5.QtCore import QRect, Qt

from scrpts.supporting.projbutton import ProjButton, CloseButton
from scrpts.supporting.appdetails import getPar, launch_webbrowser

class SettWin(QWidget):

    listnames = ['Программа настройки',
                 'Восстановить настройки указателя по умолчанию',
                 'Посетить сайт', 'Сбросить настройки программы',
                 'Системная рамка окна утилиты']

    strtolist = 'Посетить сайт разработчика и автора программы, ' \
                'для получения дополнительной информации.'

    captions = ['Выполнить', 'Перейти', 'Сброс']

    def __init__(self, parent=None, *args, **kwargs):
        super(SettWin, self).__init__(parent, *args, **kwargs)
        self.setWindowTitle('Settings')
        self.getsettUI()

    def getsettUI(self):
        vbx = QVBoxLayout(self)
        self.grid = QGridLayout()
        self.hbox = QHBoxLayout()

        closeBtn = CloseButton()
        closeBtn.clicked.connect(lambda: self.parent().getPrevious(self))
        self.hbox.addWidget(closeBtn)
        self.btnh = closeBtn.sizeHint()

        vbx.addLayout(self.hbox)

        self.boxbuttons = QVBoxLayout()

        for caption in range(len(self.captions)):
            setBtns = ProjButton(self.captions[caption])
            setBtns.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            background = ['#eeeff7', '#9aa9d5']
            backimage = str('set_button2')

            if caption == 1:
                background = ['#4f587d', '#304563']
                backimage = 'set_button1'

            setBtns.setStyleSheet('''
                QPushButton{
                    background:%s url(accessory/images/%s.png);
                    border-radius:18px;background-repeat:no-repeat;
                    background-position:left;background-origin:content;
                    padding-left:0.4em;font:bold 12px;color:#2b2e36;
                }
                QPushButton::pressed{
                    background:%s url(accessory/images/%s_Active.png);
                    background-repeat:no-repeat;
                    background-position:left;
                }''' % (background[0], backimage, background[1], backimage))

            setBtns.setMaximumSize(170, 42)
            setBtns.setMinimumSize(setBtns.size())
            setBtns.clicked.connect(partial(self.getvalBtns, caption))
            self.boxbuttons.addWidget(setBtns)

        setcheckn = QCheckBox()
        """Проверка на существование обозначения, в файле настроек,
            программы `configfile.ini`"""
        checkstate = getPar().settings.value('checkstate')
        if checkstate is not None:
            setcheckn.setCheckState(int(checkstate))
        else:
            setcheckn.setCheckState(Qt.Checked)

        setcheckn.setCursor(Qt.PointingHandCursor)
        setcheckn.setStyleSheet("""
            QCheckBox::indicator{
                background-color:#eeeff7;
                border:3px solid #4f587d;
                width:20px;height:20px;
            }
            QCheckBox::indicator:checked{
                image:url(accessory/images/check.png);
            }""")
        setcheckn.resize(20,20)
        setcheckn.setMinimumSize(setcheckn.size())
        setcheckn.stateChanged.connect(getPar().clickBox)
        self.boxbuttons.addWidget(setcheckn, 1, Qt.AlignHCenter)

        self.boxbuttons.setSpacing(30)
        vbx.addLayout(self.boxbuttons)
        self.setLayout(vbx)

    def getvalBtns(self, val):
        if val == 0:

            dlg = QDialog(self, Qt.Dialog |
                          Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
            dlg.setStyleSheet('''background-color:#81848c;''')
            dlg.resize(dlg.width() * 2.5, dlg.height() * 3.2)

            buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
            buttonBox.setCursor(Qt.PointingHandCursor)
            buttonBox.setStyleSheet('''
                QPushButton{
                    background-color:#585b63;font-size:13px;
                    border:1px solid #21242c;padding:0.2em 0;
                    width:60px;
                }
                QPushButton::pressed{
                    background-color:#76798e;color:#ffffff;
                    border-color:#a3a6bb;
                }''')

            buttonBox.setCenterButtons(True)
            buttonBox.accepted.connect(dlg.close)

            lbl = QLabel('Системные настройки указателя востнановленны.')
            lbl.setAlignment(Qt.AlignCenter)
            fnt = QFont('Helvetica, Arial, sans-serif', 10)
            fnt.setBold(True)
            lbl.setFont(fnt)
            lbl.setWordWrap(True)

            vlayout = QVBoxLayout()
            vlayout.addWidget(lbl)
            vlayout.addWidget(buttonBox)

            dlg.setLayout(vlayout)
            dlg.exec_()
        elif val == 1:
            launch_webbrowser('https://pcompstart.com/')
        elif val == 2:
            # QDialog - контейнер для кнопок
            dlg = QDialog(self, Qt.Dialog |
                          Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
            dlg.setStyleSheet('''background-color:#81848c;''')
            dlg.resize(dlg.width() * 2.5, dlg.height() * 3.2)

            """`ProjButton` создание кнопки для преврашения
                в последующее пустое место, между кнопками в
                `QDialogButtonBox`"""
            projbutton = ProjButton('')

            # `QDialogButtonBox` - кнопки `Reset` и `Cancel`
            buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel)
            buttonBox.addButton('Reset', QDialogButtonBox.AcceptRole)
            buttonBox.addButton(projbutton, QDialogButtonBox.ActionRole)
            buttonBox.setCursor(Qt.PointingHandCursor)
            buttonBox.setStyleSheet('''
                QPushButton{
                    background-color:#585b63;font-size:13px;
                    border:1px solid #21242c;padding:0.2em 0;
                    width:60px;
                }
                QPushButton::pressed{
                    background-color:#76798e;color:#ffffff;
                    border-color:#a3a6bb;
                }''')

            projbutton.setCursor(Qt.ArrowCursor)
            projbutton.setStyleSheet('''
                background:transparent;border:transparent;
                width:20px;''')

            buttonBox.setCenterButtons(True)
            buttonBox.accepted.connect(self.on_quit)
            buttonBox.rejected.connect(dlg.close)

            lbl = QLabel('После сброса, требуется перезапустить программу.')
            lbl.setAlignment(Qt.AlignCenter)
            fnt = QFont('Helvetica, Arial, sans-serif', 10)
            fnt.setBold(True)
            lbl.setFont(fnt)
            lbl.setWordWrap(True)

            vlayout = QVBoxLayout()
            vlayout.addWidget(lbl)
            vlayout.addWidget(buttonBox)

            dlg.setLayout(vlayout)
            dlg.exec_()

    def resizeEvent(self, event):
        # self.evh отступ 50 px от верха окна
        parheight = event.size().height()
        parwidth = event.size().width()
        self.evh = parheight / 13
        ymarg = (self.evh / 2) - (self.btnh.height() / 2)
        xmarg = (self.width() - self.btnh.width()) / 1.01
        self.hbox.setGeometry(QRect(
            xmarg, ymarg, self.btnh.width(), self.btnh.height()))

        self.boxbuttons.setGeometry(QRect(
            parwidth / 1.4, parheight / 40,
            190, parheight))

    # def closeEvent(self, closeEv):
    #     print(qApp.children())
    #     closeEv.ignore()


    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        pen = QPen(QColor('#eeeff7'), 2, Qt.SolidLine)
        qp.setPen(pen)

        font = QFont('Arial', 19)
        qp.setFont(font)

        # first - растояние первой линии от верха
        first = self.evh
        qp.drawLine(self.x(), first, self.width(), first)

        # Отрисовка главного заголовка настроек
        # Функция возвращающая верхнюю середину ширины окна для подзаголовка
        def getPosxTitle(name):
            wn = qp.fontMetrics().width(name)
            return (self.width() / 2) - (wn / 2)

        pos_x_title = getPosxTitle(self.listnames[0])

        # Условие описания уменьшения названия при уменьшении высоты
        if self.height() < self.parent().baseSize().height():
            fontsize = (first - font.pointSizeF()) / 1.6
            if self.height() <= 550:
                fontsize = 14

            font.setPointSizeF(fontsize)
            qp.setFont(font)
            pos_x_title = getPosxTitle(self.listnames[0])

        qp.drawText(pos_x_title, first / 1.55, self.listnames[0])

        # distance = 150 дистанция между остальными линиями
        distance = (self.height() - first) / 4
        i = 0
        '''leftIndent - маштабируемый отступ от левой стороны окна,
            для названий категорий настроек'''
        leftIndent = qp.viewport().width() / 9

        while first < self.height() and i < len(self.listnames[1:]):
            first += distance
            i += 1
            qp.setPen(QColor('#9fcdd0'))
            font.setPointSize(16)

            # ширина квадрата в котором написано название категории
            # widthrect = 240
            widthrect = 240

            # размер маленького шрифта
            smallfnt = 10

            if self.height() < self.parent().baseSize().height():
                if self.height() <= 550:
                    font.setPointSize(13)
                    widthrect = 220
                    smallfnt = 8
                else:
                    font.setPointSizeF(distance / font.pointSizeF() * 1.72)
            qp.setFont(font)

            # posvcen - вычисление маштабируемого отступа по выстое
            posvcen = lambda a: distance / a + qp.fontMetrics().height()
            if i == 2:
                qp.drawText(
                    leftIndent - 5, first - posvcen(1.55), widthrect, distance / 2,
                    Qt.TextWordWrap | Qt.AlignHCenter|Qt.AA_EnableHighDpiScaling, self.listnames[i])

                qp.setPen(QColor('#eeeff7'))
                # font.setPointSize(smallfnt)
                font.setPointSize(smallfnt)
                font.setItalic(True)
                qp.setFont(font)
                qp.drawText(
                    leftIndent, first - posvcen(2.15), 230, distance / 2,
                    Qt.TextWordWrap | Qt.AlignHCenter|Qt.AA_EnableHighDpiScaling, self.strtolist)
            else:
                font.setItalic(False)
                qp.setFont(font)
                qp.drawText(
                    leftIndent, first - posvcen(2), widthrect, distance / 2,
                    Qt.TextWordWrap | Qt.AlignHCenter|Qt.AA_EnableHighDpiScaling, self.listnames[i])
            # отрисовка линий
            if first >= self.height():
                continue
            else:
                qp.setPen(pen)
                qp.drawLine(self.rect().x(), first, self.width(), first)

    def on_quit(self):
        confpath = '{}/accessory/configfile.ini'.format(os.getcwd())
        if os.path.exists(confpath):
            os.remove(confpath)
        qApp.quit()
