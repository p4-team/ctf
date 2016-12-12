# BFS (ppc 400)

###ENG
[PL](#pl-version)

In the task we get a database [file](maze.db) with maze definition.
We dumped the data to [txt](data.txt) to simplify usage.
Each node stores a single byte of data.
We guess that the point is to find the path through the maze.
We used simple BFS search for that:

```python
import codecs
import collections


def print_matrix(matrix):
    for i in range(50):
        print(" ".join(matrix[i]))


def add_unvisited_node(to_process, visited, x, y, backtrace, prev):
    if (x, y) not in visited:
        visited.add((x, y))
        backtrace[(x, y)] = prev
        to_process.append((x, y))


def main():
    visited = {(0, 0)}
    to_process = [(0, 0)]
    graph = collections.defaultdict(dict)
    backtrace = {}
    with codecs.open("data.txt") as input_file:
        for line in input_file:
            # eg. 1|0|0|gate|1
            data = line[:-2].split("|")
            node_id = int(data[0])
            x = int(data[1])
            y = int(data[2])
            wall_type = data[3]
            payload = data[4]
            graph[x][y] = (node_id, wall_type, payload)

    while len(to_process) > 0:
        xy = to_process.pop(0)
        x = xy[0]
        y = xy[1]
        if x in graph and y in graph[x]:
            node = graph[x][y]
            if node[0] == 2500:
                break
            if node[1] == "gate":
                add_unvisited_node(to_process, visited, x - 1, y, backtrace, xy)
                add_unvisited_node(to_process, visited, x, y - 1, backtrace, xy)
                add_unvisited_node(to_process, visited, x, y + 1, backtrace, xy)
                add_unvisited_node(to_process, visited, x + 1, y, backtrace, xy)
    print(backtrace)
    current = (49, 49)
    data = []
    matrix = [['   ' for i in range(50)] for j in range(50)]
    i = 0
    while current != (0, 0):
        x = current[0]
        y = current[1]
        matrix[x][y] = "%3d" % i
        i += 1
        data.append(graph[x][y][2])
        current = backtrace[(x, y)]
    data.reverse()
    print_matrix(matrix)
    result = "".join(data)
    print(result)


main()

```

Which prints out the maze solution and the bytes picked up on the way:

```
54C82F36487A9157315AADFDDED1BB83ECD98E49EADAFEB03DB563A94E0851478C408CFD6B0BB42B030F61A82E655B7FCA0E1FA68DF676758DC60FBFD1016F0EB8E7A2B5170A157497EF711E4009653BC9B20726C98B6561EFBE316AC2AB2DCBE56494F05B44ED3EB62DA4109BEEC2537266FEDE44ACB12A17CA8C8A5BA9E1A4D24ACAD900FFBD228AC187B9024BEDC941D137EA3A92F9F8506740CD8C62DBEDB9990F3E0259434D9FCF070FEC9E60C5697BABA83A4E59EB4C3F0E7AFD44B1B8D9D93933962B27237560B5F8F7D19904D790842FA596FBB52B2A3F7EE15B7F589D28A6F20F747615E7ED135E17AFE8FE073B6606F5C893D40CB78B635AA5FE4E0EE10C572D5E7AECEAF743953D05F78BBC10A9BB3D53B0011AE5F269C806E5F9E6026C954A0CDF9C797953360602B96FC06324C3160701505C24597F6F7C77D5B76CBE25CD2B706A41DA324A1B79CFC4BA8B11F800593514D27754
```

As far as I remember this was the flag.

###PL version

W zadaniu dostajemy [plik](maze.db) z definicją labiryntu.
Zrzuciliśmy dane do [txt](data.txt) żeby ułatwić sobie pracę.
Każdy węzeł uzyskanego grafu przechowuje jeden bajt danych.
Domyślaliśmy się, ze zadaniem jest znaleźć drogę w labiryncie.
Użyliśmy do tego BFSa:

```python
import codecs
import collections


def print_matrix(matrix):
    for i in range(50):
        print(" ".join(matrix[i]))


def add_unvisited_node(to_process, visited, x, y, backtrace, prev):
    if (x, y) not in visited:
        visited.add((x, y))
        backtrace[(x, y)] = prev
        to_process.append((x, y))


def main():
    visited = {(0, 0)}
    to_process = [(0, 0)]
    graph = collections.defaultdict(dict)
    backtrace = {}
    with codecs.open("data.txt") as input_file:
        for line in input_file:
            # eg. 1|0|0|gate|1
            data = line[:-2].split("|")
            node_id = int(data[0])
            x = int(data[1])
            y = int(data[2])
            wall_type = data[3]
            payload = data[4]
            graph[x][y] = (node_id, wall_type, payload)

    while len(to_process) > 0:
        xy = to_process.pop(0)
        x = xy[0]
        y = xy[1]
        if x in graph and y in graph[x]:
            node = graph[x][y]
            if node[0] == 2500:
                break
            if node[1] == "gate":
                add_unvisited_node(to_process, visited, x - 1, y, backtrace, xy)
                add_unvisited_node(to_process, visited, x, y - 1, backtrace, xy)
                add_unvisited_node(to_process, visited, x, y + 1, backtrace, xy)
                add_unvisited_node(to_process, visited, x + 1, y, backtrace, xy)
    print(backtrace)
    current = (49, 49)
    data = []
    matrix = [['   ' for i in range(50)] for j in range(50)]
    i = 0
    while current != (0, 0):
        x = current[0]
        y = current[1]
        matrix[x][y] = "%3d" % i
        i += 1
        data.append(graph[x][y][2])
        current = backtrace[(x, y)]
    data.reverse()
    print_matrix(matrix)
    result = "".join(data)
    print(result)


main()

```

Co wypisuje na koniec rozwiązanie labiryntu oraz dane zebrane po drodze:

```
54C82F36487A9157315AADFDDED1BB83ECD98E49EADAFEB03DB563A94E0851478C408CFD6B0BB42B030F61A82E655B7FCA0E1FA68DF676758DC60FBFD1016F0EB8E7A2B5170A157497EF711E4009653BC9B20726C98B6561EFBE316AC2AB2DCBE56494F05B44ED3EB62DA4109BEEC2537266FEDE44ACB12A17CA8C8A5BA9E1A4D24ACAD900FFBD228AC187B9024BEDC941D137EA3A92F9F8506740CD8C62DBEDB9990F3E0259434D9FCF070FEC9E60C5697BABA83A4E59EB4C3F0E7AFD44B1B8D9D93933962B27237560B5F8F7D19904D790842FA596FBB52B2A3F7EE15B7F589D28A6F20F747615E7ED135E17AFE8FE073B6606F5C893D40CB78B635AA5FE4E0EE10C572D5E7AECEAF743953D05F78BBC10A9BB3D53B0011AE5F269C806E5F9E6026C954A0CDF9C797953360602B96FC06324C3160701505C24597F6F7C77D5B76CBE25CD2B706A41DA324A1B79CFC4BA8B11F800593514D27754
```

O ile dobrze pamiętam to była flaga.
