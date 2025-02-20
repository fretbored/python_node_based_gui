import math

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Scene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.nodes = []
        self.edges = []

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


    def add_node(self, node):
        self.nodes.append(node)
        self.addItem(node)


    def add_edge(self, edge):
        self.edges.append(edge)


    def remove_node(self, node):
        self.nodes.remove(node)


    def remove_edge(self, edge):
        self.edges.remove(edge)
