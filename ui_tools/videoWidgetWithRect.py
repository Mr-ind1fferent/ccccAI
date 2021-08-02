from PyQt5.QtCore import QRect, Qt, QSize
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtMultimediaWidgets import QVideoWidget


class VideoWidgetWithRect(QVideoWidget):
    anchorX = 0
    anchorY = 0
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    isMoving = False
    FrameSize = QSize(0, 0)

    # 鼠标点击事件
    def mousePressEvent(self, event):
        self.isMoving = True
        self.x0 = event.x()
        self.y0 = event.y()
        # self.draw_rectangle([event.x(), event.y()], [event.x()+30, event.y()+30])

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):
        print(event.x(), event.y())
        self.isMoving = False

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        if self.isMoving:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()

    # 绘制事件
    def paintEvent(self, event):
        super().paintEvent(event)
        print('draw:{}{}{}{}'.format(self.x0, self.y0, (self.x1 - self.x0), (self.y1 - self.y0)))
        rect = QRect(self.x0, self.y0, (self.x1 - self.x0), (self.y1 - self.y0))
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.drawRect(rect)

    def update_aspect_ratio(self, size: QSize):
        self.FrameSize = size
        self.update_anchor()

    def update_anchor(self):
        self.anchorX = round((self.width()-self.FrameSize.width()/self.FrameSize.height()*self.height())/2)
        self.anchorY = round((self.height()-self.FrameSize.height()/self.FrameSize.width()*self.width())/2)
        if self.anchorX < 0:
            self.anchorX = 0
        if self.anchorY < 0:
            self.anchorY = 0
        print("横向锚点:{} 纵向锚点:{}".format(self.anchorX, self.anchorY))

    def draw_rectangle(self, start: list, end: list):
        self.update_anchor()
        self.x0 = self.anchorX+start[0]
        self.y0 = self.anchorY+start[1]
        self.x1 = self.anchorX+end[0]
        self.y1 = self.anchorY+end[1]
        self.update()
