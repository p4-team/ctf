import Crypto
from Crypto.PublicKey import RSA
import threading
import socket
import sys
import os

# e = 8257e5269cc0cdb32271154d4f5df508380e27b8826798c7271a237ff9e4191cc047629cf9684703f4826df1c69a1cfe786841d191757515abfe1a09d8bef7d92b40c6b37377e3218b109cfa734802ec418c2e08468ffcf6c11a1314600fce6714fa10fb3d5ed4a7ca89d69dc66d1f34aa9acbc8830b3319d281e0defc393ecb
# n = cd67fc599866f87bc45ff87c1634aa144ee257c963ab2541052f3b38d22a11b255b0dd9318153699664b1007b7f38118df77f703909888c3930b73221c57828fc423a643b1eaf47f03d6c24b11d907f979dae4aa47347959c7c77bda8f9804dd95cc438d75ced522c7391a5d1432978440bfacc9939a33d6e6e058b15a084f99

class ClientThread(threading.Thread):

    def __init__(self,ip,port,socket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        self.keysFile = "/home/challenge/keys.txt"
        self.encrypted_flag_file = "/home/challenge/flag.encrypted"
        print "[+] New thread started for "+ip+":"+str(port)

    def run(self):
        print "Connection from : "+ip+":"+str(port)
        original_ctext = open(self.encrypted_flag_file, 'r').readline()
        self.socket.send("Enter cipher text for which you want the plaintext.\n")
        ct = self.socket.recv(1024).strip()
        print ct
        if ct == original_ctext:
            self.socket.send("Enter a different ciphertext!\n")
        else:
            parameters = open(self.keysFile, 'r').readlines()
            for i in range(len(parameters)):
                parameters[i] = int(parameters[i], 16)
            parameter_tuple = tuple(parameters)
            key = RSA.construct(parameter_tuple)
            try:
                decrypted = key.decrypt(ct.decode('hex'))
                self.socket.send("Plaintext: %s" % decrypted.encode('hex'))
            except:
                self.socket.send("Invalid" + "\n")
                self.socket.close()

        print "Client disconnected..."
        self.socket.close()

host = "0.0.0.0"
port = 18734

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcpsock.bind((host,port))
threads = []

while True:
    tcpsock.listen(4)
    print "\nListening for incoming connections..."
    (clientsock, (ip, port)) = tcpsock.accept()

    # Let's use a new thread for each incoming connection
    newthread = ClientThread(ip, port, clientsock)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()