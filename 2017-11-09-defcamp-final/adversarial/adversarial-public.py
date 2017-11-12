#!/usr/bin/python

import numpy as np
import random
import json
import socket
import sys
from thread import *

HOST = ''   
PORT = 6666 
FLAG = ''


Nfeatures  = 100
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
s.listen(10)
print 'Socket now listening'


def generate_features(Nclasses, Nfeatures):
	feats = []
	for i in range(0,Nclasses):
		f = []
		for j in range(0, Nfeatures):
			f.append(random.uniform(-1,1))
		feats.append(f)
	return feats

def get_probability(z):
	return 1./(1+np.exp(-(z)))

def fit(X, feats):
	y = []
	for i in range(0, len(feats)):
		y.append(get_probability(np.dot(X, feats[i])))
	return y

def job(conn):   
	conn.send('Welcome to the server. \n')

	feats        = generate_features(1000, Nfeatures)
	total_solved = 0
	target       = None
	while True:
		data = conn.recv(1024)
		if data.startswith("exit"):
			#print "exit"
			break
		elif data.startswith("hi"):
			#print "hi"
			conn.sendall(json.dumps(feats))
		elif data.startswith("target") and target is None:
			#print "target"
			target = random.randint(0, 1000)
			conn.sendall(str(target))
		elif data.startswith('answer') and target is not None:
			#print "answer"
			X = np.array(data.replace("answer ","").strip().split(" "), dtype=int)
			X = X[X <= 1]
			X = X[X >= -1]
		 		
			if(X.size != Nfeatures):
				break

			y = fit(X, feats)
			conn.sendall(str(1.-float(y[target])))
			if 1.-float(y[target]) <= 0.001:
				total_solved += 1
				target       = None
				conn.sendall("Ok")
			else:
				conn.sendall("Not ok")
				break

		if total_solved == 30:
			conn.sendall(FLAG)
	conn.close()
 
while 1:
	try:
	    conn, addr = s.accept()
	    print 'Connected with ' + addr[0] + ':' + str(addr[1])   
	    start_new_thread(job ,(conn,))
	except KeyboardInterrupt:
		break
s.close()
