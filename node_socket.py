from enum import Enum

from node_graphics_socket import NodeGraphicsSocket


class SocketPosition(Enum):
    LEFT_TOP = 1
    LEFT_BOTTOM = 2
    RIGHT_TOP = 3
    RIGHT_BOTTOM = 4


class Socket:
    def __init__(self, node, index=0, position=SocketPosition.LEFT_TOP):
        self.node = node
        self.index = index
        self.position = position

        self.gr_socket = NodeGraphicsSocket(self.node.gr_node)
        self.gr_socket.setPos(*self.node.get_socket_placement(self.index, self.position))
