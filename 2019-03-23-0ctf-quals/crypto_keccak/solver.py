import hashlib
import itertools
import re
import string
from multiprocessing import freeze_support
from os import urandom
from time import time, sleep

from crypto_commons.brute.brute import brute
from crypto_commons.generic import xor_hex
from crypto_commons.netcat.netcat_commons import nc, receive_until_match, send, interactive

full = 1600
capacity = 48
rate = full - capacity


def ROL64(a, n):
    return ((a >> (64 - (n % 64))) + (a << (n % 64))) % (1 << 64)


def KeccakF1600onLanes(lanes):
    R = 1
    for round in range(24):
        # θ
        C = [lanes[x][0] ^ lanes[x][1] ^ lanes[x][2] ^ lanes[x][3] ^ lanes[x][4] for x in range(5)]
        D = [C[(x + 4) % 5] ^ ROL64(C[(x + 1) % 5], 1) for x in range(5)]
        lanes = [[lanes[x][y] ^ D[x] for y in range(5)] for x in range(5)]
        # ρ and π
        (x, y) = (1, 0)
        current = lanes[x][y]
        for t in range(24):
            (x, y) = (y, (2 * x + 3 * y) % 5)
            (current, lanes[x][y]) = (lanes[x][y], ROL64(current, (t + 1) * (t + 2) // 2))
        # χ
        for y in range(5):
            T = [lanes[x][y] for x in range(5)]
            for x in range(5):
                lanes[x][y] = T[x] ^ ((~T[(x + 1) % 5]) & T[(x + 2) % 5])
        # ι
        for j in range(7):
            R = ((R << 1) ^ ((R >> 7) * 0x71)) % 256
            if (R & 2):
                lanes[0][0] = lanes[0][0] ^ (1 << ((1 << j) - 1))
    return lanes


def load64(b):
    return sum((b[i] << (8 * i)) for i in range(8))


def store64(a):
    return list((a >> (8 * i)) % 256 for i in range(8))


def KeccakF1600(state):
    lanes = [[load64(state[8 * (x + 5 * y):8 * (x + 5 * y) + 8]) for y in range(5)] for x in range(5)]
    lanes = KeccakF1600onLanes(lanes)
    state = bytearray(200)
    for x in range(5):
        for y in range(5):
            state[8 * (x + 5 * y):8 * (x + 5 * y) + 8] = store64(lanes[x][y])
    return state


def Keccak(rate, capacity, inputBytes, delimitedSuffix, outputByteLen):
    outputBytes = bytearray()
    state = bytearray([0 for i in range(200)])
    rateInBytes = rate // 8
    blockSize = 0
    if (((rate + capacity) != 1600) or ((rate % 8) != 0)):
        return
    inputOffset = 0
    # === Absorb all the input blocks ===
    while (inputOffset < len(inputBytes)):
        blockSize = min(len(inputBytes) - inputOffset, rateInBytes)
        for i in range(blockSize):
            state[i] = state[i] ^ inputBytes[i + inputOffset]
        inputOffset = inputOffset + blockSize
        if (blockSize == rateInBytes):
            state = KeccakF1600(state)
            blockSize = 0
        state_hex = str(state).encode("hex")
        c = state[-capacity / 8:]
        # print('state', str(state).encode("hex"))
        # print('c', state[-capacity / 8:])
    # === Do the padding and switch to the squeezing phase ===
    state[blockSize] = state[blockSize] ^ delimitedSuffix
    if (((delimitedSuffix & 0x80) != 0) and (blockSize == (rateInBytes - 1))):
        state = KeccakF1600(state)
    state[rateInBytes - 1] = state[rateInBytes - 1] ^ 0x80
    state = KeccakF1600(state)
    # === Squeeze out all the output blocks ===
    while (outputByteLen > 0):
        blockSize = min(outputByteLen, rateInBytes)
        outputBytes = outputBytes + state[0:blockSize]
        outputByteLen = outputByteLen - blockSize
        if (outputByteLen > 0):
            state = KeccakF1600(state)
    return outputBytes, c, state_hex


def hash(msg):
    return Keccak(rate, capacity, bytearray(msg), 0x06, rate / 8)


def worker(msgs):
    return [(msg, hash(msg)[1]) for msg in msgs]


def collision_search():
    bytes_no = rate / 8
    space = {}
    stage = 1000
    start = 0
    processes = 7
    print("generate space")
    while True:
        print(str(100 * start / (2.0 ** (capacity / 2 + 1))) + "%")
        start += stage
        results = brute(worker, [[urandom(bytes_no) for _ in range(stage)] for _ in range(processes)], processes=processes)
        results = reduce(lambda x, y: x + y, results)
        for (msg, c) in results:
            c = str(c)
            if c in space:
                print(len(space))
                return space[c], msg
            else:
                space[c] = msg


def collide():
    msg, msg2 = collision_search()
    zero = '\0' * (rate / 8)
    _, _, state1 = hash(msg)
    res1, _, _ = hash(msg + zero)
    _, _, state2 = hash(msg2)
    fixer = xor_hex(state1, state2).decode("hex")[:-(capacity / 8)]
    res2, _, _ = hash(msg2 + fixer)
    print(msg, msg2)
    assert msg != msg2
    assert res1 == res2
    return msg + zero, msg2 + fixer


def break_pow(suffix, expected):
    for x in itertools.product(string.ascii_letters + string.digits, repeat=4):
        prefix = "".join(list(x))
        h = hashlib.sha256(prefix + suffix).hexdigest()
        if h == expected:
            return prefix


def get_flag(msg1, msg2):
    url = "111.186.63.14"
    port = 10001
    s = nc(url, port)
    challenge = receive_until_match(s, "XXXX:")
    suffix, result = re.findall("sha256\(XXXX\+(.*?)\) == (.*)\s", challenge)[0]
    print(suffix, result)
    prefix = break_pow(suffix, result)
    print(prefix)
    send(s, prefix)
    send(s, msg1)
    sleep(1)
    send(s, msg2)
    print(interactive(s))


def main():
    start = time()
    m1, m2 = collide()
    print(m1.encode("hex"))
    print(m2.encode("hex"))
    stop = time()
    print('found in', stop - start)
    get_flag(m1, m2)


def sanity():
    msg = urandom(rate / 8)
    _, c, state1 = hash(msg)
    while True:
        msg2 = urandom(rate / 8)
        _, c2, state2 = hash(msg2)
        if c == c2:
            break
    zero = '\0' * (rate / 8)
    res1, _, _ = hash(msg + zero)
    fixer = xor_hex(state1, state2).decode("hex")[:-(capacity / 8)]
    res2, _, _ = hash(msg2 + fixer)
    print('res1', res1)
    print('res2', res2)
    assert res1 == res2
    assert msg != msg2


def sanity2():
    start = time()
    m1, m2 = collide()
    stop = time()
    print('found in', stop - start)
    assert m1 != m2
    assert hash(m1) == hash(m2)


if __name__ == '__main__':
    freeze_support()
    # sanity()
    # sanity2()

    # main()

    msg1 = '2ac79b239ee01b3da93a9ed8edf4d035240d03360ab7f2a90fd7797135bde103b35e08e0a60b49694d8d02acc896261f589e3320e2d7ec55d3661d3dc57716f6047b26b47d2c22fe5a8d17de4c7e9dd98d2b45f3add9503b1797d225df55116a9d4f4105442145af5d2eed582b3b2812d70eea058faeab04245b762c6993f705685e3c5e2d6488f92068b5c23b9df115938fe512cf4b24ffb80b73a45b492d1360e9de6263d8d8effd3cb2c04b5f80eb2cb8dcab0f6bba8319ba327dfc447937fd870000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    msg2 = '4cf30b4f6c5bea3644e4f7093365fc9808dec255b7930c76d4609b41edac3b3c27ab9330684f5cd6c2ab110f982ba8bf218a8a186a90bb9dbaa0f8592c64d9b4979d76b06f66660bb25fc7ec35ed57d02b53350a976fef12b902e867a4d0ac3b5f22e1571b278e5fd2c38fcce79a6e55d5ab8cc1b1e25ea245e395db388e7e0837215f253448c514049780a448c62793c01740123d5a4d6725787130c89b6b53e6fb92398f082d94301f9d6be304cada2cec6537a1db810e2d47d433e85691b209aabf987d2680385b78405abbc0b0fc8315b39d991b13c6b0f13697e1010b1e1da9b482fe966760b4322aa1f5912cfe4e86eb8addc626182d9b2cdb6f4e512e0ab8cff95b51008b5c0003fc64c38c25ab0a3b9e2ba6d959fb781d26472303cdd3404aa0b8552e5c5698837430ca5fd6600a65268e35c002e876f85ecd25a425997dbb8e35f325019cc5777d3ed65f96ce91a2d9b5f6b0e42a9946465c71104c18e067693469b347c48ad429034f7e7d2d87fd97a4fa0bc631b3440b38bdaa1edd0f694c'
    get_flag(msg1, msg2)
