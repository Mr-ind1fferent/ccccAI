import sys

from PyQt5.QtWidgets import QApplication

from ui.targetResultWin import TargetResultWin

app = QApplication(sys.argv)
win = TargetResultWin()
sys.exit(app.exec_())


