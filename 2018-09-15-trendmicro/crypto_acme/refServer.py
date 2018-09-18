# REQUIRED: PyCrypto 2.6.1
#     To install: pip install pycrypto
#     Homepage: https://www.dlitz.net/software/pycrypto/

import argparse
import SocketServer
import socket
import time
import sys
import json
import logging
from io import BytesIO
from base64 import b64encode, b64decode
from struct import pack, unpack
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA256

################################
# BEGIN SERVER SECRET DATA

serverKey = b64decode("zfAjjf1mNH3HStxAOR0Q+w==")

authDb = \
	[
		{ "user": "admin", "password": "BLTL-INCC-6GPM-N6S7", "groups": [ "admin" ] },
		{ "user": "guest", "password": "Z29S-L47Z-9R8N-D76J", "groups": [ "guests" ] }
	]
	
# END SERVER SECRET DATA
################################

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def pad(data):
	result = data
	nPadBytes = AES.block_size - len(data) % AES.block_size
	for i in range(0, nPadBytes):
		result += chr(nPadBytes)
	return result

def unpad(data):
	if len(data) == 0:
		raise ValueError("Incorrect padding")
	padLength = ord(data[-1])
	if padLength == 0 or padLength > AES.block_size:
		raise ValueError("Incorrect padding")
	if padLength > len(data):
		raise ValueError("Incorrect padding")
	for i in range(-padLength, -2):
		if ord(data[i]) != padLength:
			raise ValueError("Incorrect padding")
	return data[0:-padLength]

def encrypt(plaintext, key):
	iv = Random.new().read(AES.block_size)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	plaintextPadded = pad(plaintext)
	return iv + cipher.encrypt(plaintextPadded)

def decrypt(ciphertext, key):
	if len(ciphertext) < AES.block_size:
		raise ValueError("Ciphertext is invalid - too short to contain IV")
	iv = ciphertext[0:AES.block_size]
	cipher = AES.new(key, AES.MODE_CBC, iv)
	plaintextPadded = cipher.decrypt(ciphertext[AES.block_size:])
	return unpad(plaintextPadded)
	
def getCurrentTimestamp():
	return time.time() * 1000
	
def readNullTerminatedString(f):
	buf = b''
	while True:
		if len(buf) > 1 << 20:
			logger.warning("Overly long input string encountered")
			raise Exception("Overly long input")
		c = f.read(1)
		if len(c) == 0:
			logger.info("Unexpected end of stream encountered while reading a null-terminated string")
			raise Exception("End of stream encountered")
		if ord(c[0]) == 0:		# Indicates NULL termination of a UTF-8 string.
			break
		buf += c
	return unicode(buf, encoding="utf-8", errors="strict")
	
def readBytes(f, nBytes):
	result = f.read(nBytes)
	if len(result) != nBytes:
		logger.warning("Unexpected end of stream encountered while reading a null-terminated string")
		raise Exception("End of stream encountered")
	return result

def toNullTerminatedUtf8(s):
	return unicode(s).encode("utf-8") + "\x00"
		
def stringEquals_dataIndependentTime(a, b):
	if len(a) != len(b):
		return False
	error = 0
	for i in range(0, len(a)):
		error |= ord(a[i]) ^ ord(b[i])
	return error == 0

