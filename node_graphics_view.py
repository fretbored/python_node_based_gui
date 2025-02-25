from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class NodeGraphicsView(QGraphicsView):
    def __init__(self, graphics_scene, parent=None):
        super().__init__(parent)
        self.graphics_scene = graphics_scene
        self.init_ui()
        self.setScene(self.graphics_scene)
        # Setup zoom settings.
        self.zoom_factor = 1.25
        self.zoom = 10
        self.zoom_step = 1
        self.zoom_range = [0, 12]


    def init_ui(self):
        # Set antialiasing
        self.setRenderHints(QPainter.Antialiasing |
                            QPainter.HighQualityAntialiasing |
                            QPainter.TextAntialiasing |
                            QPainter.SmoothPixmapTransform)
        # Set to update the entire viewport
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        # Turn off scrollbars
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)


    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)


    def middleMouseButtonPress(self, event):
        """
        Use the middle mouse button to pan the view.
        """
        left_release_event = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                    Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(left_release_event)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        left_press_event = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                       Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(left_press_event)


    def middleMouseButtonRelease(self, event):
        """
        Release the middle mouse button to stop panning the view.
        """
        left_release_event = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                            Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(left_release_event)
        self.setDragMode(QGraphicsView.NoDrag)


    def wheelEvent(self, event):
        """
        Use the mouse wheel to zoom in and out.
        """
        # Calculate the zoom factor.
        zoom_out_factor = 1 / self.zoom_factor

        # Store scene position.
        old_pos = self.mapToScene(event.pos())

        # Calculate new zoom.
        if event.angleDelta().y() > 0:
            # Scrolling up with the mouse wheel.
            zoom_factor = self.zoom_factor
            self.zoom += self.zoom_step
        else:
            # Scrolling down with the mouse wheel.
            zoom_factor = zoom_out_factor
            self.zoom -= self.zoom_step
        
        zoom_clamping = False
        if self.zoom < self.zoom_range[0]:
            zoom_clamping = True
            self.zoom = self.zoom_range[0]
        elif self.zoom > self.zoom_range[1]:
            zoom_clamping = True
            self.zoom = self.zoom_range[1]

        # Zoom in our out based on the zoom factor.
        if not zoom_clamping:
            self.scale(zoom_factor, zoom_factor)