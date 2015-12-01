#!/usr/bin/python

import time;
import random;
FLAG = '';

def cycleLen(data, place):
	seen = {};
	count = 0;
	while not place in seen:
		seen[place] = 1;
		count += 1;
		place = data[place];
	return count;

def realSign(data):
	res = 1;
	for i in range(256):
		res *= cycleLen(map(ord, data), i);
	return res;


import base64, SocketServer, os, sys, hashlib;

class ServerHandler(SocketServer.BaseRequestHandler):

	def fail(self, message):
		self.request.sendall(message + "\n");
		self.request.close();

	def pow(self):
		proof = base64.b64encode(os.urandom(9));
		self.request.sendall(proof);
		test = self.request.recv(20);
		ha = hashlib.sha1();
		ha.update(test);
		if test[0:12] != proof or not ha.digest().endswith('\x00\x00\x00'):
			self.fail("Bad proof of work.");

	def sign(self, invalid):
		data = base64.b64decode(self.request.recv(172));
		if len(data) != 128:
			self.fail("Bad data");
			return;
		if data == invalid:
			self.fail("Same data");
			return;
		self.request.sendall(str(realSign(self.SECRET + data)) + "\n");
	
	def check(self, compare):
		sig = int(self.request.recv(620));
		return sig == realSign(self.SECRET + compare);

	def handle(self):
		#self.pow();
		self.SECRET = os.urandom(128);
		self.TO_SIGN = os.urandom(128);
		self.request.sendall("You need to sign:\n");
		self.request.sendall(base64.b64encode(self.TO_SIGN));
		for i in range(256):
			self.request.sendall("\n1) Sign something\n2) Give me signiture of data\n");
			op = int(self.request.recv(2));
			if op == 1:
				self.sign(self.TO_SIGN);
			elif op == 2:
				if self.check(self.TO_SIGN):
					self.request.sendall(FLAG);
				break;
			else:
				self.fail("Bad option");
				break;
		self.request.close();


class ThreadedServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
	pass;

if __name__ == "__main__":
	HOST = sys.argv[1];
	PORT = int(sys.argv[2]);

	FLAG = open('flag.txt', 'r').read();
	server = ThreadedServer((HOST, PORT), ServerHandler);
	server.allow_reuse_address = True;
	server.serve_forever();
