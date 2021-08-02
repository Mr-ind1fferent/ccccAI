import subprocess
import threading

from PyQt5.QtCore import pyqtSignal, QObject


class TargetCmdExecutor(threading.Thread, QObject):
    finished = pyqtSignal()
    gotTopImg = pyqtSignal(str)
    gotAllResults = pyqtSignal()

    def __init__(self, order: str):
        threading.Thread.__init__(self)
        QObject.__init__(self)
        self._isExecuting = False
        # order = 'E:/Code/PaddleDetection/venv/Scripts/python.exe test/test.py'
        print(order)
        self.order = order
        self.cmd = subprocess.Popen(self.order, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.isReceiveTopImgs = False

    def run(self) -> None:

        self._isExecuting = True

        for i in iter(self.cmd.stdout.readline, 'b'):
            if not i:
                break

            try:
                msg = i.decode('utf8')
                print(msg)
            except UnicodeDecodeError:
                print('DECODE ERROR')
                continue

            if 'Top images' in msg:
                self.finished.emit()
                self.isReceiveTopImgs = True
            elif self.isReceiveTopImgs:
                if '.jpg' in msg:
                    self.gotTopImg.emit(msg)
                elif 'result saved' in msg:
                    self.gotAllResults.emit()
                else:
                    self.isReceiveTopImgs = False

        for i in iter(self.cmd.stdout.readline, 'b'):
            if not i:
                break
            try:
                msg = i.decode('utf8')
                print(msg)
            except UnicodeDecodeError:
                print('DECODE ERROR')
                continue

        self._isExecuting = False

    def is_executing(self):
        return self._isExecuting

    def terminate(self):
        if self.is_alive():
            print(self.getName(), "命令行终止...")
            self.cmd.terminate()
