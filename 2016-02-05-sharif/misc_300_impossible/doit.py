import binascii, hashlib, time, string, sys
from ws4py.client.threadedclient import WebSocketClient

CHALLENGE = "0";
RE_ARRANGED = "1";
GIVE_GUESS = "2";
UNACCEPTABLE = "3";
GREATE_GUESS = "4";
WRONG_GUESS = "5";
BYE = "6";
FLAG_IS = "7";

slave=-1
guess=0

class Client(WebSocketClient):
    def closed(self, code, reason=None):
        print "Closed down", code, reason

    def received_message(self, m):
        global slave, guess
        print "Received:"
        m=str(m)
        print m
        code=m[0]
        msg=m[1:]
        if code==CHALLENGE:
            self.auth=True
            i=0
            while True:
                i+=1
                th=hex(i)[2:]
                th="0"*(8-len(th))+th
                chal = hashlib.md5(th).hexdigest()
                chal = bin(int(chal, 16))[2:]
                chal = chal[:22].zfill(22)
                if chal==msg:
                    self.send(th)
                    break
                if i%500000==0:
                    print i
        elif code==RE_ARRANGED:
            print "Rearranged to", msg
            slave+=1
            guess=slave
        elif code==GIVE_GUESS:
            print "Give guess:",msg
            r.send(str(guess))
        elif code==WRONG_GUESS:
            print "Wrong guess:",msg
            guess=int(msg)
        elif code==GREATE_GUESS:
            print "CORRECT!!!!!!!!!!!",msg



r=Client("ws://ctf.sharif.edu:8998", protocols=["http-only", "chat"])
r.connect()
r.run_forever()
