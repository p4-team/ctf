from pwn import *

context.log_level = 'debug'

def xor_to_byte(data):
	return reduce(lambda x,y: x ^ y, map(ord, data), 1)

def get_bot_id():
	a = 0xdeadbeef
	b = (a * 0x5851F42D4C957F2D + 1) & 0xffffffff00000000
	return a | b

def send_packet(r, data, add_size=8):
	bot_id = p64(get_bot_id())

	r.send(p32(len(data) + 1 + 8)) # 4 bytes for bot_id and 1 byte for checksum
	r.send(bot_id)
	r.send(data)
	r.send(chr(xor_to_byte(bot_id) ^ xor_to_byte(data)))

def receive_packet(r):
	size = u32(r.recv(4))
	bot_id = u64(r.recv(8))
	data = r.recv(size - 1 - 8)
	xored = ord(r.recv(1))
	return data

r = remote('mlwr-part1.ctfcompetition.com', 4242)

send_packet(r, 'part1 flag')
r.interactive()

