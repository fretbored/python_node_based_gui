from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from node_scene import Scene
from node_node import Node
from node_socket import Socket
from node_graphics_view import NodeGraphicsView


class NodeEditorWindow(QWidget):
    """
    Represents the main window used to create and edit nodes.
    """
    def __init__(self, parent=None):
        """
        This constructor sets up the QWidget, loads a stylesheet for styling, and
        initializes the user interface. The window can optionally have a parent.

        Args:
            parent (QWidget, optional): The parent widget of this window. Defaults to None.
        """
        super().__init__(parent)
        self.stylesheet_path = 'qss/node_style.qss'
        self.load_stylesheet(self.stylesheet_path)
        
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
        self.scene = Scene()
        # Create graphics view
        self.view = NodeGraphicsView(self.scene, self)
        self.layout.addWidget(self.view)

        self.center_window()
        self.show()


    def load_stylesheet(self, path):
        print(f'Loading stylesheet from: {path}...')
        with open(path, 'r') as f:
            QApplication.instance().setStyleSheet(f.read())