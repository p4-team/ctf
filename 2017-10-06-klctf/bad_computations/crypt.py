from random import choice
from sys import argv
from base64 import b64encode


b = 22


def dwfregrgre(x, z):
    wdef = []
    for a in range(x, z + 1):
        for i in range(2, a):
            if (a % i) == 0:
                break
        else:
            wdef.append(a)

    return wdef


def sdsd(edefefef):
    fvfegve = [x for x in range(2, edefefef)]

    x = 2
    rrerrrr = True
    while rrerrrr:
        for i in range(x * x, edefefef, x):
            if i in fvfegve:
                fvfegve.remove(i)

        rrerrrr = False
        for i in fvfegve:
            if i > x:
                x = i
                rrerrrr = True
                break

    return fvfegve


def swsdwd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = swsdwd(b % a, a)
        return (g, x - (b // a) * y, y)

def swsdwdwdwa(a, m):
    g, x, y = swsdwd(a, m)
    if g != 1:
        raise Exception('Oops! Error!')
    else:
        return x % m

def L(u, n):
    return (u - 1) // n


if __name__ == '__main__':
    print("Key cryptor v1.0")

    if len(argv) != 2:
        print("Start script like: python crypt.py <YourOwnPasswordString>")

    if (not str(argv[1]).startswith("KLCTF{")) or (not str(argv[1]).endswith("}")):
        print("Error! Password must starts with KLCTF")
        exit()

    p = choice(dwfregrgre(100, 1000))
    q = choice(dwfregrgre(200, 1000))

    print("Waiting for encryption...")

    n = p * q
    g = None
    for i in range(n + 1, n * n):
        if ((i % p) == 0) or ((i % q) == 0) or ((i % n) == 0):
            continue

        g = i
        break

    if g is None:
        print("Error! Can't find g!")
        exit()

    lamb = (p - 1) * (q - 1)
    mu = swsdwdwdwa(L(pow(g, lamb, n * n), n), n) % n

    rc = sdsd(n - 1)
    if len(rc) == 0:
        print("Error! Candidates for r not found!")
        exit()

    if p in rc:
        rc.remove(p)
    if q in rc:
        rc.remove(q)

    r = choice(rc)

    wdwfewgwggrgrg = [ord(x) for x in argv[1][6:-1]]
    dcew = (pow(g, b, (n * n)) * pow(r, n, (n * n))) % (n * n)

    for i in range(len(wdwfewgwggrgrg)):
        wdwfewgwggrgrg[i] = (((pow(g, wdwfewgwggrgrg[i], (n * n)) * pow(r, n, (n * n))) % (n * n)) * dcew) % (n * n)
        wdwfewgwggrgrg[i] = (L(pow(wdwfewgwggrgrg[i], lamb, (n * n)), n) * mu) % n

    wdwfewgwggrgrg = b64encode(bytearray(wdwfewgwggrgrg))
    print(str(wdwfewgwggrgrg)[2:-1])
