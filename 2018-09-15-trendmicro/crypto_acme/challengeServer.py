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
import sys
import os.path
import subprocess
import binascii
from io import BytesIO
from base64 import b64encode, b64decode
from struct import pack, unpack
from Crypto.Hash import SHA256

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

OOP_server = os.path.join(sys.path[0], "server", "server", "server");

def readNullTerminatedByteString(f):
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
	return buf

def readNullTerminatedString(f):
	return unicode(readNullTerminatedByteString(f), encoding="utf-8", errors="strict")
	
def readBytes(f, nBytes):
	result = f.read(nBytes)
	if len(result) != nBytes:
		logger.warning("Unexpected end of stream encountered while reading a null-terminated string")
		raise Exception("End of stream encountered")
	return result

def invokeOOPServer(message):
	messageBase64 = b64encode(message);
	oopServer = subprocess.Popen(
		OOP_server,
		stdin=subprocess.PIPE,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE)
	oopResult = oopServer.communicate(messageBase64)
	response = oopResult[0]
	testString = "STARTUP_SELF_TEST\x00"
	if response[0:len(testString)] != testString:
		error = "Out-of-process server is not working properly. Path to executable : %s" % OOP_server
		logger.fatal(error)
		raise Exception(error)
	response = response[len(testString):]
	return (oopServer.returncode, response)


class MyTCPHandler(SocketServer.StreamRequestHandler):
	
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
						self._processMessage_LogonRequest_OOP()
					elif messageType == 0x03:
						self._processMessage_LogonResponse_OOP()
					elif messageType == 0x06:
						self._processMessage_Command_OOP()
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
	
	def _sendMessage_AuthxFailure(self, terminateConnection = False):
		logger.info("Sending message: AUTHX_FAILURE")
		self.wfile.write("\x05")
		self.wfile.flush()
		if terminateConnection:
			logger.info("Connection will be terminated")
			self._terminateConnection = True
			
	def _processMessage_OOP(self, message):
		logger.debug("Sending message to out-of-process server: " + binascii.hexlify(message))
		returncode, response = invokeOOPServer(message)
		if returncode != 0:
			raise Exception("Out-of-process server failed to process the received message")
		logger.debug("Response message produced by out-of-process server: " + binascii.hexlify(response))
		self.wfile.write(response)
		self.wfile.flush()

	def _processMessage_LogonRequest_OOP(self):
		logger.info("Processing LOGON_REQUEST message using out-of-process server")
		userName = readNullTerminatedString(self.rfile)
		message = b'\x01' + userName + '\0'
		self._processMessage_OOP(message)

	def _processMessage_LogonResponse_OOP(self):
		logger.info("Processing LOGON_RESPONSE message using out-of-process server")
		r = self._readBytes(SHA256.digest_size)
		challengeCookie = readNullTerminatedByteString(self.rfile)
		message = b'\x03' + r + challengeCookie + '\0'
		self._processMessage_OOP(message)
	
	def _processMessage_Command_OOP(self):
		logger.info("Processing COMMAND message using out-of-process server")
		ticket = readNullTerminatedString(self.rfile)
		command = readNullTerminatedString(self.rfile)
		message = b'\x06' + ticket + '\0' + command + '\0'
		self._processMessage_OOP(message)
	
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
	parser.add_argument("--serverBindAddress", required=False, default="localhost")
	parser.add_argument("port", type=int, nargs="?", default="9999")

	args = parser.parse_args()

	if not os.path.exists(OOP_server):
		logger.fatal("Out-of-process binary not found: %s" % OOP_server)
		sys.exit(-1)

	# Start with a self-test of the out-of-process server
	invokeOOPServer("")

	server = MyThreadingTCPServer((args.serverBindAddress, args.port), MyTCPHandler)

	try:
		logger.warn("Listing on interface %s, port %d", args.serverBindAddress, args.port)
		server.serve_forever()
	except KeyboardInterrupt:
		pass
	
	logger.warn("")
	logger.warn("Shutting down...")
	server.shutdown()	
	logger.warn("Exiting")

