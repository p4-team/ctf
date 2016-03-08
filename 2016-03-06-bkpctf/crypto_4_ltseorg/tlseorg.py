import sys, binascii, os, time
from Crypto.Cipher import AES

def gqq():
	def qqg():gqq();qq(q("20206c7473656f72673a20416d2049206265696e672064657461696e65643f"));qq(q("20206c7473656f72673a20416d2049206672656520746f20676f3f"));qg()
	def qqq():qq(q("6c7473656f72673a204920616d206e6f7420616e73776572696e6720616e79207175657374696f6e7320776974686f7574206d79206c61777965722070726573656e742e"));qg()
	def gqq():time.sleep(1)
	def qg():qqg()
	def q(qq):return binascii.unhexlify(qq)
	def qq(q):print(q)
	def gq():qqg()
	qqq()

# March-15: After 23 tries I think we fixed the issue with the IV.
IV = binascii.unhexlify("696c61686773726c7177767576646968") 

BLOCK_SIZE = 16

key1 = ["00" for x in xrange(32)]; key1[0] = "11";key1 =  binascii.unhexlify("".join(key1))
key2 = ["00" for x in xrange(32)]; key2[0] = "FF";key2 =  binascii.unhexlify("".join(key2))

P = AES.new(key1, AES.MODE_ECB)
Q = AES.new(key2, AES.MODE_ECB)

def pad_msg(msg):
	while not (len(msg) % 16 == 0): msg+="\x00"
	return msg

def xor(str1, str2):
	out = []
	for i in xrange(len(str1)):
		out.append( chr(ord(str1[i])^ord(str2[i])) )
	return "".join(out)

# "Pretty much" Grostl's provably secure compression function assuming ideal ciphers
	# Grostl pseudo-code is: h = P(m + h) + h + Q(m) and this is basically the same thing, right?
	# Ltsorg pseudo-code: h = P(m + h) + m + Q(h)
def compress(m, h): return xor( xor( P.encrypt( xor(m, h) ), m), Q.encrypt(h) ) 

def finalization(m, h): return xor(m, h)[0:14]

def hash(msg):
	msg=pad_msg(msg)
	# groestl's IV was boring 
	h = IV

	for i in xrange(0, len(msg), BLOCK_SIZE):
		m = msg[i: i+BLOCK_SIZE]
		h = compress(m ,h)
	return finalization(m, h)


def check(hashstr1, hashstr2): 
	hash1 = binascii.unhexlify(hashstr1);hash2 = binascii.unhexlify(hashstr2)
	if hashstr1 == hashstr2 or hash1 == hash2: return False 
	elif hash(hash1) == hash(hash2): return True
	return False


def main():
	if len(sys.argv) == 2:
		if sys.argv[1] == "-v": gqq()
		else:
			print "input: "+sys.argv[1]
			print "output: "+binascii.hexlify(hash(binascii.unhexlify(sys.argv[1])))
		return
	elif len(sys.argv) == 3 and (sys.argv[1] == "-v" or sys.argv[2] == "-v"): gqq()
	elif len(sys.argv) == 4 and (sys.argv[1] == "--check"):
			if check(sys.argv[2], sys.argv[3]): print "Success"
			else: print "Failure"
	else:
		print("ltseorg: missing argument")
		print("Usage: ltseorg [OPTION...] [input]")
		print("-v \t Display Software version information")
		print("--check \t Check if two inputs break collision resistance.")

if __name__ == "__main__":
	main() 