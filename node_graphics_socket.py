from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class NodeGraphicsSocket(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.radius = 6
        self.outline_width = 1
        self.bg_color = QColor(255, 153, 51, 255)
        self.outline_color = QColor(0, 0, 0, 255)

        self._pen = QPen(self.outline_color)
        self._pen.setWidth(self.outline_width)
        self._brush = QBrush(self.bg_color)


    def boundingRect(self):
        return QRectF(-self.radius - self.outline_width,
                      -self.radius - self.outline_width,
                      2* (self.radius + self.outline_width),
                      2* (self.radius + self.outline_width)
                      ).normalized()


    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        painter.setPen(self._pen)
        painter.setBrush(self._brush)
        painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)