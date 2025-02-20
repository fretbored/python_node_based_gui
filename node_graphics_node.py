from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class NodeGraphicsNode(QGraphicsItem):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node
        self.content = self.node.content

        self._title_color = Qt.white
        self._title_font = QFont('Ubuntu', 10)

        self.width = 180
        self.height = 240
        self.edge_size = 10
        self.title_height = 24
        self._padding = 5.0

        self._pen_default = QPen(QColor(0, 0, 0, 125))
        self._pen_selected = QPen(QColor(255, 200, 40, 255))

        self._brush_title = QBrush(QColor(100, 100, 120, 255))
        self._brush_background = QBrush(QColor(65, 65, 85, 230))

        self.create_title()
        self.title = self.node.title

        # Initialize sockets.
        self.create_sockets(self.node.inputs, self.node.outputs)

        # Initialize content.
        self.create_content()

        self.init_ui()


    @property
    def title(self):
        return self._title
    
    
    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)


    def init_ui(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)


    def create_title(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setTextWidth(self.width - 2 * self._padding)
        self.title_item.setPos(self._padding, 0)


    def create_sockets(self, inputs, outputs):
        pass


    def create_content(self):
        self.gr_content = QGraphicsProxyWidget(self)
        self.content.setGeometry(self.edge_size,
                                 self.title_height + self.edge_size,
                                 self.width - 2 * self.edge_size,
                                 self.height - (2 * self.edge_size) - self.title_height
                                 )
        self.gr_content.setWidget(self.content)

    def boundingRect(self):
        return QRectF(0,
                      0,
                      self.width,
                      self.height
                      ).normalized()


    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # Paint the title.
        title_path = QPainterPath()
        title_path.setFillRule(Qt.WindingFill)
        title_path.addRoundedRect(0, 0, self.width, self.title_height, self.edge_size, self.edge_size)
        title_path.addRect(0, self.title_height - self.edge_size, self.width, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(title_path.simplified())
        # Paint the background.
        background_path = QPainterPath()
        background_path.setFillRule(Qt.WindingFill)
        background_path.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height, self.edge_size, self.edge_size)
        background_path.addRect(0, self.title_height, self.width, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(background_path.simplified())
        # Paint the node outline.
        outline_path = QPainterPath()
        outline_path.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        if self.isSelected():
            painter.setPen(self._pen_selected)
        else:
            painter.setPen(self._pen_default)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(outline_path.simplified())