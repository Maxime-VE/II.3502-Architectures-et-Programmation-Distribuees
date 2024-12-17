# Python code for implemementing Merkle Tree
from typing import List
import hashlib
import logging

logging.basicConfig(
    level=logging.INFO,
    filename="merkletree.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)

class Node:
    def __init__(self, left, right, value: str, content):
        self.left: Node = left
        self.right: Node = right
        self.value = value
        self.content = content
        logging.info(f"New node added : {self}")


    def hash(val: str):
        return f"h({val})"
        # return hashlib.sha256(val.encode('utf-8')).hexdigest()

    def __str__(self):
        return str(self.value)

    # Copy left node to right node (used in case of odd node log entry)
    def copy(self):
        return Node(self.left, self.right, self.value, self.content, True)


class MerkleTree:
    def __init__(self, values):
        logging.info("Creation of a new Merkle Tree")
        self.values = values
        self.build_tree(values)

    def build_tree(self, values):
        leaves: List[Node] = [Node(None, None, Node.hash(e), e) for e in values]
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

    def getRootHash(self):
        logging.info("Root Hash asked for Merkle Tree")
        return self.root.value

    def add_node(self, value: str):
        logging.info(f"Adding new value to Merkle Tree: {value}")
        self.values.append(value)
        self.build_tree(self.values)  # Rebuild the tree

    def add_node_list(self, values):
        new_nodes = ' | '.join(values)
        logging.info(f"Adding new value to Merkle Tree: {new_nodes}")
        for event in values:
            self.add_node(event)
        self.build_tree(self.values)  # Rebuild the tree


def mixmerkletree(data_into_list):
    print("Inputs: ")
    print(*element_list, sep=" | ")
    print("")
    mtree = MerkleTree(element_list)
    print("Root Hash: "+mtree.getRootHash()+"\n")
    mtree.print_tree()
    mtree.add_node('6')
    print("Root Hash: "+mtree.getRootHash()+"\n")
    mtree.add_node('7')
    print("Root Hash: "+mtree.getRootHash()+"\n")
    mtree.add_node_list(['8', '9'])
    print("Root Hash: "+mtree.getRootHash()+"\n")



filename = "example.txt"

with open(filename, 'r') as fichier:
    lignes = fichier.readlines()
element_list = [ligne.strip() for ligne in lignes]
logging.info(f"New file received : {filename}")
mixmerkletree(element_list)
