import socket
from time import sleep

import re


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("randBox-iw8w3ae3.9447.plumbing", 9447))
    ct = getCiphertext(s)
    breakLevel2(ct, s)
    for i in range(3):
        ct = getCiphertext(s)
        breakLevel3(ct, s)
    ct = getCiphertext(s)
    breakLevel6(ct, s)
    ct = getCiphertext(s)
    breakLevel1(ct, s)
    ct = getCiphertext(s)
    breakLevel7(ct, s)
    ct = getCiphertext(s)
    breakLevel8(ct, s)
    ct = getCiphertext(s)
    breakLevel9(ct, s)
    ct = getCiphertext(s)
    breakLevel7(ct, s)
    sleep(1)
    print(s.recv(1024))


def getCiphertext(s):
    sleep(1)
    data = s.recv(1024)
    print(data)
    m = re.search("encrypts to '(.*)'", data)
    ct = m.group(1)
    print("ciphertext = " + ct)
    return ct


def breakLevel1(ct, s):
    # caesar cipher
    send_via_nc(s, "0")
    data = s.recv(1024)[:-1]
    shift = int(data, 16)
    result = "".join([format((int(letter, 16) - shift) % 16, "x") for letter in ct])
    send_via_nc(s, result)


def breakLevel2(ct, s):
    # circular shifting input by some random number
    send_via_nc(s, "1" + ("0" * (len(ct) - 1)))
    data = s.recv(1024)[:-1]
    shift = data.index("1")
    result = ct[shift:] + ct[:shift]
    send_via_nc(s, result)


def breakLevel3(ct, s):
    # substitution cipher
    initial = "0123456789abcdef"
    send_via_nc(s, initial)
    data = s.recv(1024)[:-1]
    decoder = {data[i]: initial[i] for i in range(len(initial))}
    result = "".join([decoder[letter] for letter in ct])
    send_via_nc(s, result)


def breakLevel6(ct, s):
    # shifting each number by some distance
    initial = "0" * len(ct)
    send_via_nc(s, initial)
    data = s.recv(1024)[:-1]
    shifts = [int(data[i], 16) for i in range(len(ct))]
    result = "".join([format((int(ct[i], 16) - shifts[i]) % 16, "x") for i in range(len(ct))])
    send_via_nc(s, result)


