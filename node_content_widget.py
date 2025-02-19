from PyQt5.QtWidgets import *


class NodeContentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()


    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.label = QLabel('My Widget Title')
        self.layout.addWidget(self.label)
        self.layout.addWidget(QTextEdit('foo'))