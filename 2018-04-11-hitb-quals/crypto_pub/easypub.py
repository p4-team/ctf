from Crypto.PublicKey import RSA, ElGamal
from Crypto.Util.number import bytes_to_long, long_to_bytes, GCD, inverse, size
from Crypto import Random
from hashlib import sha256
from time import time
from random import randint, seed
from signal import alarm
from os import urandom


class cipher(object):
    def __init__(self):
        self.rsa = RSA.generate(1024)
        self.elgamal = ElGamal.generate(128, Random.new().read)

    def encrypt(self, msg):
        return self.rsa.encrypt(msg, None)[0]

    def decrypt(self, sec):
        return self.rsa.decrypt(sec)

    def sign(self, msg):
        msg = long_to_bytes(msg)
        h = sha256(msg).digest()

        seed(time())
        k = randint(1, self.elgamal.p - 1)
        while GCD(k, self.elgamal.p - 1) != 1:
            k = randint(1, self.elgamal.p - 1)

        return self.elgamal.sign(h, k)

    def verify(self, msg, sig):
        msg = long_to_bytes(msg)
        h = sha256(msg).digest()
        return self.elgamal.verify(h, sig)


def main():
    with open('admin.key', 'r') as f:
        admin_k = f.readline()
    cry = cipher()
    print('welcome to Fantasy Terram')
    print(cry.rsa.e)
    print(cry.rsa.n)
    print(cry.elgamal.p)
    print(cry.elgamal.g)
    print(cry.elgamal.y)

    alarm(200)
    while True:
        choice = input("Please [r]egister or [l]ogin :>>")

        if not choice:
            break
        if choice[0] == 'r':
            r = randint(1, 3)
            # if r in(2, 3):
            #     print('Sorry, you cannot register now. Good luck.')
            #     exit()
            name = input('please input your username:>>')
            name = bytes(name, 'ISO-8859-1')
            if name == b'admin':
                tmp = input("please impurt admin's key:>>")
                if tmp != admin_k:
                    print('Liar! Get out of here!')
                    exit()
                else:
                    print('Welcom admin!')
                    with open('flag', 'r') as f:
                        print(f.readline())
                        exit()
            msg = name + b'\x00' + bytes(admin_k, 'ISO-8859-1')
            if size(bytes_to_long(msg)) > 700:
                print('Too long username')
                continue
            msg = msg + urandom(120 - len(msg))
            msg = bytes_to_long(msg)
            if msg % 2 == 1:
                msg += 1
            sig = cry.sign(msg)
            ticket = cry.encrypt(msg)
            print(ticket)
            print(sig[0])
            print(sig[1])

        elif choice[0] == 'l':
            ticket = int(input('ticket:>>'))
            sig0 = int(input('sig[0]'))
            sig1 = int(input('sig[1]'))
            msg = cry.decrypt(ticket)
            if msg % 2 == 1:
                print('A bit is wrong, may be something is wrong.')
                continue
            if cry.verify(msg, (sig0, sig1)) == cry.verify(msg, (sig1, sig0)):
                print('Wrong signature!')
            msg = long_to_bytes(msg)
            name = msg.split(b'\x00')[0]
            print('Welcome!{}'.format(name))
        else:
            break


if __name__ == '__main__':
    main()
