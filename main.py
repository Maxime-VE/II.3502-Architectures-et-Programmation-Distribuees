


class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.hash = data

    def set_left_node(self, node):
        self.left = node

    def set_right_node(self, node):
        self.right = node

class MerkleTree:
    def __init__(self, data):
        self.root = Node(data)

    def insert(self, data):
        node = Node(data)
        if self.root is None:
            self.root = node
            return
        queue = [self.root]
        while queue:
            curr_node = queue.pop(0)
            if curr_node.left is None:
                curr_node.left = node
                break
            else:
                queue.append(curr_node.left)
            if curr_node.right is None:
                curr_node.right = node
                break
            else:
                queue.append(curr_node.right)

