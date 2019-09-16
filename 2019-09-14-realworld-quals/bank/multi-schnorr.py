import os
import SocketServer
import base64 as b64
import hashlib
from Crypto.Util import number
from Crypto import Random
from Crypto.PublicKey.pubkey import *
import datetime
import calendar

from schnorr import *

MSGLENGTH = 40000
HASHLENGTH = 16
FLAG = open("flag","r").read()
PORT_NUM = 20014

def digitalize(m):
    return int(m.encode('hex'), 16)

class HandleCheckin(SocketServer.StreamRequestHandler):
    def handle(self):
        Random.atfork()
        req = self.request
        proof = b64.b64encode(os.urandom(12))

        req.sendall(
            "Please provide your proof of work, a sha1 sum ending in 16 bit's set to 0, it must be of length %d bytes, starting with %s\n" % (
            len(proof) + 5, proof))

        test = req.recv(21)
        ha = hashlib.sha1()
        ha.update(test)

        if (test[0:16] != proof or ord(ha.digest()[-1]) != 0 or ord(ha.digest()[-2]) != 0): # or ord(ha.digest()[-3]) != 0 or ord(ha.digest()[-4]) != 0):
            req.sendall("Check failed")
            req.close()
            return

        req.sendall("Generating keys...\n")
        sk, pk = generate_keys()
        balance = 0
        while True:
                req.sendall("Please tell us your public key:")
                msg = self.rfile.readline().strip().decode('base64')
                if len(msg) < 6 or len(msg) > MSGLENGTH:
                    req.sendall("what are you doing?")
                    req.close()
                    return
                userPk = (int(msg.split(',')[0]), int(msg.split(',')[1]))
                req.sendall('''User logged in.

                [Beep]

    Please select your options:

    1. Deposit a coin into your account, you can sign a message 'DEPOSIT' and send us the signature.
    2. Withdraw a coin from your account, you need to provide us a message 'WITHDRAW' signed by both of you and our RESPECTED BANK MANAGER.
    3. Find one of our customer support representative to assist you.


    Our working hour is 9:00 am to 5:00 pm every %s!
    Thank you for being our loyal customer and your satisfaction is our first priority!
    ''' % calendar.day_name[(datetime.datetime.today() + datetime.timedelta(days=1)).weekday()])
                msg = self.rfile.readline().strip().decode('base64')
                if msg[0] == '1':
                    req.sendall("Please send us your signature")
                    msg = self.rfile.readline().strip().decode('base64')
                    if schnorr_verify('DEPOSIT', userPk, msg):
                        balance += 1
                    req.sendall("Coin deposited.\n")
                elif msg[0] == '2':
                    req.sendall("Please send us your signature")
                    msg = self.rfile.readline().strip().decode('base64')
                    if schnorr_verify('WITHDRAW', point_add(userPk, pk), msg) and balance > 0:
                        req.sendall("Here is your coin: %s\n" % FLAG)
                elif msg[0] == '3':
                    req.sendall("The custom service is offline now.\n\nBut here is our public key just in case a random guy claims himself as one of us: %s\n" % repr(pk))


class ThreadedServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", int(PORT_NUM)
    server = ThreadedServer((HOST, PORT), HandleCheckin)
    server.allow_reuse_address = True
    server.serve_forever()

