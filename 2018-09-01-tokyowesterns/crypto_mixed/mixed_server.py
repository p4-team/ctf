from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes

import random
import signal
import os
import sys

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
privkey = RSA.generate(1024)
pubkey = privkey.publickey()
flag = open('./flag').read().strip()
aeskey = os.urandom(16)
BLOCK_SIZE = 16

def pad(s):
    n = 16 - len(s)%16
    return s + chr(n)*n

def unpad(s):
    n = ord(s[-1])
    return s[:-n]

def aes_encrypt(s):
    iv = long_to_bytes(random.getrandbits(BLOCK_SIZE*8), 16)
    aes = AES.new(aeskey, AES.MODE_CBC, iv)
    return iv + aes.encrypt(pad(s))

def aes_decrypt(s):
    iv = s[:BLOCK_SIZE]
    aes = AES.new(aeskey, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(s[BLOCK_SIZE:]))

def bulldozer(s):
    s = bytearray(s)
    print('Bulldozer is coming!')
    for idx in range(len(s) - 1):
        s[idx] = '#'
    return str(s)

def encrypt():
    p = raw_input('input plain text: ').strip()
    print('RSA: {}'.format(pubkey.encrypt(p, 0)[0].encode('hex')))
    print('AES: {}'.format(aes_encrypt(p).encode('hex')))

def decrypt():
    c = raw_input('input hexencoded cipher text: ').strip().decode('hex')
    print('RSA: {}'.format(bulldozer(privkey.decrypt(c)).encode('hex')))

def print_flag():
    print('here is encrypted flag :)')
    p = flag
    print('another bulldozer is coming!')
    print(('#'*BLOCK_SIZE+aes_encrypt(p)[BLOCK_SIZE:]).encode('hex'))

def print_key():
    print('here is encrypted key :)')
    p = aeskey
    c = pubkey.encrypt(p, 0)[0]
    print(c.encode('hex'))

signal.alarm(300)
while True:
    print("""Welcome to mixed cipher :)
I heard bulldozer is on this channel, be careful!
1: encrypt
2: decrypt
3: get encrypted flag
4: get encrypted key""")
    n = int(raw_input())

    menu = {
        1: encrypt,
        2: decrypt,
        3: print_flag,
        4: print_key,
    }

    if n not in menu:
        print('bye :)')
        exit()
    menu[n]()
