#/usr/bin/env python

from Crypto.Random import random, atfork
from Crypto.Util.number import bytes_to_long, long_to_bytes
from hashlib import sha1

import SocketServer,threading,os,time
import signal

from util import *
from key import *

PORT = 7763
FLAG = "REDACTED"
msg = """Welcome to the LSB oracle! N = {}\n""".format(N)

def pad(s):
    assert(len(s) < N.bit_length() / 8)
    padded = bytes_to_long(s.ljust(N.bit_length()/8, padchar))
    while decrypt(padded, p, q) == None:
        padded += 1
    return padded

padded = pad(FLAG)
enc_flag = encrypt(padded, N)

assert long_to_bytes(padded)[:len(FLAG)] == FLAG
assert decrypt(enc_flag, p, q) == padded
assert decrypt(2, p, q) != None

def proof_of_work(req):
    import string
    req.sendall("Before we begin, a quick proof of work:\n")
    prefix = "".join([random.choice(string.digits + string.letters) for i in range(10)])
    req.sendall("Give me a string starting with {}, of length {}, such that its sha1 sum ends in ffffff\n".format(prefix, len(prefix)+5))
    response = req.recv(len(prefix) + 5)
    if sha1(response).digest()[-3:] != "\xff"*3 or not response.startswith(prefix):
        req.sendall("Doesn't work, sorry.\n")
        exit()

class incoming(SocketServer.BaseRequestHandler):
    def handle(self):
        atfork()
        req = self.request
        signal.alarm(60)

        def recvline():
            buf = ""
            while not buf.endswith("\n"):
                buf += req.recv(1)
            return buf

        proof_of_work(req)

        signal.alarm(120)

        req.sendall(msg)

        req.sendall("Encrypted Flag: {}\n".format(enc_flag))
        while True:
            req.sendall("Give a ciphertext: ")
            x = long(recvline())
            m = decrypt(x, p, q)
            if m == None:
                m = 0
            req.sendall("lsb is {}\n".format(m % 2))

        req.close()

class ReusableTCPServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
  pass

SocketServer.TCPServer.allow_reuse_address = True
server = ReusableTCPServer(("0.0.0.0", PORT), incoming)

print "Listening on port %d" % PORT
server.serve_forever()
