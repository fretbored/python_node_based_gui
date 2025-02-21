import math

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from node_node import Node
from node_edge import Edge
from node_socket import Socket


class Scene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.nodes = []
        self.edges = []
        self.mouse_position = QPoint(0, 0)
        self.current_edge = None

        self.scene_width = 64000
        self.scene_height = 64000

        # Setup the grid appearance
        self.grid_size = 20
        self.grid_squares = 4

        self.bg_color = QColor(100, 100, 100, 255)
        self.setBackgroundBrush(self.bg_color)

        self.pen_color_light = QColor(88, 88, 88, 255)
        self.small_grid_pen = QPen(self.pen_color_light)
        self.small_grid_pen.setWidth(1)

        self.pen_color_dark = QColor(80, 80, 80, 255)
        self.large_grid_pen = QPen(self.pen_color_dark)
        self.large_grid_pen.setWidth(2)

        self.init_ui()


    def init_ui(self):
        self.set_gr_scene(self.scene_width, self.scene_height)


    def set_gr_scene(self, width, height):
        self.setSceneRect(-width//2, -height//2, width, height)


    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        # Draw the grid
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.ceil(rect.top()))
        bottom = int(math.floor(rect.bottom()))

        first_left = left - (left % self.grid_size)
        first_top = top - (top % self.grid_size)

        # Create all lines to be drawn
        grid_lines_light = []
        grid_lines_dark = []
        for x in range(first_left, right, self.grid_size):
            if x % (self.grid_size * self.grid_squares) == 0:
                # Draw a dark line every 80 pixels
                grid_lines_dark.append(QLine(x, top, x, bottom))
            else:
                grid_lines_light.append(QLine(x, top, x, bottom))
        for y in range(first_top, bottom, self.grid_size):
            if y % (self.grid_size * self.grid_squares) == 0:
                # Draw a dark line every 80 pixels
                grid_lines_dark.append(QLine(left, y, right, y))
            else:
                grid_lines_light.append(QLine(left, y, right, y))

        # Draw the lines
        painter.setPen(self.small_grid_pen)
        painter.drawLines(grid_lines_light)
        painter.setPen(self.large_grid_pen)
        painter.drawLines(grid_lines_dark)


    def contextMenuEvent(self, event):
        menu = QMenu()
        add_action = QAction('Add Node', menu)
        add_action.triggered.connect(lambda: self.add_node(event.scenePos()))
        menu.addAction(add_action)
        menu.exec_(event.screenPos())


    def mouseMoveEvent(self, event):
        """
        Store the mouse position in the scene for drawing edges.
        """
        self.mouse_position = event.scenePos()
        if self.current_edge:
            self.current_edge.update_path()
        super().mouseMoveEvent(event)


    def mouseReleaseEvent(self, event):
        """
        Handles the completion of new edges. Edges hovered over an input socket
        are created, while edges hovered over an output socket are deleted.
        """
        if self.current_edge:
            # Check if mouse is over a socket.
            items = self.items(event.scenePos())
            valid_end_socket = None

            for item in items:
                if isinstance(item, Socket):
                    if self.current_edge.start_socket.is_input:
                        # Creating a new edge from an input socket is invalid.
                        continue
                    if not item.is_input:
                        # Connecting a new edge to an output socket is invalid.
                        continue
                    if item.is_input and not item.connections:
                        # Connecting to an empty input socket.
                        valid_end_socket = item
                        break
            
            if valid_end_socket:
                # Complete creating the edge.
                self.current_edge.end_socket = valid_end_socket
                valid_end_socket.connections.append(self.current_edge)
                # self.current_edge.update_path()
            else:
                # Delete the edge.
                self.current_edge.start_socket.connections.remove(self.current_edge)
                self.removeItem(self.current_edge)
        self.current_edge = None
        super().mouseReleaseEvent(event)


    def create_edge(self, socket):
        """
        Create a new edge from the given socket.
        """
        self.current_edge = Edge(self, socket)
        socket.connections.append(self.current_edge)
        self.edges.append(self.current_edge)
        self.addItem(self.current_edge)


    def add_node(self, position):
        node = Node(self,
                    'My First Node',
                    inputs=['foo', 'bar'],
                    outputs=['baz'],
                    parent=self)
        node.setPos(position)
        self.nodes.append(node)
        self.addItem(node)
        # if len(self.nodes) == 2:
        #     self.add_edge()


    # def add_edge(self):
    #     edge = Edge(self, self.nodes[0].output_sockets[0], self.nodes[1].input_sockets[0])
    #     self.edges.append(edge)
    #     self.addItem(edge)


    def remove_node(self, node):
        self.nodes.remove(node)


    def remove_edge(self, edge):
        self.removeItem(edge)
        self.edges.remove(edge)
