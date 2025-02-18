from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from node_graphics_scene import NodeGraphicsScene
from node_graphics_view import NodeGraphicsView


class NodeEditorWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()


    def center_window(self):
        """
        Centers the window on the screen by calculating the frame geometry
        and moving the window to the top-left corner to the center of the screen.
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def init_ui(self):
        self.setWindowTitle('Node Editor')
        self.resize(1200, 800)
        self.setContentsMargins(0, 0, 0, 0)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create graphics scene
        self.graphics_scene = NodeGraphicsScene()
        # Create graphics view
        self.view = NodeGraphicsView(self.graphics_scene, self)
        self.layout.addWidget(self.view)

        self.center_window()
        self.show()

        self.add_debug_content()


    def add_debug_content(self):
        green_brush = QBrush(Qt.green)
        outline_pen = QPen(Qt.black)
        outline_pen.setWidth(2)
        
        rect = self.graphics_scene.addRect(-100, -100, 80, 100, outline_pen, green_brush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)

        text = self.graphics_scene.addText('Lorum Ipsum!')
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setDefaultTextColor(Qt.white)

        widget1 = QPushButton('Hello World')
        proxy1 = self.graphics_scene.addWidget(widget1)
        proxy1.setFlag(QGraphicsItem.ItemIsMovable)
        proxy1.setPos(0, 30)

        widget2 = QTextEdit()
        proxy2 = self.graphics_scene.addWidget(widget2)
        proxy2.setFlag(QGraphicsItem.ItemIsSelectable)
        proxy2.setPos(0, 60)

        line = self.graphics_scene.addLine(-200, -200, 400, -100, outline_pen)
        line.setFlag(QGraphicsItem.ItemIsSelectable)
        line.setFlag(QGraphicsItem.ItemIsMovable)