def breakLevel7(ct, s):
    # sub cipher depending on previous number
    cracking_map = {
        '0': {'a': 'a', 'c': 'c', 'b': 'b', 'e': 'e', 'd': 'd', 'f': 'f', '1': '1', '0': '0', '3': '3', '2': '2',
              '5': '5', '4': '4', '7': '7', '6': '6', '9': '9', '8': '8'},
        '1': {'a': 'b', 'c': 'd', 'b': 'a', 'e': 'f', 'd': 'c', 'f': 'e', '1': '0', '0': '1', '3': '2', '2': '3',
              '5': '4', '4': '5', '7': '6', '6': '7', '9': '8', '8': '9'},
        '2': {'a': '8', 'c': 'e', 'b': '9', 'e': 'c', 'd': 'f', 'f': 'd', '1': '3', '0': '2', '3': '1', '2': '0',
              '5': '7', '4': '6', '7': '5', '6': '4', '9': 'b', '8': 'a'},
        '3': {'a': '9', 'c': 'f', 'b': '8', 'e': 'd', 'd': 'e', 'f': 'c', '1': '2', '0': '3', '3': '0', '2': '1',
              '5': '6', '4': '7', '7': '4', '6': '5', '9': 'a', '8': 'b'},
        '4': {'a': 'e', 'c': '8', 'b': 'f', 'e': 'a', 'd': '9', 'f': 'b', '1': '5', '0': '4', '3': '7', '2': '6',
              '5': '1', '4': '0', '7': '3', '6': '2', '9': 'd', '8': 'c'},
        '5': {'a': 'f', 'c': '9', 'b': 'e', 'e': 'b', 'd': '8', 'f': 'a', '1': '4', '0': '5', '3': '6', '2': '7',
              '5': '0', '4': '1', '7': '2', '6': '3', '9': 'c', '8': 'd'},
        '6': {'a': 'c', 'c': 'a', 'b': 'd', 'e': '8', 'd': 'b', 'f': '9', '1': '7', '0': '6', '3': '5', '2': '4',
              '5': '3', '4': '2', '7': '1', '6': '0', '9': 'f', '8': 'e'},
        '7': {'a': 'd', 'c': 'b', 'b': 'c', 'e': '9', 'd': 'a', 'f': '8', '1': '6', '0': '7', '3': '4', '2': '5',
              '5': '2', '4': '3', '7': '0', '6': '1', '9': 'e', '8': 'f'},
        '8': {'a': '2', 'c': '4', 'b': '3', 'e': '6', 'd': '5', 'f': '7', '1': '9', '0': '8', '3': 'b', '2': 'a',
              '5': 'd', '4': 'c', '7': 'f', '6': 'e', '9': '1', '8': '0'},
        '9': {'a': '3', 'c': '5', 'b': '2', 'e': '7', 'd': '4', 'f': '6', '1': '8', '0': '9', '3': 'a', '2': 'b',
              '5': 'c', '4': 'd', '7': 'e', '6': 'f', '9': '0', '8': '1'},
        'a': {'a': '0', 'c': '6', 'b': '1', 'e': '4', 'd': '7', 'f': '5', '1': 'b', '0': 'a', '3': '9', '2': '8',
              '5': 'f', '4': 'e', '7': 'd', '6': 'c', '9': '3', '8': '2'},
        'b': {'a': '1', 'c': '7', 'b': '0', 'e': '5', 'd': '6', 'f': '4', '1': 'a', '0': 'b', '3': '8', '2': '9',
              '5': 'e', '4': 'f', '7': 'c', '6': 'd', '9': '2', '8': '3'},
        'c': {'a': '6', 'c': '0', 'b': '7', 'e': '2', 'd': '1', 'f': '3', '1': 'd', '0': 'c', '3': 'f', '2': 'e',
              '5': '9', '4': '8', '7': 'b', '6': 'a', '9': '5', '8': '4'},
        'd': {'a': '7', 'c': '1', 'b': '6', 'e': '3', 'd': '0', 'f': '2', '1': 'c', '0': 'd', '3': 'e', '2': 'f',
              '5': '8', '4': '9', '7': 'a', '6': 'b', '9': '4', '8': '5'},
        'e': {'a': '4', 'c': '2', 'b': '5', 'e': '0', 'd': '3', 'f': '1', '1': 'f', '0': 'e', '3': 'd', '2': 'c',
              '5': 'b', '4': 'a', '7': '9', '6': '8', '9': '7', '8': '6'},
        'f': {'a': '5', 'c': '3', 'b': '4', 'e': '1', 'd': '2', 'f': '0', '1': 'e', '0': 'f', '3': 'c', '2': 'd',
              '5': 'a', '4': 'b', '7': '8', '6': '9', '9': '6', '8': '7'}
    }
    initial = "0"
    send_via_nc(s, initial)
    data = s.recv(1024)
    data = data[:data.index("\n")]
    current_number = find_start_number(cracking_map, data)
    result = ""
    for letter in ct:
        generator = find_generator(cracking_map, current_number, letter)
        result += generator
        current_number = generator
    send_via_nc(s, result)


def find_start_number(cracking_map, result):
    for cracking_entry in cracking_map.items():
        initial_letter = cracking_entry[0]
        correspondence_map = cracking_entry[1]
        if correspondence_map['0'] == result:
            return initial_letter


def find_generator(cracking_map, current_number, result):
    correspondence_map = cracking_map[current_number]
    for entry in correspondence_map.items():
        generator = entry[0]
        value = entry[1]
        if value == result:
            return generator


def breakLevel8(ct, s):
    # adding current number to previous modulo 16
    initial = "0"
    send_via_nc(s, initial)
    data = s.recv(1024)
    data = data[:data.index("\n")]
    previous = int(data, 16)
    result = ""
    for number in ct:
        current = int(number, 16)
        missing = (current - previous) % 16
        result += format(missing, "x")
        previous = current
    send_via_nc(s, result)


def breakLevel9(ct, s):
    # substitution with byte swap, x->1, y->2, xy -> 21
    initial = "0123456789abcdef"
    send_via_nc(s, initial)
    data = s.recv(1024)
    data = data[:data.index("\n")]
    substitution = {}
    for i in range(0, len(initial) - 1, 2):
        substitution[initial[i + 1]] = data[i]
        substitution[initial[i]] = data[i + 1]
    result = ""
    for i in range(0, len(ct) - 1, 2):
        first = ct[i]
        second = ct[i + 1]
        result += substitution[second] + substitution[first]
    send_via_nc(s, result)


def breakInteractive(ct, s):
    while True:
        query = raw_input()
        send_via_nc(s, query)
        sleep(1)
        data = s.recv(1024)
        print(data)


def send_via_nc(s, data):
    print("sending "+data)
    s.sendall(data + "\n")


main()
