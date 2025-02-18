from PyQt5.QtWidgets import *

from node_graphics_scene import NodeGraphicsScene


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
        self.view = QGraphicsView(self)
        self.view.setScene(self.graphics_scene)
        self.layout.addWidget(self.view)

        self.center_window()
        self.show()