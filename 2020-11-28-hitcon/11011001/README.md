# 11011001, reverse, 255p

> 0100111001101111001000000110100001101001011011100111010000100000011010000110010101110010011001010010110000100000011101110110100001100001011101000010000001100001011100100110010100100000011110010110111101110101001000000110010101111000011100000110010101100011011101000110100101101110011001110010000001100110011011110111001000111111

The hint is useless, so we've got to reverse the binary.  The binary expects 20 integers from us, on which it performs some checks.
The most useful way to visualize the input is 20x20 binary matrix with the following rules:
* each column and row has 10 ones and 10 zeroes
* no column or row can have three consecutive ones or zeroes in a row
* no column can repeat
* no row can repeat
* there are some bits that are fixed to one or zero

I actually missed the last two rules accidentally, but it appears my solver got the unique solution anyway.
The riddle is a bit similar to sudoku, so I implemented a backtracking solver in Python. Whenever one of the squares is forced to be 0 or 1,
we put it; otherwise, we just simulate both options for an arbitrary square. I guess if I implemented all the rules, guessing would not be necessary...

```python3

known = [
0x81002, 0x1000, 0x29065, 0x29061, 0x2, 2, 0x16C40, 0x16C00,
0x20905, 0x805, 0x10220, 0x220, 0x98868, 0x80860, 0x21102,
0x21000, 0x491, 0x481, 0x31140, 0x1000, 0x801, 0x0, 0x60405,
0x400, 0x0C860, 0x60, 0x508, 0x400, 0x40900, 0x800, 0x12213,
0x10003, 0x428C0, 0x840, 0x840C, 0x0C, 0x43500, 0x2000, 0x8105A,
0x1000,]

def is_good(board):
    for row in board:
        cnt1, cnt0 = 0, 0
        prev2, prev = None, None
        for x in row:
            if x == "1":
                cnt1 += 1
            if x == "0":
                cnt0 += 1
            if x == prev and prev == prev2 and prev in "01":
                return False
            prev2, prev = prev, x
        if cnt1 > 10 or cnt0 > 10:
            return False

    for col in range(20):
        cnt1, cnt0 = 0, 0
        prev2, prev = None, None
        for row in board:
            if row[col] == "1":
                cnt1 += 1
            if row[col] == "0":
                cnt0 += 1
            if row[col] == prev and prev == prev2 and prev in "01":
                return False
            prev2, prev = prev, row[col]
        if cnt1 > 10 or cnt0 > 10:
            return False
    return True

board = [["."]*20 for i in range(20)]

for i in range(20):
    mask = known[2*i]
    res = known[2*i+1]
    print("{:020b}".format(mask))
    print("{:020b}".format(res))
    print()
    for j in range(20):
        if (1<<j)&mask:
            board[i][j] = str((res>>j)&1)

for row in board:
    print("".join(row))


def dfs():
    missing = 0
    for i in range(20):
        for j in range(20):
            if board[i][j] not in "01":
                missing += 1
                board[i][j] = "0"
                n0 = is_good(board)
                board[i][j] = "1"
                n1 = is_good(board)
                board[i][j] = "."
                if n0 == False and n1 == False:
                    return False
                if n0 == True and n1 == False:
                    board[i][j] = "0"
                    r = dfs()
                    board[i][j] = "."
                    return r
                if n0 == False and n1 == True:
                    board[i][j] = "1"
                    r = dfs()
                    board[i][j] = "."
                    return r
    print(missing)
    for i in range(20):
        for j in range(20):
            if board[i][j] not in "01":
                board[i][j] = "0"
                n0 = dfs()
                board[i][j] = "1"
                n1 = dfs()
                board[i][j] = "."
                return n0 or n1
    print(board)
    raise Exception("asd")

            



dfs()
```
