import hashlib
import itertools
import re
import sys

from crypto_commons.netcat.netcat_commons import nc, receive_until_match, send, interactive


def pow(suffix, data):
    if 'sha1' in data:
        func = hashlib.sha1
    elif 'sha224' in data:
        func = hashlib.sha224
    elif 'sha256' in data:
        func = hashlib.sha256
    elif 'sha384' in data:
        func = hashlib.sha384
    elif 'sha512' in data:
        func = hashlib.sha512
    elif 'md5' in data:
        func = hashlib.md5
    else:
        return "dupa"
    i = 0
    while True:
        payload = str(i)
        result = func(payload).hexdigest()[-6:]
        if result == suffix:
            return payload
        i += 1


def combine(perm, op, parenthesis1, parenthesis2):
    result = ""
    for i in range(len(op)):
        if parenthesis1 == i and parenthesis1 != parenthesis2:
            result += "(" + str(perm[i]) + str(op[i])
        elif parenthesis2 == i and parenthesis1 != parenthesis2:
            result += str(perm[i]) + ")" + str(op[i])
        else:
            result += str(perm[i]) + str(op[i])
    result = result + str(perm[-1])
    if parenthesis2 == len(perm) - 1:
        result += ")"
    result = result.replace("$", "")
    return result


def calculate(number, i):
    ops = '$%&*+-/<>^|~'
    for perm in itertools.permutations(list(number)):
        for parenthesis1 in range(len(perm) - 1):
            for parenthesis2 in range(parenthesis1, len(perm) - 1):
                for op in itertools.product(list(ops), repeat=len(perm) - 1):
                    equation = combine(perm, op, parenthesis1, parenthesis2)
                    try:
                        if eval(equation) == i:
                            return equation
                    except:
                        pass
    print("No configuration found for " + str(number) + " " + str(i))
    sys.exit(0)


def main():
    host = "37.139.4.247"
    port = 19153
    s = nc(host, port)
    data = receive_until_match(s, "= .*\n")
    print(data)
    suffix = data[-7:-1]
    print(suffix)
    response = pow(suffix, data)
    print('pow', response)
    send(s, response)
    print(receive_until_match(s, "solve"))
    send(s, 'C')
    data = receive_until_match(s, "n = \d+\n")
    print(data)
    number = re.findall("n = (\d+)", data)[0]
    for i in range(101):
        data = receive_until_match(s, "equal to " + str(i))
        print(data)
        response = calculate(number, i)
        print(i, response)
        send(s, response)
    interactive(s)


main()

