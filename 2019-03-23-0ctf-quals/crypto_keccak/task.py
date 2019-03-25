import os,random,sys,string
from hashlib import sha256
import SocketServer

import CompactFIPS202
from flag import FLAG

class Task(SocketServer.BaseRequestHandler):
    def proof_of_work(self):
        proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in xrange(20)])
        digest = sha256(proof).hexdigest()
        self.request.send("sha256(XXXX+%s) == %s\n" % (proof[4:],digest))
        self.request.send('Give me XXXX:')
        x = self.request.recv(10)
        x = x.strip()
        if len(x) != 4 or sha256(x+proof[4:]).hexdigest() != digest: 
            return False
        return True

    def recvhex(self, sz):
        try:
            r = sz
            res = ''
            while r>0:
                res += self.request.recv(r)
                if res.endswith('\n'):
                    r = 0
                else:
                    r = sz - len(res)
            res = res.strip()
            res = res.decode('hex')
        except:
            res = ''
        return res

    def dosend(self, msg):
        try:
            self.request.sendall(msg)
        except:
            pass

    def dohash(self, msg):
        return CompactFIPS202.Keccak(1552, 48, bytearray(msg), 0x06, 32)

    def handle(self):
        if not self.proof_of_work():
            return
        self.request.settimeout(3)
        self.dosend("first message(hex): ")
        msg0 = self.recvhex(8000)
        self.dosend("second message(hex): ")
        msg1 = self.recvhex(8000)
        if msg0!=msg1 and self.dohash(msg0) == self.dohash(msg1):
            self.dosend("%s\n" % FLAG)
        else:
            self.dosend(">.<\n")
        self.request.close()


class ForkingServer(SocketServer.ForkingTCPServer, SocketServer.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10001
    print HOST
    print PORT
    server = ForkingServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
