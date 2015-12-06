import re
import threading
from time import sleep
import math
import requests

lower_bound = 0
bound_lock = threading.Lock()


def seed_collector():
    global bound_lock
    global lower_bound
    while True:
        url = "http://pailler.quals.seccon.jp/cgi-bin/pq.cgi"
        data = str(requests.get(url).content)
        c, o, h = map(int, re.findall("\d+", data))
        potential_n = int(math.sqrt(max([c, o, h])))
        bound_lock.acquire()
        if potential_n > lower_bound:
            lower_bound = potential_n
            print("new lower bound " + str(lower_bound))
        bound_lock.release()
        print(c, o, h)
        sleep(3)


def bruter():
    global lower_bound
    global bound_lock
    bound = 1
    while True:
        bound_lock.acquire()
        current = max([bound, lower_bound])
        lower_bound = current
        if valid_n(lower_bound):
            print("n=" + str(lower_bound))
            return
        else:
            lower_bound += 1
        bound_lock.release()


def valid_n(n):
    return ((4329821979223433093 * 5091080979048341208) % (n * n) == 2181673299914317485)


def main():
    threading.Thread(target=seed_collector, args=[]).start()
    threading.Thread(target=bruter, args=[]).start()

# main()

def egcd(a, b):
    u, u1 = 1, 0
    v, v1 = 0, 1
    while b:
        q = a // b
        u, u1 = u1, u - q * u1
        v, v1 = v1, v - q * v1
        a, b = b, a - q * b
    return a, u, v


def modinv(n, e):
    _gcd, d, _2 = egcd(e, n)
    if d < 0:
        d += n
    return d


def L(u, n):
    return int((u - 1) / n)


def breaker():
    p, q = 42727, 58757
    n = 2510510339
    lbd = 1255204428  # lcm(p-1, q-1)
    g = n + 1
    x = L(pow(g, lbd, n * n), n)
    mi = int(modinv(n, x))
    c = 2662407698910651121  # przykladowy ciphertext
    m = L(pow(c, lbd, n * n), n) * pow(mi, 1, n)
    print(m % n)


breaker()
#1510490612
#SECCON{SECCoooo_oooOooo_ooooooooN}