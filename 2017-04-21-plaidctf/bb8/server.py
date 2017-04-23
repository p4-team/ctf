#!/usr/bin/env python

import SocketServer,threading,os,socket
from quantum import qubit, Alice, Bob

def recvuntil(s, until, maxlen=2048):
  buf = ''
  while until not in buf and len(buf) < maxlen:
    tmp = s.recv(1)
    if len(tmp) == 0:
      raise socket.error
    buf += tmp
  return buf

class threadedserver(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
  pass

def do_intercept(sock, q, dest):
  if q is not None and q.__class__ != qubit:
    sock.send("There is a classical message (%s) going to %s, do you want to intercept (y/N)? "%(q,dest))
    sock.send(" (Note: if you intercept, the message will not be sent, and only a qubit will)\n")
    r = recvuntil(sock, "\n")
    if not r.lower().startswith("y"):
      return q
    else:
      sock.send("In what basis should the new qubit be prepared? (Z/Y)\n")
      r = recvuntil(sock, "\n")
      basis = "Z" if r.lower().startswith("z") else "Y"
      sock.send("OK, using the %s basis... what should the value be? (-1/1)\n"%basis)
      value = int(recvuntil(sock, "\n"))
      sock.send("OK, we prepared a new qubit in the %s basis with value %d"%(basis, value))
      q = qubit(basis, value)
      return q
  if q is not None:
    sock.send("There is a qubit on the line going to %s, do you want to intercept (y/N)?\n"%dest)
    r = recvuntil(sock, "\n")
    if r.lower().startswith("y"):
      sock.send("OK, intercepting... in which basis shall we measure? (Z/Y)\n")
      r = recvuntil(sock, "\n")
      sock.send("OK, measured %d\nShall we pass this along (N) or replace it (Y)?\n"% \
                q.measure("Z" if r.lower().startswith("z") else "Y"))
      r = recvuntil(sock, "\n")
      if r.lower().startswith("n"):
        sock.send("OK, forwarding the qubit along\n")
      else:
        sock.send("In what basis should the new qubit be prepared? (Z/Y)\n")
        r = recvuntil(sock, "\n")
        basis = "Z" if r.lower().startswith("z") else "Y"
        sock.send("OK, using the %s basis... what should the value be? (-1/1)\n"%basis)
        value = int(recvuntil(sock, "\n"))
        sock.send("OK, we prepared a new qubit in the %s basis with value %d"%(basis, value))
        q = qubit(basis, value)
  else:
    sock.send("The connection has been aborted, do you want to send a qubit to %s anyway? (y/N)\n"%dest)
    r = recvuntil(sock, "\n")
    if r.lower().startswith("y"):
      sock.send("In what basis should the new qubit be prepared? (Z/Y)\n")
      r = recvuntil(sock, "\n")
      basis = "Z" if r.lower().startswith("z") else "Y"
      sock.send("OK, using the %s basis... what should the value be? (-1/1)\n"%basis)
      value = int(recvuntil(sock, "\n"))
      sock.send("OK, we prepared a new qubit in the %s basis with value %d"%(basis, value))
      q = qubit(basis, value)
    else:
      sock.send("OK, forwarding along the abort\n")
  return q


class incoming(SocketServer.BaseRequestHandler):
  def handle(self):
    self.request.settimeout(10*60)
    self.request.send("Welcome to the\n")
    self.request.send("Q U A N T U M    K E Y   I N T E R C E P T O R\n")
    self.request.send("We've managed to splice the fiber optic cable in between Alice and Bob\n")
    self.request.send("But how can we read their message?? They're using QKD to share keys!!\n")
    self.request.send("We've provided you all the tools we can.. good luck...\n")

    a = Alice()
    b = Bob()

    state = qubit("Z",1)
    while state:
      state = a.process(state)
      state = do_intercept(self.request, state, "Bob")
      state = b.process(state)
      state = do_intercept(self.request, state, "Alice")



if __name__ == "__main__":
  SocketServer.TCPServer.allow_reuse_address = True
  server = threadedserver(("0.0.0.0", 20811), incoming)
  server.timeout = 4
  server_thread = threading.Thread(target=server.serve_forever)
  server_thread.daemon = False
  server_thread.start()

