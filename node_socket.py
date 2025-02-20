from enum import Enum

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class SocketPosition(Enum):
    LEFT_TOP = 1
    LEFT_BOTTOM = 2
    RIGHT_TOP = 3
    RIGHT_BOTTOM = 4


class Socket(QGraphicsEllipseItem):
    def __init__(self, node, index=0, position=SocketPosition.LEFT_TOP, radius=6):
        super().__init__(0, 0, radius * 2, radius * 2, parent=node)
        self.node = node
        self.index = index
        self.position = position

        # Setup socket appearance.
        self.radius = radius
        self.outline_width = 1
        self.bg_color = QColor(255, 153, 51, 255)
        self.outline_color = QColor(0, 0, 0, 255)

        self._pen = QPen(self.outline_color)
        self._pen.setWidth(self.outline_width)
        self._brush = QBrush(self.bg_color)

        self.setPos(*self.node.get_socket_placement(self.index, self.position))


    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        painter.setPen(self._pen)
        painter.setBrush(self._brush)
        painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)