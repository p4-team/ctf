#!/usr/bin/python
import sys
import hashlib
import logging
import SocketServer
import base64
from flag import secret
from checksum_gen import WinternizChecksum


logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(ch)


HASH_LENGTH=32
CHECKSUM_LENGTH=4
MESSAGE_LENGTH=32
CHANGED_MESSAGE_LENGTH=MESSAGE_LENGTH+CHECKSUM_LENGTH
BITS_PER_BYTE=8
show_flag_command="show flag"+(MESSAGE_LENGTH-9)*"\xff"
admin_command="su admin"+(MESSAGE_LENGTH-8)*"\x00"
PORT = 1337

def extend_signature_key(initial_key):
  full_sign_key=str(initial_key)
  for i in range(0,255):
    for j in range(0,CHANGED_MESSAGE_LENGTH):
      full_sign_key+=hashlib.sha256(full_sign_key[j*HASH_LENGTH+i*CHANGED_MESSAGE_LENGTH*HASH_LENGTH:(j+1)*HASH_LENGTH+i*CHANGED_MESSAGE_LENGTH*HASH_LENGTH]).digest()
  return full_sign_key
class Signer:
  
  def __init__(self):
    with open("/dev/urandom","rb") as f:
      self.signkey=f.read(HASH_LENGTH*CHANGED_MESSAGE_LENGTH)
    self.full_sign_key=extend_signature_key(self.signkey)
    self.wc=WinternizChecksum()
    self.user_is_admin=False

  def sign_byte(self,a,ind):
    assert(0<=a<=255)
    signature=self.full_sign_key[(CHANGED_MESSAGE_LENGTH*a+ind)*HASH_LENGTH:(CHANGED_MESSAGE_LENGTH*a+ind+1)*HASH_LENGTH]
    return signature

  def sign(self,data):
    decoded_data=base64.b64decode(data)
    if len(decoded_data)>MESSAGE_LENGTH:
      return "Error: message too large"
    if decoded_data==show_flag_command or decoded_data==admin_command:
      return "Error: nice try, punk"
    decoded_data+=(MESSAGE_LENGTH-len(decoded_data))*"\xff"
    decoded_data+=self.wc.generate(decoded_data)
    signature=""
    for i in range(0, CHANGED_MESSAGE_LENGTH):
      signature+=self.sign_byte(ord(decoded_data[i]),i)
    return base64.b64encode(decoded_data)+','+base64.b64encode(signature)
  
  def execute_command(self,data_sig):
    (data_with_checksum, signature)=map(base64.b64decode,data_sig.split(','))
    data=data_with_checksum[:MESSAGE_LENGTH]
    data_checksummed=data+self.wc.generate(data)
    if data_checksummed!=data_with_checksum:
      return "Error: wrong checksum!"
    signature_for_comparison=""
    for i in range(0, CHANGED_MESSAGE_LENGTH):
      signature_for_comparison+=self.sign_byte(ord(data_with_checksum[i]),i)
    if signature!=signature_for_comparison:
      return "Error: wrong signature!"
    if data==admin_command:
      self.user_is_admin=True
      return "Hello, admin"
    if data==show_flag_command:
      if self.user_is_admin:
        return "The flag is %s"%secret
      else:
        return "Only admin can get the flag\n"
    else:
      return "Unknown command\n"
def process(data,signer):
  [query,params]=data.split(':')
  params=params.rstrip("\n")
  if query=="hello":
    return "Hi"
  elif query=="sign":
    return signer.sign(params)
  elif query=="execute_command":
    return signer.execute_command(params)
  else:
    return "bad query"

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
  
  def handle(self):
    signer=Signer()
    logger.info("%s client sconnected" % self.client_address[0])
    self.request.sendall("Welcome to the Tiny Signature Server!\nYou can sign any messages except for controlled ones\n")
    while True:
      data = self.request.recv(2048)
      try:
        ret = process(data,signer)
      except Exception:
        ret = 'Error'
      try:
        self.request.sendall(ret + '\n')
      except Exception:
        break

  def finish(self):
    logger.info("%s client disconnected" % self.client_address[0])


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
  pass

if __name__ == '__main__':
  server = ThreadedTCPServer(('0.0.0.0', PORT), ThreadedTCPRequestHandler)
  server.allow_reuse_address = True
  server.serve_forever()

