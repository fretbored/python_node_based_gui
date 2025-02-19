from node_graphics_node import NodeGraphicsNode
from node_content_widget import NodeContentWidget


class Node:
    def __init__(self, scene, title='New Node'):
        self.scene = scene
        self.title = title
        self.inputs = []
        self.outputs = []

        self.content = NodeContentWidget()
        self.gr_node = NodeGraphicsNode(self)
        self.scene.add_node(self)