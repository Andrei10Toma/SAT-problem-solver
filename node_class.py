class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    def set_left(self, left_node):
        self.left = left_node

    def set_right(self, right_node):
        self.right = right_node

    def __str__(self):
        return str(self.data)

    def preorder_traverse(self, start_node):
        if start_node is None:
            return
        print(start_node.data)
        self.preorder_traverse(start_node.left)
        self.preorder_traverse(start_node.right)
