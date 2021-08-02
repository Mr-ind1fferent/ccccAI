import subprocess
import threading

from PyQt5.QtCore import pyqtSignal, QObject


class TrackCmdExecutor(threading.Thread, QObject):
    startedTrack = pyqtSignal()
    gotFrameCount = pyqtSignal(int)
    gotTempImg = pyqtSignal()
    updateProgress = pyqtSignal(int)
    finishedTrack = pyqtSignal()
    savedVideo = pyqtSignal()

    def __init__(self, order: str, thread_lock: threading.Lock):
        threading.Thread.__init__(self)
        QObject.__init__(self)
        print(order)
        self.order = order
        self.threadLock = thread_lock
        self._isExecuting = False
        self.cmd = subprocess.Popen(self.order, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.trackedFrame = 0
        self.frameCount = 999999

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

            if msg[:10] == 'temp_image':
                self.trackedFrame += 1
                self.gotTempImg.emit()
                self.updateProgress.emit(int(self.trackedFrame / self.frameCount * 100))
            elif msg[0] == '[':
                # if 'Processing frame' in msg:
                #     self.updateProgress.emit(int(msg.split()[-3]) / self.frameCount * 100)
                if 'Length of' in msg:
                    self.frameCount = int(msg.split()[-2])
                    self.gotFrameCount.emit(self.frameCount)
                elif 'MOT results' in msg:
                    self.finishedTrack.emit()
                elif 'Save video' in msg:
                    self.savedVideo.emit()
                elif 'Starting tracking' in msg:
                    self.startedTrack.emit()

        self._isExecuting = False

    def is_executing(self):
        return self._isExecuting

    def terminate(self):
        if self.is_alive():
            if self.threadLock.locked():
                self.threadLock.release()
            print(self.getName(), "命令行终止...")
            self.cmd.terminate()
