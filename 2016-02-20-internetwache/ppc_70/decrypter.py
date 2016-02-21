import re
import socket
from time import sleep


def encode(eq):
    b = encode1(eq)
    return encode2(b)


def encode1(eq):
    out = []
    for c in eq:
        q = bin((ord(c) ^ 32)).lstrip("0b")
        q = "0" * (8 - len(q)) + q
        out.append(q)
    b = ''.join(out)
    return b


def decode1(b):
    result = []
    for i in range(0, len(b), 8):
        q = b[i:i + 8]
        q = chr(int(q, 2) ^ 32)
        result.append(q)
    return "".join(result)


def encode2(b):
    pr = []
    for x in range(0, len(b), 2):
        c = chr(int(b[x:x + 2], 2) + 51)
        pr.append(c)
    s = '.'.join(pr)
    return s


def decode2(task):
    return "".join("{0:02b}".format((ord(c) - 51)) for c in task.split("."))


def decode(task):
    b = decode2(task)
    return decode1(b)


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("188.166.133.53", 11071))
    cipher_regex = "Level \d+\.: (.*)"
    initial_data = str(s.recv(4096))
    print(initial_data)
    while True:
        sleep(1)
        task = str(s.recv(4096))
        m = re.search(cipher_regex, task)
        print(task)
        ciphertext = m.group(1)
        decoded = decode(ciphertext)
        print(decoded)
        x = calculate_equation(decoded)
        s.sendall(encode(str(x)) + "\n")
    pass


def calculate_equation(task):
    equation_regex = "x (.) (\d+) = (.+)"
    m = re.search(equation_regex, task)
    operation = m.group(1)
    operand = int(m.group(2))
    result = int(m.group(3))
    x = result
    if operation == "+":
        x = result - operand
    elif operation == "-":
        x = result + operand
    elif operation == "*":
        x = result / operand
    elif operation == "/":
        x = result * operand
    return x

main()

#IW{Crypt0_c0d3}