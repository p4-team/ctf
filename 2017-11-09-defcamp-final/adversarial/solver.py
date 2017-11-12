import numpy as np
import json
from crypto_commons.netcat.netcat_commons import nc, send, receive_until_match


def solve(feats):
    return [-1 if feats[i] < 0 else 1 for i in range(len(feats))]


def get_probability(z):
    return 1. / (1 + np.exp(-(z)))


def fit(X, feats, target):
    y = []
    for i in range(0, len(feats)):
        y.append(get_probability(np.dot(X, feats[i])))
    return 1. - float(y[target])


def cmd_hi(s):
    send(s, "hi")
    response = ""
    while ']]' not in response:
        response += s.recv(9999999)
    feats = json.loads(response)
    return feats


def cmd_target(s):
    send(s, "target")
    response = s.recv(9999)
    target = int(response)
    return target


def attack(s):
    response = receive_until_match(s, "Welcome to the server. \n")
    print(response)
    feats = cmd_hi(s)
    target = cmd_target(s)
    print target
    solution = solve(feats[target])
    print(solution)
    print(fit(solution, feats, target))
    send(s, "answer " + " ".join(map(str, solution)))
    print(s.recv(9999))


def main():
    s = nc("adversarial.dctf-f1nals-2017.def.camp", 6666)
    for i in range(30):
        attack(s)


main()
