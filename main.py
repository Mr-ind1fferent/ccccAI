import sys
from PyQt5.QtWidgets import QApplication
from ui.mainWin import MainWin


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())