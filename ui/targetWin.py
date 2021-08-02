from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QButtonGroup, QFrame, QMessageBox
from os import listdir

from ui.targetSelect import Ui_Dialog
from ui_tools.clickUsableFrame import ClickUsableFrame
from ui_tools.targetCmdExcutor import TargetCmdExecutor


class TargetWin(QDialog, Ui_Dialog):
    gotTopImages = pyqtSignal(list)

    def __init__(self, jpg_dir: str):
        super().__init__()
        self.setupUi(self)

        self.files = []
        self.jpgsDir = jpg_dir
        self.jpgPath = ''
        self.fileName = ''
        self.targetsIndex = 0
        self.topImages = []
        self.buttonGroup = QButtonGroup()
        self.btn_cancel.clicked.connect(self.close)
        self.btn_yes.clicked.connect(self.execute)
        self.show()

        self.add_items()

    def _new_scroll_area_horizontal(self):
        frame = QFrame(self.scrollAreaWidgetContents_vertical)
        self.scrollArea_horizontal = QtWidgets.QScrollArea(frame)
        self.scrollArea_horizontal.setMinimumSize(QtCore.QSize(600, 200))
        self.scrollArea_horizontal.setFrameShape(QtWidgets.QFrame.Panel)
        self.scrollArea_horizontal.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.scrollArea_horizontal.setWidgetResizable(True)
        self.scrollAreaWidgetContents_horizontal = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_horizontal.setGeometry(QtCore.QRect(0, 0, 942, 534))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents_horizontal)
        self.scrollArea_horizontal.setWidget(self.scrollAreaWidgetContents_horizontal)
        layout = QtWidgets.QGridLayout(frame)
        frame.setLayout(layout)
        layout.addWidget(QtWidgets.QLabel(self.fileName.split('_')[0]), 0, 0, 1, 1)
        layout.addWidget(self.scrollArea_horizontal, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(frame)

    def add_items(self):
        self.files = listdir(self.jpgsDir)
        # self.files.sort()
        # print(self.files)
        last_video_name = ''
        for file in self.files:
            self.fileName = file.split('/')[-1].split('.')[0]
            video_name = self.fileName.split('_')[0]
            if video_name != last_video_name:
                self._new_scroll_area_horizontal()
                last_video_name = video_name
            self._add_item(file)

    def _add_item(self, jpg_file: str):
        frame = ClickUsableFrame(self.scrollAreaWidgetContents_horizontal)
        # frame.setMinimumSize(QtCore.QSize(90, 120))
        # frame.setMaximumSize(QtCore.QSize(180, 270))
        frame.setMaximumHeight(self.scrollAreaWidgetContents_horizontal.height())
        frame.setFrameShape(QtWidgets.QFrame.Box)
        frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        frame.setMaximumWidth(100)
        gridLayout = QtWidgets.QGridLayout(frame)

        label = QtWidgets.QLabel(frame)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setMinimumHeight(70)
        gridLayout.addWidget(label, 0, 0, 1, 1)

        radioButton = QtWidgets.QRadioButton(frame)
        radioButton.setChecked(True)
        self.buttonGroup.addButton(radioButton)
        self.buttonGroup.setId(radioButton, self.targetsIndex)
        gridLayout.addWidget(radioButton, 1, 0, 1, 1)

        frame.clicked.connect(radioButton.click)

        name = self.fileName.split('_')[1]
        radioButton.setText(name)

        # pixmap = QPixmap(self.jpgsDir + jpg_file)
        # print(pixmap.size()
        label.setPixmap(QPixmap(self.jpgsDir + jpg_file).scaledToHeight(label.height()))

        self.horizontalLayout.addWidget(frame)
        self.targetsIndex += 1

    def execute(self):
        index = self.buttonGroup.checkedId()

        order = ('python'
                 ' reid.py'
                 ' --mode vis'
                 ' --query_image ' + self.jpgsDir + self.files[index] +
                 ' --weight model_450.pdparams'
                 ' --confidence ' + str(self.doubleSpinBox.value()))
        self.btn_yes.setEnabled(False)
        self.btn_cancel.setEnabled(False)
        # return
        executor = TargetCmdExecutor(order)
        executor.finished.connect(self.on_finished)
        executor.gotTopImg.connect(self.on_got_result)
        executor.gotAllResults.connect(self.on_got_all_results)
        executor.start()
        self.lbl_msg.setText('正在处理...')

    def on_finished(self):
        self.lbl_msg.setText('已完成！')
        self.btn_yes.setEnabled(True)
        self.btn_cancel.setEnabled(True)

    def on_got_result(self, img_path: str):
        print('匹配:'+img_path)
        self.topImages.append(img_path)

    def on_got_all_results(self):
        self.gotTopImages.emit(self.topImages)
