from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFrame


class ClickUsableFrame(QFrame):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.clicked.emit()
