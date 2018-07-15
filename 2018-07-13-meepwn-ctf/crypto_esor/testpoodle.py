#!/usr/bin/python2
from Crypto.Cipher import AES
import hmac, hashlib
import os
import sys

menu = """Choose one:
1. encrypt data
2. decrypt data
3. quit
"""

class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)
sys.stderr = None

encrypt_key = '\xff' * 32
secret = 'MeePwnCTF{#flag_here#}'
hmac_secret = ''
blocksize = 16
hmac_size = 20

def pad(msg):
	padlen = blocksize - (len(msg) % blocksize) - 1
	return os.urandom(padlen) + chr(padlen)

def unpad(msg):
	return msg[:-(ord(msg[-1]) + 1)]

def compute_hmac(msg):
	return hmac.new(hmac_secret, msg, digestmod=hashlib.sha1).digest()

def encrypt(prefix='', suffix=''):
	_enc = prefix + secret + suffix
	_enc+= compute_hmac(_enc)
	_enc+= pad(_enc)
	iv = os.urandom(16)
	_aes = AES.new(encrypt_key, AES.MODE_CBC, iv)
	return (iv + _aes.encrypt(_enc)).encode('hex')

def decrypt(data):
	data = data.decode('hex')
	try:
		iv = data[:blocksize]
		_aes = AES.new(encrypt_key, AES.MODE_CBC, iv)
		data = _aes.decrypt(data[blocksize:])
		data = unpad(data)
		plaintext = data[:-hmac_size]
		mac = data[-hmac_size:]
		if mac == compute_hmac(plaintext): return True
		else: return False
	except: return False

print """Welcome to our super secure enc/dec server. 
We use hmac, so, plz don't hack us (and you can't). Thanks."""

while True:
	choice = int(raw_input(menu))
	if choice == 1:
		_pre = raw_input('prefix: ')
		_suf = raw_input('suffix: ')
		print encrypt(prefix=_pre, suffix=_suf)
	elif choice == 2:
		_data = raw_input('data: ')
		if decrypt(_data):
			print 'OK'
		else:
			print 'KO'
	elif choice == 3:
		sys.exit(0)
	else:
		choice = int(raw_input(menu))