from node_graphics_node import NodeGraphicsNode
from node_content_widget import NodeContentWidget
from node_socket import *


class Node:
    def __init__(self, scene, title='New Node', inputs=[], outputs=[]):
        self.scene = scene
        self.title = title
        self.inputs = inputs
        self.outputs = outputs
        self.socket_spacing = 22

        self.content = NodeContentWidget()
        self.gr_node = NodeGraphicsNode(self)
        self.scene.add_node(self)

        for i in range(len(self.inputs)):
            socket = Socket(node=self, index=i, position=SocketPosition.LEFT_BOTTOM)
            self.inputs.append(socket)

        for i in range(len(self.outputs)):
            socket = Socket(node=self, index=i, position=SocketPosition.RIGHT_TOP)
            self.inputs.append(socket)


    def get_socket_placement(self, index, position=SocketPosition.LEFT_TOP):
        socket_x = 0
        if position in (SocketPosition.RIGHT_TOP, SocketPosition.RIGHT_BOTTOM):
            socket_x = self.gr_node.width
        if position in (SocketPosition.RIGHT_TOP, SocketPosition.LEFT_TOP):
            socket_y = (self.gr_node.title_height +
                        (self.gr_node._padding * 3) +
                        (index * self.socket_spacing))
        else:
            socket_y = (self.gr_node.height -
                        (self.gr_node._padding * 3) -
                        (index * self.socket_spacing))

        return socket_x, socket_y