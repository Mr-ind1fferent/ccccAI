from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow
from ui.videoWindow import Ui_videoWindow


class VideoWin(QMainWindow, Ui_videoWindow):

    def __init__(self, vf):
        super(VideoWin, self).__init__()
        self.vf = vf
        self.setupUi(self)
        self.setWindowTitle(vf.fileName)
        self.gridLayout.addWidget(self.vf.frame)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        super(VideoWin, self).closeEvent(a0)
        self.vf.to_window()
