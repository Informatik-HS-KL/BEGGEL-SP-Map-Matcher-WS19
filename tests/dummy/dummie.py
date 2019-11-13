class Node:
    def __init__(self, node_pos: tuple):
        self.node_pos = node_pos

    def get_latlon(self):
        return self.node_pos

class Link:
    def __init__(self, start: tuple, end: tuple):
        self.start = start
        self.end = end

    def get_start_node(self):
        return Node(self.start)

    def get_end_node(self):
        return Node(self.end)
