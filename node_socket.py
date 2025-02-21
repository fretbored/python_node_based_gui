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
    def __init__(self, node, index=0, position=SocketPosition.LEFT_TOP, is_input=True, radius=6):
        super().__init__(0, 0, radius * 2, radius * 2, parent=node)
        self.node = node
        self.index = index
        self.position = position
        self.is_input = is_input
        self.connections = []

        # Setup socket appearance.
        self.radius = radius
        self.outline_width = 1
        self.bg_color = QColor(255, 153, 51, 255)
        self.outline_color = QColor(0, 0, 0, 255)

        self._pen = QPen(self.outline_color)
        self._pen.setWidth(self.outline_width)
        self._brush = QBrush(self.bg_color)

        self.hover_color = QColor(200, 200, 200, 255)
        self._hover_brush = QBrush(self.hover_color)

        # Setup socket behavior.
        self.setAcceptHoverEvents(True)

        self.setBrush(self._brush)

        socket_pos = self.get_socket_position()
        self.setPos(socket_pos[0], socket_pos[1])


    def hoverEnterEvent(self, event):
        """
        Highlight the socket when the mouse hovers over it.
        """
        self.setBrush(self._hover_brush)
        super().hoverEnterEvent(event)


    def hoverLeaveEvent(self, event):
        self.setBrush(self._brush)
        super().hoverMoveEvent(event)


    def mousePressEvent(self, event):
        # Start creating an edge.
        if event.button() == Qt.LeftButton and not self.is_input:
            # Only create edges from output sockets.
            self.node.scene.create_edge(self)
        super().mousePressEvent(event)


    def get_scene_position(self):
        return self.node.mapToScene(self.pos())


    def get_socket_position(self):
        return self.node.get_socket_placement(self.index, self.position, self.radius)