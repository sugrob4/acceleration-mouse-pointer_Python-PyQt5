from PyQt5.QtCore import pyqtSignal, QObject, pyqtProperty


class ProjProperty(QObject):
    def __init__(self, parent=None):
        super(ProjProperty, self).__init__(parent)

        self._name = str()
        self._numbers = int()
        self._objects = object()

    @pyqtProperty(str)
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @name.getter
    def name(self):
        return self._name

    @pyqtProperty(int)
    def numbers(self):
        return self._numbers

    @numbers.setter
    def numbers(self, numbers):
        self._numbers = numbers

    @numbers.getter
    def numbers(self):
        return self._numbers

    @pyqtProperty(object)
    def objects(self):
        return self._objects

    @objects.setter
    def objects(self, objects):
        self._objects = objects

    @objects.getter
    def objects(self):
        return self._objects

class ProjSignal(QObject):
    appSignal = pyqtSignal()
