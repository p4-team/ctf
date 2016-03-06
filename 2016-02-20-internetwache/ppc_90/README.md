## Dark Forest (PPC, 90p)

	Description: Someone pre-ordered a forest and now I'm lost in it. 
	There are a lot of binary trees in front and behind of me. 
	Some are smaller or equal-sized than others. 
	Can you help me to invert the path and find out of the forest? 
	Hint: It's about (inverted) BSTs. Don't forget the spaces. 
	
###ENG
[PL](#pl-version)

Server sends input as:

	I'm lost in a forest. Can you invert the path?
	Level 1.: [13, 3]
	
This is list of binary tree nodes in pre-order. 
Our task is to recontruct the tree, invert it and send to the server as pre-order.
Inverting the tree means that any left branch becomes right branch, and right branch becomes left:

```python
def invert_tree(root):
    left = root.left
    right = root.right
    root.right = left
    root.left = right
    if root.right is not None:
        invert_tree(root.right)
    if root.left is not None:
        invert_tree(root.left)
```

Traversing and printing pre-order means that we print the value of the node before we print the branches nodes:

```python
def display(root):
    result = []
    result.append(root.data)
    if root.left is not None:
        result.extend(display(root.left))
    if root.right is not None:
        result.extend(display(root.right))
    return result
```

Therefore we simply read nodes from input, add them to the tree, invert it and send inverted tree as response.
Complete solution is [here](tree.py).

After 100 tasks we get the flag: `IW{10000101010101TR33}`

###PL version

Serwer przysyła dane jako:

	I'm lost in a forest. Can you invert the path?
	Level 1.: [13, 3]
	
To jest lista węzłów drzewa binarnego w porządku pre-order.
Naszym zadaniem jest odbudować drzewo, odwrócić je a następnie wysłać je do serwera w porządku pre-order.
Odwracanie drzewa oznacza że każda lewa gałąź staje się prawą a prawa lewą:

```python
def invert_tree(root):
    left = root.left
    right = root.right
    root.right = left
    root.left = right
    if root.right is not None:
        invert_tree(root.right)
    if root.left is not None:
        invert_tree(root.left)
```

Przechodzenie i wypisanie drzewa pre-order oznacza że najpierw wypisujemy wartość danego węzła a dopiero potem jego gałęzi:

```python
def display(root):
    result = []
    result.append(root.data)
    if root.left is not None:
        result.extend(display(root.left))
    if root.right is not None:
        result.extend(display(root.right))
    return result
```

W związku z tym pobieramy z wejścia listę węzłów, dodajemy je do drzewa, odwracamy je i odsyłamy odwrócone drzewo jako odpowiedź.
Całe rozwiązanie jest [tutaj](tree.py).

Po 100 przykładach dostajemy flagę: `IW{10000101010101TR33}`
