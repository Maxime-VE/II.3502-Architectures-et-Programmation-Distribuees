import math
import hashlib
import logging

class Node:
    def __init__(self, left, right, value: str, content):
        self.left: Node = left
        self.right: Node = right
        self.value = value
        self.content = content
        logging.info(f"New node added : {self}")


    def hash(val: str):
        # return f"h({val})"
        return hashlib.sha256(val.encode('utf-8')).hexdigest()

    def __str__(self):
        return str(self.value)


class MerkleTree:
    def __init__(self, values):
        logging.info("Creation of a new Merkle Tree")
        self.values = values
        self.size = self.compute_size()
        self.build_tree(values)

    def build_tree(self, values):
        leaves = [Node(None, None, Node.hash(e), e) for e in values]
        self.root = self.build_tree_recursive(leaves)

    def build_tree_recursive(self, nodes):
        if len(nodes) == 1:
            return nodes[0]

        if len(nodes) % 2 == 1:
            nodes.append(None)

        parents = []
        for i in range(0, len(nodes), 2):
            left = nodes[i]
            right = nodes[i + 1]

            if right is None:
                value = Node.hash(left.value)
                content = left.content
            else:
                value = Node.hash(left.value + right.value)
                content = f'{left.content} + {right.content}'

            parents.append(Node(left, right, value, content))
        return self.build_tree_recursive(parents)

    def compute_size(self):
        if len(self.values) < 1:
            return 0
        return math.ceil(math.log2(len(self.values))) + 1

    def print_tree(self):
        logging.info("Full Merkle Tree scheme asked")
        self.print_tree_recursive(self.root)

    def print_tree_recursive(self, node):
        if node is not None:
            if node.left is not None or node.right is not None:
                print("Left: "+str(node.left))
                print("Right: "+str(node.right))
            else:
                print("Input")

            print("Value: "+str(node.value))
            print("Content: "+str(node.content))
            print("")
            self.print_tree_recursive(node.left)
            self.print_tree_recursive(node.right)

    def get_root_value(self):
        logging.info("Root Hash asked for Merkle Tree")
        return self.root.value

    def add_node(self, value):
        logging.info(f"Adding new value to Merkle Tree: {value}")
        self.values.append(value)
        self.size = self.compute_size()
        self.build_tree(self.values)  # Rebuild the tree

    def add_node_list(self, values):
        new_nodes = ' | '.join(values)
        logging.info(f"Adding new value to Merkle Tree: {new_nodes}")
        for event in values:
            self.add_node(event)
        self.size = self.compute_size()
        self.build_tree(self.values)  # Rebuild the tree

    def gen_path(self, index):
        path = []
        path = self.gen_path_recursive(index, self.root, self.size, path)
        logging.info(f"Gen Path called for Merkle Tree with index: {index}")
        return path[::-1] #Reverse the list to have a path from leaves to root

    def gen_path_recursive(self, index, node, level, path):
        if level == 1:
            return path

        if index <= pow(2, level-2):
            path.append([node.right.value, "right"])
            self.gen_path_recursive(index, node.left, level - 1, path)
        else:
            path.append([node.left.value, "left"])
            index = index - pow(2, level-2)
            self.gen_path_recursive(index, node.right, level - 1, path)
        return path

    def gen_proof(self, index):
        proof = []
        proof = self.gen_proof_recursive(index, self.root, self.size, proof)
        logging.info(f"Gen Proof called for Merkle Tree: index={index}, n={self.size}")
        return proof[::-1]


    def gen_proof_recursive(self, index, node, level, proof):
        if level == 1:
            return proof

        half = pow(2, level - 2)
        if index <= half:
            proof.append(node.right.value if level != 2 else node.value)
            self.gen_proof_recursive(index, node.left, level - 1, proof)
        else:
            proof.append(node.left.value if level != 2 else node.value)
            self.gen_proof_recursive(index - half, node.right, level - 1, proof)
        return proof

    def is_member(self, event_value, audit_path):
        event_hash = Node.hash(event_value)

        for sibling_hash, direction in audit_path:
            if direction == "left":
                event_hash = Node.hash(sibling_hash + event_hash)
            elif direction == "right":
                event_hash = Node.hash(event_hash + sibling_hash)
            else:
                raise ValueError(f"Invalid direction in audit path: {direction}")

        result = event_hash == self.get_root_value()
        logging.info(f"The value \"{event_value}\" is {'' if result else 'not'} the event that match the given audit path")
        return result
