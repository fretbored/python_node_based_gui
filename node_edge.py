from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Edge(QGraphicsPathItem):
    def __init__(self, scene, start_socket, end_socket=None):
        super().__init__()
        self.scene = scene
        self.start_socket = start_socket
        self.end_socket = end_socket

        # Setup edge appearance.
        self.setZValue(-1) # Draw edges behind nodes.
        self._path_color = start_socket.bg_color
        self._pen = QPen(self._path_color)
        self._pen.setWidth(2)

        self._path_under_mouse_color = QColor(200, 200, 200, 255)
        self._pen_under_mouse = QPen(self._path_under_mouse_color)
        self._pen_under_mouse.setWidth(2)

        self._path_selected_color = QColor(204, 204, 0, 255)
        self._pen_selected = QPen(self._path_selected_color)
        self._pen_selected.setWidth(2)

        self.setPen(self._pen)
        # Setup edge behavior.
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.hovered = False


    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        self.update_path()

        painter.setBrush(Qt.NoBrush)
        if self.hovered:
            painter.setPen(self._pen_under_mouse)
        elif self.isSelected():
            painter.setPen(self._pen_selected)
        else:
            painter.setPen(self._pen)

        painter.drawPath(self.path())


    def hoverEnterEvent(self, event):
        # self.setPen(self._pen_under_mouse)
        self.hovered = True
        super().hoverEnterEvent(event)


    def hoverLeaveEvent(self, event):
        # self.setPen(self._pen)
        self.hovered = False
        super().hoverLeaveEvent(event)


    def update_path(self):
        start_pos = self.start_socket.get_scene_position()
        # Add the buffer to the y position so that the edge starts at the center of the socket.
        buffer = self.start_socket.radius
        path = QPainterPath(QPointF(start_pos.x(), start_pos.y() + buffer))
        if self.end_socket:
            # The edge has both a start socket and end socket.
            end_pos = self.end_socket.get_scene_position()
        else:
            # The edge only has a start socket.
            end_pos = self.scene.mouse_position
        distance = (end_pos.x() - start_pos.x()) / 2
        path.cubicTo(QPointF(start_pos.x() + distance, start_pos.y() + buffer),
                    QPointF(end_pos.x() - distance, end_pos.y() + buffer),
                    QPointF(end_pos.x(), end_pos.y() + buffer))

        self.setPath(path)


    def remove_from_sockets(self):
        if self.start_socket:
            self.start_socket.edge = None
        if self.end_socket:
            self.end_socket.edge = None
        self.start_socket = None
        self.end_socket = None


    def remove(self):
        self.remove_from_sockets()
        self.scene.remove_edge(self)