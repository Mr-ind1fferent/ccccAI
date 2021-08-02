from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog

from ui.targetResult import Ui_Dialog


class TargetResultWin(QDialog, Ui_Dialog):
    def __init__(self):
        super(TargetResultWin, self).__init__()
        self.setupUi(self)

    def add_item(self, video_name: str, person: str, image: str, time: str):
        frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frame.sizePolicy().hasHeightForWidth())
        frame.setSizePolicy(sizePolicy)
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)
        horizontal_layout = QtWidgets.QHBoxLayout(frame)

        lbl_video = QtWidgets.QLabel(frame)
        lbl_video.setText(video_name)
        horizontal_layout.addWidget(lbl_video)
        lbl_id = QtWidgets.QLabel(frame)
        lbl_id.setText(person)
        horizontal_layout.addWidget(lbl_id)
        lbl_img = QtWidgets.QLabel(frame)
        lbl_img.setPixmap(QPixmap(image))
        horizontal_layout.addWidget(lbl_img)
        lbl_frame = QtWidgets.QLabel(frame)
        lbl_frame.setText(time)
        horizontal_layout.addWidget(lbl_frame)
        self.verticalLayout.addWidget(frame)