class MyTCPHandler(SocketServer.StreamRequestHandler):
	
	nonceLengthInBytes = 8
	
	def __init__(self, *a, **k):
		logger.info("Instantiating MyTCPHandler")
		self._terminateConnection = False
		SocketServer.StreamRequestHandler.__init__(self, *a, **k)
	
	def handle(self):
		logger.debug("In MyTCPHandler.handle")
		try:
			while not self._terminateConnection:
				messageTypeByte = self.rfile.read(1)
				if len(messageTypeByte) == 0:
					# Client has disconnected.
					logger.info("Client has disconnected")
					self._terminateConnection = True
				else:
					messageType = ord(messageTypeByte)
					if messageType == 0x01:
						self._processMessage_LogonRequest()
					elif messageType == 0x03:
						self._processMessage_LogonResponse()
					elif messageType == 0x06:
						self._processMessage_Command()
					else:
						raise Exception("Unknown message type received")
		except:
			# All malformed requests caught here.
			# Send AUTHX_FAILURE and terminate connection.
			exceptionInfo = sys.exc_info()
			try:
				logger.info("Exception: %s", exceptionInfo[1])
				self._sendMessage_AuthxFailure(terminateConnection = True)
			except:
				pass
			raise exceptionInfo[0], exceptionInfo[1], exceptionInfo[2]
	
	def _isAdmin(self, identity):
		for group in identity["groups"]:
			if group == "admin":
				return True
		return False

	def _processMessage_LogonRequest(self):
		logger.info("Processing message: LOGON_REQUEST")
		userName = readNullTerminatedString(self.rfile)
		nonce = Random.new().read(self.nonceLengthInBytes)
		timestamp = getCurrentTimestamp()
		challengeCookie = b64encode(encrypt( \
					nonce + \
					toNullTerminatedUtf8(userName) + \
					pack("<q", timestamp), \
				serverKey))
		self._sendMessage_LogonChallenge(nonce, challengeCookie)
	
	def _sendMessage_LogonChallenge(self, nonce, challengeCookie):
		logger.info("Sending message: LOGON_CHALLENGE")
		self.wfile.write(
			"\x02" + \
			nonce + \
			toNullTerminatedUtf8(challengeCookie))
		self.wfile.flush()
		
	def _sendMessage_AuthxFailure(self, terminateConnection = False):
		logger.info("Sending message: AUTHX_FAILURE")
		self.wfile.write("\x05")
		self.wfile.flush()
		if terminateConnection:
			logger.info("Connection will be terminated")
			self._terminateConnection = True
			
	def _processMessage_LogonResponse(self):
		logger.info("Processing message: LOGON_RESPONSE")
		r = self._readBytes(SHA256.digest_size)
		challengeCookie = readNullTerminatedString(self.rfile)
		logger.debug("Challenge cookie received: %s", challengeCookie)
		d = BytesIO(decrypt(b64decode(challengeCookie), serverKey))
		nonce = readBytes(d, self.nonceLengthInBytes)
		username = readNullTerminatedString(d)
		timestamp = unpack("<q", readBytes(d, 8))[0]
		if len(d.read(1)) != 0:		# Not at end of string
			logger.warn("Challenge cookie received does not have proper format")
			raise Exception("Challenge cookie received does not have proper format")
		currentTime = getCurrentTimestamp()
		logger.debug("Cookie timestamp: %d. Current time: %d", timestamp, currentTime)
		if timestamp < currentTime - 5 * 60 * 1000 or timestamp > currentTime:
			logger.info("Challenge cookie is expired")
			self._sendMessage_AuthxFailure()
			return
		userRecord = None
		for element in authDb:
			if element["user"] == username:
				userRecord = element
				break
		if not userRecord:
			logger.info("User does not exist in database: %s", username)
			self._sendMessage_AuthxFailure()
			return
		correctResponse = SHA256.new(nonce + userRecord["password"]).digest()
		logger.debug("Correct response to challenge : %s", correctResponse.__repr__())
		logger.debug("Received response to challenge: %s", r.__repr__())
		if not stringEquals_dataIndependentTime(r, correctResponse):
			logger.info("Response to authentication challenge is not correct. User: %s", username)
			self._sendMessage_AuthxFailure()
			return
		ticketTimestamp = getCurrentTimestamp()
		identity = json.dumps( \
			{ "user" : userRecord["user"], "groups": userRecord["groups"] }, \
			ensure_ascii = False)
		ticket = b64encode(encrypt( \
						toNullTerminatedUtf8(identity) + \
						pack("<q", ticketTimestamp), \
					serverKey))
		logger.info("Authentication succeeded. User: %s", username)
		self._sendMessage_LogonSuccess(ticket)
	
	def _sendMessage_LogonSuccess(self, ticket):
		logger.info("Sending message: LOGON_SUCCESS")
		self.wfile.write(
			"\x04" + \
			toNullTerminatedUtf8(ticket))
		self.wfile.flush()
		
	def _processMessage_Command(self):
		logger.info("Processing message: COMMAND")
		ticket = readNullTerminatedString(self.rfile)
		(identity, error) = self._validateTicket(ticket)
		if error == "EXPIRED":
			logger.info("Ticket expired")
			self._sendMessage_AuthxFailure()
			return
		elif error or not identity:
			logger.info("Ticket invalid")
			self._sendMessage_AuthxFailure(terminateConnection = True)
			return
		command = readNullTerminatedString(self.rfile)
		logger.info("Command: %s. User: %s", command, identity["user"])
		if command == "whoami":
			result = json.dumps(identity, ensure_ascii = False)
		elif command == "getflag":
			if not self._isAdmin(identity):
				logger.info("Unauthorized")
				self._sendMessage_AuthxFailure()
				return
			else:
				result = "GETFLAG AUTHORIZED BUT THIS SERVER DOES NOT CONTAIN A REAL FLAG"
		else:
			logger.info("Unrecognized command")
			self._sendMessage_AuthxFailure()
			return
		self._sendMessage_CommandResult(result)

	# Validates ticket and returns a tuple (identity, error).
	# On success, identity is an identity object and error is None.
	# On failure, identity is None and error is a string indicating the type of error
	def _validateTicket(self, ticket):
		try:
			logger.debug("Ticket: %s", ticket)
			d = BytesIO(decrypt(b64decode(ticket), serverKey))
			identityFromTicket = json.loads(readNullTerminatedString(d))
			timestamp = unpack("<q", readBytes(d, 8))[0]
			if len(d.read(1)) != 0:		# Not at end of string
				raise Exception("Ticket is not well formed")
			currentTime = getCurrentTimestamp()
			logger.debug("Ticket timestamp: %d. Current time: %d", timestamp, currentTime)
			if timestamp < currentTime - 1 * 60 * 60 * 1000 or timestamp > currentTime:
				return (None, "EXPIRED")
			username = identityFromTicket["user"]
			if not (isinstance(username, str) or isinstance(username, unicode)):
				raise Exception("Ticket is not well formed: username is not a string")
			groups = []
			for group in identityFromTicket["groups"]:
				if not (isinstance(group, str) or isinstance(group, unicode)):
					raise Exception("Ticket is not well formed: group name not a string")
				groups.append(group)
			identity = { "user": username, "groups": groups }
			return (identity, None)
		except:
			logger.info("Ticket is not well formed", exc_info=True)
			return (None, "INVALID")
		
	def _sendMessage_CommandResult(self, commandResult):
		self.wfile.write(
			"\x07" + \
			toNullTerminatedUtf8(commandResult))
		self.wfile.flush()
		
	def _readBytes(self, nBytes):
		result = self.rfile.read(nBytes)
		if len(result) != nBytes:
			raise Exception("Connection was closed")
		return result


class MyThreadingTCPServer(SocketServer.ThreadingTCPServer):
	def server_bind(self):
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind(self.server_address)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--serverBindAddress", required=False, default="127.0.0.1")
	parser.add_argument("port", type=int, nargs="?", default="8888")

	args = parser.parse_args()

	server = MyThreadingTCPServer((args.serverBindAddress, args.port), MyTCPHandler)

	try:
		logger.warn("Listing on interface '%s', port %d", args.serverBindAddress, args.port)
		server.serve_forever()
	except KeyboardInterrupt:
		pass
	
	logger.warn("")
	logger.warn("Shutting down...")
	server.shutdown()	
	logger.warn("Exiting")

