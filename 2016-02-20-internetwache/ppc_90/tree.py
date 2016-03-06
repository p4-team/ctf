import re
import socket
from time import sleep

import bintrees


class Node:
    def __init__(self, data=None):
        self.left = None
        self.right = None
        self.data = data

    def insert(self, data):
        if self.data:
            if data <= self.data:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data


def display(root):
    result = []
    result.append(root.data)
    if root.left is not None:
        result.extend(display(root.left))
    if root.right is not None:
        result.extend(display(root.right))
    return result


def invert_tree(root):
    left = root.left
    right = root.right
    root.right = left
    root.left = right
    if root.right is not None:
        invert_tree(root.right)
    if root.left is not None:
        invert_tree(root.left)


def order(nodes):
    root = Node()
    for node in nodes:
        root.insert(node)
    invert_tree(root)
    return display(root)


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("188.166.133.53", 11491))
    regex = "Level \d+\.: \[(.*)\]"
    initial_data = str(s.recv(4096))
    print(initial_data)
    while True:
        sleep(1)
        task = str(s.recv(4096))
        print(task)
        m = re.search(regex, task)
        nodes = [int(x) for x in m.group(1).split(",")]
        print(nodes)
        result = order(nodes)
        print(result)
        s.sendall(str(result) + "\n")
    pass


main()

#IW{10000101010101TR33}