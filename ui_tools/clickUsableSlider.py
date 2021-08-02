from PyQt5 import Qt
from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import *


class ClickUsableSlider(QSlider):
    sliderClicked = pyqtSignal(int)
    # wheelScrolled = pyqtSignal(int)

    def __init__(self, father):
        super().__init__(Qt.Horizontal, father)

    def mousePressEvent(self, event):
        super(ClickUsableSlider, self).mousePressEvent(event)
        value = event.localPos().x()
        value = round(value / self.width() * self.maximum())
        self.sliderClicked.emit(value)

    def wheelEvent(self, e):
        pass
