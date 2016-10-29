# number_place (misc 150)

###ENG
[PL](#pl-version)

In the task we get hint about sudoku and address of remote server which sends us inputs in form:

```
.418.5..9..9.7..58.3............26..3...6..25...5...97.....69.2.1..4......7......
```

It's quite clear that this is definition of sudoku grid and we need to solve it to get the flag.
In some later stages the inputs were also containing roman numbers, binary numbers and base-64 decoded numbers.

So we grabbed first sudoku solver from internet, coded data parsing and communication with the server and used the script:

```python
import base64
import socket
import re
from time import sleep


def findNextCellToFill(grid, i, j):
    for x in range(i, 9):
        for y in range(j, 9):
            if grid[x][y] == 0:
                return x, y
    for x in range(0, 9):
        for y in range(0, 9):
            if grid[x][y] == 0:
                return x, y
    return -1, -1


def isValid(grid, i, j, e):
    rowOk = all([e != grid[i][x] for x in range(9)])
    if rowOk:
        columnOk = all([e != grid[x][j] for x in range(9)])
        if columnOk:
            # finding the top left x,y co-ordinates of the section containing the i,j cell
            secTopX, secTopY = 3 * (i / 3), 3 * (j / 3)
            for x in range(secTopX, secTopX + 3):
                for y in range(secTopY, secTopY + 3):
                    if grid[x][y] == e:
                        return False
            return True
    return False


def solveSudoku(grid, i=0, j=0):
    i, j = findNextCellToFill(grid, i, j)
    if i == -1:
        return True
    for e in range(1, 10):
        if isValid(grid, i, j, e):
            grid[i][j] = e
            if solveSudoku(grid, i, j):
                return True
            # Undo the current cell for backtracking
            grid[i][j] = 0
    return False


def stringify(arrays):
    return "".join("".join([str(c) for c in x]) for x in arrays)


def solve(s):
    arrays = [[int(c) for c in s[i * 9:(i + 1) * 9]] for i in range(9)]
    solveSudoku(arrays)
    result = stringify(arrays)
    return result


def parse_bin(s):
    bins = re.findall("\(.+?\)", s)
    for found in bins:
        s = s.replace(found, str(int(found[1:-1], 2)))
    return s


def parse_base64(s):
    bins = re.findall("\[.+?\]", s)
    for found in bins:
        s = s.replace(found, str(base64.b64decode(found[1:-1])))
    return s


def parse_roman(s):
    s = s.replace('<I>', '1')
    s = s.replace('<II>', '2')
    s = s.replace('<III>', '3')
    s = s.replace('<IV>', '4')
    s = s.replace('<V>', '5')
    s = s.replace('<VI>', '6')
    s = s.replace('<VII>', '7')
    s = s.replace('<VIII>', '8')
    s = s.replace('<IX>', '9')
    return s


def parse(s):
    s = s.replace('.', '0')
    s = parse_roman(s)
    s = parse_bin(s)
    s = parse_base64(s)
    return s


def main():
    url = '35.161.87.33'
    port = 10101
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, port))
    while True:
        sleep(1)
        received = s.recv(9999)[:-1]
        print(received)
        received = parse(received)
        result = solve(received)
        print(result)
        s.sendall(result + "\n")


main()

```

Finally we got `ECTF{jk_w3_41n7_s0rrY}`

###PL version

W zadaniu dostajemy hint na temat sudoku oraz adres serwera który wysyła dane w formie:

```
.418.5..9..9.7..58.3............26..3...6..25...5...97.....69.2.1..4......7......
```

Jest dość jasne, że to opis planszy sudoku a my mamy ją rozwiązać aby dostać flagę.
W dalszych poziomach dane zawierały również liczby rzymskie, liczby binarne oraz liczby enkodowane jako base-64.

W związku z tym ściągnęliśmy pierwszy lepszy solver sudoku z internetu, napisalismy parser dla danych oraz komunikacje z serwerem:

```python
import base64
import socket
import re
from time import sleep


def findNextCellToFill(grid, i, j):
    for x in range(i, 9):
        for y in range(j, 9):
            if grid[x][y] == 0:
                return x, y
    for x in range(0, 9):
        for y in range(0, 9):
            if grid[x][y] == 0:
                return x, y
    return -1, -1


def isValid(grid, i, j, e):
    rowOk = all([e != grid[i][x] for x in range(9)])
    if rowOk:
        columnOk = all([e != grid[x][j] for x in range(9)])
        if columnOk:
            # finding the top left x,y co-ordinates of the section containing the i,j cell
            secTopX, secTopY = 3 * (i / 3), 3 * (j / 3)
            for x in range(secTopX, secTopX + 3):
                for y in range(secTopY, secTopY + 3):
                    if grid[x][y] == e:
                        return False
            return True
    return False


def solveSudoku(grid, i=0, j=0):
    i, j = findNextCellToFill(grid, i, j)
    if i == -1:
        return True
    for e in range(1, 10):
        if isValid(grid, i, j, e):
            grid[i][j] = e
            if solveSudoku(grid, i, j):
                return True
            # Undo the current cell for backtracking
            grid[i][j] = 0
    return False


def stringify(arrays):
    return "".join("".join([str(c) for c in x]) for x in arrays)


def solve(s):
    arrays = [[int(c) for c in s[i * 9:(i + 1) * 9]] for i in range(9)]
    solveSudoku(arrays)
    result = stringify(arrays)
    return result


def parse_bin(s):
    bins = re.findall("\(.+?\)", s)
    for found in bins:
        s = s.replace(found, str(int(found[1:-1], 2)))
    return s


def parse_base64(s):
    bins = re.findall("\[.+?\]", s)
    for found in bins:
        s = s.replace(found, str(base64.b64decode(found[1:-1])))
    return s


def parse_roman(s):
    s = s.replace('<I>', '1')
    s = s.replace('<II>', '2')
    s = s.replace('<III>', '3')
    s = s.replace('<IV>', '4')
    s = s.replace('<V>', '5')
    s = s.replace('<VI>', '6')
    s = s.replace('<VII>', '7')
    s = s.replace('<VIII>', '8')
    s = s.replace('<IX>', '9')
    return s


def parse(s):
    s = s.replace('.', '0')
    s = parse_roman(s)
    s = parse_bin(s)
    s = parse_base64(s)
    return s


def main():
    url = '35.161.87.33'
    port = 10101
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, port))
    while True:
        sleep(1)
        received = s.recv(9999)[:-1]
        print(received)
        received = parse(received)
        result = solve(received)
        print(result)
        s.sendall(result + "\n")


main()

```

Co dało nam `ECTF{jk_w3_41n7_s0rrY}`
