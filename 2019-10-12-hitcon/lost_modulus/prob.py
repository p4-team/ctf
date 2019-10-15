from Crypto.Util.number import *


class Key:
    def __init__(self, bits):
        assert bits >= 512
        self.p = getPrime(bits)
        self.q = getPrime(bits)
        self.n = self.p * self.q
        self.e = 0x100007
        self.d = inverse(self.e, (self.p-1)*(self.q-1))
        self.dmp1 = self.d%(self.p-1)
        self.dmq1 = self.d%(self.q-1)
        self.iqmp = inverse(self.q, self.p)
        self.ipmq = inverse(self.p, self.q)

    def encrypt(self, data):
        num = bytes_to_long(data)
        result = pow(num, self.e, self.n)
        return long_to_bytes(result)

    def decrypt(self, data):
        num = bytes_to_long(data)
        v1 = pow(num, self.dmp1, self.p)
        v2 = pow(num, self.dmq1, self.q)
        result = (v2*self.p*self.ipmq+v1*self.q*self.iqmp) % self.n
        return long_to_bytes(result)

    def __str__(self):
        return "Key([e = {0}, n = {1}, x = {2}, y = {3}])".format(self.e, self.d, self.iqmp, self.ipmq)

def main():
    key = Key(1024)
    flag = open('flag').read()
    encrypt_flag = key.encrypt(flag)
    assert key.decrypt(encrypt_flag) == flag
    print key
    print encrypt_flag.encode('hex')


if __name__ == '__main__':
    main()
