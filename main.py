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
    def __init__(self, left, right, value: str, content, is_copied=False):
        self.left: Node = left
        self.right: Node = right
        self.value = value
        self.content = content
        self.is_copied = is_copied
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
        self.build_tree(values)

    def build_tree(self, values):

        leaves: List[Node] = [Node(None, None, Node.hash(e), e) for e in values]
        if len(leaves) % 2 == 1:
            leaves.append(leaves[-1].copy())
        self.root = self.build_tree_recursive(leaves)

    def build_tree_recursive(self, nodes):
        if len(nodes) % 2 == 1:
            nodes.append(nodes[-1].copy())
        half = len(nodes) // 2

        if len(nodes) == 2:
            return Node(nodes[0], nodes[1], Node.hash(nodes[0].value + nodes[1].value), f" {nodes[0].content} + {nodes[1].content} ")

        left = self.build_tree_recursive(nodes[:half])
        right = self.build_tree_recursive(nodes[half:])
        value = Node.hash(left.value + right.value)
        content = f'{left.content}+{right.content}'
        return Node(left, right, value, content)

    def print_tree(self):
        logging.info("Full Merkle Tree scheme asked")
        self.print_tree_recursive(self.root)

    def print_tree_recursive(self, node):
        if node != None:
            if node.left != None:
                print("Left: "+str(node.left))
                print("Right: "+str(node.right))
            else:
                print("Input")

            if node.is_copied:
                print('(Padding)')
            print("Value: "+str(node.value))
            print("Content: "+str(node.content))
            print("")
            self.print_tree_recursive(node.left)
            self.print_tree_recursive(node.right)

    def getRootHash(self):
        logging.info("Root Hash asked for Merkle Tree")
        return self.root.value


def mixmerkletree(data_into_list):
    print("Inputs: ")
    print(*element_list, sep=" | ")
    print("")
    mtree = MerkleTree(element_list)
    print("Root Hash: "+mtree.getRootHash()+"\n")
    mtree.print_tree()


filename = "example.txt"

with open(filename, 'r') as fichier:
    lignes = fichier.readlines()
element_list = [ligne.strip() for ligne in lignes]
logging.info(f"New file received : {filename}")
mixmerkletree(element_list)
