HOST = "localhost"
PORT = 1337

import os
import sys
from FLAG import FLAG
from pwn import *
import multiprocessing

r = None
remote_start_time = None

LED = 64

state = [[0 for i in range(4)] for j in range(4)]

MixColMatrix = [
	[4,  1, 2, 2],
	[8,  6, 5, 6],
	[11,14,10, 9],
	[2,  2,15,11],
]

sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]
WORDFILTER = 0xF

def FieldMult(a,b):
  ReductionPoly = 0x3
  x = a
  ret = 0
  for i in range(0,4):
    if (b>>i)&1 == 1: ret ^= x
    if (x&0x8) != 0:
      x <<= 1
      x ^= ReductionPoly
    else: x <<= 1
  return ret&WORDFILTER

def AddKey(keyBytes,step):
  global state
  for i in range(0,4):
    for j in range(0,4):
      state[i][j] ^= keyBytes[(4*i+j+step*16)%(LED/4)]
  return state

def AddConstants(r):
  global state
  RC = [
		0x01, 0x03, 0x07, 0x0F, 0x1F, 0x3E, 0x3D, 0x3B, 0x37, 0x2F,
		0x1E, 0x3C, 0x39, 0x33, 0x27, 0x0E, 0x1D, 0x3A, 0x35, 0x2B,
		0x16, 0x2C, 0x18, 0x30, 0x21, 0x02, 0x05, 0x0B, 0x17, 0x2E,
		0x1C, 0x38, 0x31, 0x23, 0x06, 0x0D, 0x1B, 0x36, 0x2D, 0x1A,
		0x34, 0x29, 0x12, 0x24, 0x08, 0x11, 0x22, 0x04
	]
  state[1][0] ^= 1
  state[2][0] ^= 2
  state[3][0] ^= 3

  state[0][0] ^= (LED>>4)&0xf
  state[1][0] ^= (LED>>4)&0xf
  state[2][0] ^= LED & 0xf
  state[3][0] ^= LED & 0xf

  tmp = (RC[r] >> 3) & 7
  state[0][1] ^= tmp
  state[2][1] ^= tmp
  tmp =  RC[r] & 7
  state[1][1] ^= tmp
  state[3][1] ^= tmp


def SubCell():
  global state
  for i in range(0,4):
    for j in range(0,4):
      state[i][j] = sbox[state[i][j]]

def ShiftRow(): 
  global state
  tmp = [0]*4
  for i in range(1,4):
    for j in range(0,4):tmp[j] = state[i][j]
    for j in range(0,4):state[i][j] = tmp[(j+i)%4]

def MixColumn():

  global state
  tmp = [0]*4
  for j in range(0,4):
    for i in range(0,4):
      sum = 0
      for k in range(0,4):
        sum ^= FieldMult(MixColMatrix[i][k], state[k][j]) 
      tmp[i] = sum
    for i in range(0,4):state[i][j] = tmp[i]


def host_encrypt_for_key(input,userkey,sbox_lazy,rounds):
  """
  input - list of integers from range 0x0 - 0xFF
  userkey - list of integers from range 0x0 - 0xFF
  rounds - lazy
  sbox_lazy - my chosen sbox_lazy
  returns: string
  """
  global state, LED
  ksbits = 16*8

  if rounds < 1 or rounds > 10:
    print "Sorry I'm not in the mood. Bye!"
    exit(0)

  keyNibbles = [0]*32

  for i in range(0,16):
    if (i%2) == 1: state[i/4][i%4] = input[i>>1]&0xF
    else: state[i/4][i%4] = (input[i>>1]>>4)&0xF
  #state to input

  for i in range(0,ksbits/4):
    if (i%2) == 1: keyNibbles[i] = userkey[i>>1]&0xF
    else: keyNibbles[i] = (userkey[i>>1]>>4)&0xF


  #print "keyNibbles = "+str(keyNibbles) #len(_)=32
  
  LED = ksbits
  RN = 48
  if LED <= 64: RN = 32
  AddKey(keyNibbles,0)

  #print "state = "
  #print state

  rr = 0

  for i in range(0,RN/4): # I don't want to do it so many times!
    for j in range(0,4):
      AddConstants(i*4+j)
      SubCell()
      ShiftRow()
      MixColumn()
      rr += 1
      if rr == rounds:break # bye!
    if rr == rounds:break # bye!
    AddKey(keyNibbles, i+1)

  """  Making output string is so hard for me!
  output = [0]*8
  ret = ""
  for i in range(0,8):
    output[i] = ((state[(2*i)/4][(2*i)%4] & 0xF) << 4) | (state[(2*i+1)/4][(2*i+1)%4] & 0xF)
    ret += chr( output[i] )
  """
  ret = ""
  for i in range(0,4):
    for j in range(0,4):
      ret += chr(state[i][j])

  #print "ret :"+repr(ret)

  ret2 = ""
  for i in range(16):
    ret2 += ret[ sbox_lazy[i] ] # Now it's safe!

  #print "ret2 :"+repr(ret2)	
  return ret2


def Lazy_LED_enc_no_lazy_sbox(input,userkey,ksbits,rounds):
  """
  userkey -list
  input - list 
  """
  
  global state, LED, sbox_lazy

  if rounds < 1 or rounds > 10:
    print "Sorry I'm not in the mood. Bye!"
    exit(0)

  keyNibbles = [0]*32

  for i in range(0,16):
    if (i%2) == 1: state[i/4][i%4] = input[i>>1]&0xF
    else: state[i/4][i%4] = (input[i>>1]>>4)&0xF
  #state to input

  for i in range(0,ksbits/4):
    if (i%2) == 1: keyNibbles[i] = userkey[i>>1]&0xF
    else: keyNibbles[i] = (userkey[i>>1]>>4)&0xF

  
  LED = ksbits
  RN = 48
  if LED <= 64: RN = 32 
  AddKey(keyNibbles,0)

  rr = 0

  for i in range(0,RN/4): #I don't want to do it so many times!
    for j in range(0,4):
      AddConstants(i*4+j)
      SubCell()
      ShiftRow()
      MixColumn()
      rr += 1
      if rr == rounds:break # bye!
    if rr == rounds:break # bye!
    AddKey(keyNibbles, i+1)
    
  """  Making output string is so hard for me!
  output = [0]*8
  ret = ""
  for i in range(0,8):
    output[i] = ((state[(2*i)/4][(2*i)%4] & 0xF) << 4) | (state[(2*i+1)/4][(2*i+1)%4] & 0xF)
    ret += chr( output[i] )
  """
  ret = ""
  for i in range(0,4):
    for j in range(0,4):
      ret += chr(state[i][j])

  #print "ret :"+repr(ret)
  return ret

"""
#to nibbles
for i in range(0,ksbits/4): #tutaj sie liczy jakies keyNibbles z calego keya, aaaaa, bajty sa rozdzialane na polowy
    if (i%2) == 1: keyNibbles[i] = userkey[i>>1]&0xF
    else: keyNibbles[i] = (userkey[i>>1]>>4)&0xF
"""

def from_nibbles(nibbles):
	key = []
	for i in range(len(nibbles)/2):
		key.append(nibbles[i*2]*16+nibbles[i*2+1])
	return key

server_encrypt_for_nibbles_map = {}

def to_hex(i):
	e = hex(i)[2:] 
	if len(e) == 1:
		e = "0"+e
	return e

server_encrypt_cache = {}
def server_encrypt(password, lazy):
	"""
	password - list integers from range 0x0 - 0xFF
	"""
	
	global r
	global remote_start_time
	global server_encrypt_cache
	if (tuple(password), lazy) in server_encrypt_cache:
		return server_encrypt_cache[(tuple(password), lazy)]
	
	if r == None:
		r = remote(HOST,PORT)
		r.recvuntil("hex.")
		remote_start_time = time.time()
	
	#local:
	#return Lazy_LED_enc(password, k_data, 16*8, lazy)

	#remote:
	r.sendline( "".join(map(lambda x: to_hex(x), password ))+"lazy"+str(lazy) )
	data = r.recvuntil("hex.")
	
	print repr(data)
	
	print re.findall(r"ciphertext: \n([0-9a-f]{32})",data)
	
	cipher = re.findall(r"ciphertext: \n([0-9a-f]{32})",data)[0]
	ret = cipher.decode("hex")
	
	server_encrypt_cache[(tuple(password), lazy)] = ret
	
	return ret
	
def server_encrypt_for_nibbles(arg,nibbles):
		
	password = [0 for x in range(16)]
	password[nibbles[0]]=arg[0]
	password[nibbles[1]]=arg[1]
	password[nibbles[2]]=arg[2]
	password[nibbles[3]]=arg[3]
	
	out = server_encrypt(from_nibbles(password), 1)
	
	out = [ord(x) for x in out]
	
	return out
	
def server_encrypt_for_nibbles_(arg,nibbles1,nibbles2,nibbles3,nibbles4):
		
	password = [0 for x in range(16)]
	password[nibbles1[0]]=arg[0]
	password[nibbles1[1]]=arg[1]
	password[nibbles1[2]]=arg[2]
	password[nibbles1[3]]=arg[3]
	
	password[nibbles2[0]]=arg[0]
	password[nibbles2[1]]=arg[1]
	password[nibbles2[2]]=arg[2]
	password[nibbles2[3]]=arg[3]
	
	password[nibbles3[0]]=arg[0]
	password[nibbles3[1]]=arg[1]
	password[nibbles3[2]]=arg[2]
	password[nibbles3[3]]=arg[3]
	
	password[nibbles4[0]]=arg[0]
	password[nibbles4[1]]=arg[1]
	password[nibbles4[2]]=arg[2]
	password[nibbles4[3]]=arg[3]
	
	out = server_encrypt(from_nibbles(password), 1)
	
	out = [ord(x) for x in out]
	
	return out


def get_changing_bytes(tests,nibbles):
	chbytes = set()
	
	prev = server_encrypt_for_nibbles(tests[0],nibbles)
	
	for test in tests[1:]:
		
		now = server_encrypt_for_nibbles(test,nibbles)
		
		print "****"
		print now
		print prev
		
		for i in range(16):
			if prev[i]!=now[i]:
				chbytes.add(i) 
		if len(chbytes) == 4:
			break
				
	assert( len(chbytes) == 4 )			
	return list(chbytes)


def compute_key_out(out_nibbles, in_nibbles):
	
	#brute one column - nibbles in -> nibbles out
	
	key_out = {}
	
	for n1 in range(16):
		for n2 in range(16):
			for n3 in range(16):
				for n4 in range(16):
					nibbles = [0 for x in range(16)]
					nibbles[in_nibbles[0]]=n1
					nibbles[in_nibbles[1]]=n2
					nibbles[in_nibbles[2]]=n3
					nibbles[in_nibbles[3]]=n4
					key = from_nibbles(nibbles)
					out = Lazy_LED_enc_no_lazy_sbox([0 for x in range(8)], key + [0 for x in range(8)], 16*8, 1)
					out = [ord(x) for x in out]
					out = [out[out_nibbles[0]],out[out_nibbles[1]],out[out_nibbles[2]],out[out_nibbles[3]]]
					key_out[(n1,n2,n3,n4)]=tuple(sorted(out)) # posortowane
					
	print "map key_out created!"
	return key_out

def solve_for_nibbles(key_out, out_nibbles, in_nibbles, nibbles_list):
	nibbles1 = nibbles_list[0]
	nibbles2 = nibbles_list[1]
	nibbles3 = nibbles_list[2]
	nibbles4 = nibbles_list[3]
		
	password_tests = [tuple([y for x in range(4)]) for y in range(16)]

	changing_bytes = get_changing_bytes(password_tests,in_nibbles)
	print "changing bytes = "+str(changing_bytes)
	
	
	for n1 in range(16):
		for n2 in range(16):
			for n3 in range(16):
				for n4 in range(16):			
										
					key_correct = True
					
					for password in password_tests:
						out = server_encrypt_for_nibbles_(password,nibbles1,nibbles2,nibbles3,nibbles4) #co ta funkcjarobi
						out = tuple(sorted([out[changing_bytes[0]],out[changing_bytes[1]],out[changing_bytes[2]],out[changing_bytes[3]]]))
						
						real_out = key_out[(n1^password[0],n2^password[1],n3^password[2],n4^password[3])]
						
						if out!=real_out:
							key_correct=False
							break
							
					if key_correct:
						print "found 2B of key!!!"
						print (n1,n2,n3,n4)
						return (n1,n2,n3,n4)

def update_key_nibbles(key_nibbles, nibbles, key_part):
	for i in range(4):
		key_nibbles[nibbles[i]]=key_part[i]

def recover_lazy_sbox(key_nibbles):
	"""
	key_nibbles - list
	"""
	password_tests = [[0x41]*8,[0x61]*8,[0x63]*8,[0x7a]*8,[0x00]*8,[0x20]*8,[0xf0]*8,[0xaa]*8,[0xc8]*8]
	
	lazy_sbox = [None]*16
	b = False
	
	for test in password_tests:
		if b:
			break
		
		real_out = server_encrypt(test, 1)
		real_out = [ord(x) for x in real_out]
		
		my_out = Lazy_LED_enc_no_lazy_sbox(test, from_nibbles(key_nibbles+ [0 for x in range(16)]), 16*8, 1)
		my_out = [ord(x) for x in my_out]
		
		"""
		print "!!!!"
		print sbox_lazy
		print my_out
		print real_out
		"""
		
		for i in range(16):
			if my_out.count(i) == 1:
				
				idx1 = my_out.index(i)
				idx2 = real_out.index(i)
				
				lazy_sbox[idx2] = idx1
				
				if not None in lazy_sbox:
					b = True
					break
		
		#print lazy_sbox
	
	print "lazy sbox = "+str(lazy_sbox)
	return lazy_sbox

def reverse_permutation(l):
	
	r = [None for x in l]
	
	for i in range(len(l)):
		r[l[i]] = i
		
	return r
	
def worker( arguments ):
	half_key_nibbles = arguments[0]
	lazy_sbox = arguments[1]
	server_out = arguments[2]
	nibbles1 = arguments[3]
	nibbles2 = arguments[4]
	return solve2_for_nibbles(half_key_nibbles, lazy_sbox, server_out, nibbles1,nibbles2)
		
					
def solve_second_part(half_key_nibbles, lazy_sbox):
	test_password = [0x61]*8 
	
	server_out = server_encrypt(test_password, 5)
	server_out = map(ord, server_out)
	
	
	#let's multithread this
	
	"""
	fifth_2B = solve2_for_nibbles(half_key_nibbles, lazy_sbox, server_out, (0,4,8,12),(0,5,10,15))
	sixth_2B = solve2_for_nibbles(half_key_nibbles, lazy_sbox, server_out, (1,5,9,13),(1,6,11,12))
	seventh_2B = solve2_for_nibbles(half_key_nibbles, lazy_sbox, server_out, (2,6,10,14),(2,7,8,13))
	eighth_2B = solve2_for_nibbles(half_key_nibbles, lazy_sbox, server_out, (3,7,11,15),(3,4,9,14))
	"""
	
	print "starting multiprocessing"
	print "time = "+str(int(time.time()-remote_start_time))
	
	pool = multiprocessing.Pool(processes=4)
	result = pool.map(worker, [(half_key_nibbles, lazy_sbox, server_out,(0,4,8,12),(0,5,10,15)) , (half_key_nibbles, lazy_sbox, server_out,(1,5,9,13),(1,6,11,12)) ,  (half_key_nibbles, lazy_sbox, server_out,(2,6,10,14),(2,7,8,13)) ,  (half_key_nibbles, lazy_sbox, server_out,(3,7,11,15),(3,4,9,14))  ])
	pool.close()
    
	print result
	(fifth_2B, sixth_2B, seventh_2B, eighth_2B) = result
	
	#join them in key
	key_nibbles = [0]*16
	update_key_nibbles(key_nibbles, (0,5,10,15), fifth_2B)
	update_key_nibbles(key_nibbles, (1,6,11,12), sixth_2B)
	update_key_nibbles(key_nibbles, (2,7,8,13), seventh_2B)
	update_key_nibbles(key_nibbles, (3,4,9,14), eighth_2B)
	key = from_nibbles(key_nibbles)
	print "second part of key = "+str(key)
	return key
	
def solve2_for_nibbles(half_key_nibbles, lazy_sbox, server_out, out_nibbles, in_nibbles):	
	
	test_password = [0x61]*8
	
	lazy_sbox_reverse = reverse_permutation(lazy_sbox)
	changing_bytes = [lazy_sbox_reverse[out_nibbles[x]] for x in range(4) ]
	print "changing bytes = "+str(changing_bytes)
	
	for n1 in range(16):
		for n2 in range(16):
			for n3 in range(16):
				for n4 in range(16):
					nibbles = [0 for x in range(16)]
					nibbles[in_nibbles[0]]=n1
					nibbles[in_nibbles[1]]=n2
					nibbles[in_nibbles[2]]=n3
					nibbles[in_nibbles[3]]=n4
					
					out = host_encrypt_for_key(test_password,from_nibbles(half_key_nibbles + nibbles), lazy_sbox, 5)
					out = map(ord, out)
					
					if out[changing_bytes[0]] == server_out[changing_bytes[0]] and out[changing_bytes[1]] == server_out[changing_bytes[1]] and out[changing_bytes[2]] == server_out[changing_bytes[2]] and out[changing_bytes[3]] == server_out[changing_bytes[3]]:
						new_part = (n1,n2,n3,n4)
						print "found next 2B part!! "+str(new_part)
						print "time = "+str(int(time.time()-remote_start_time))
						return new_part

def solve():
	#get 4 2-Bytes parts of key
	
	key_out1 = compute_key_out((0,4,8,12),(0,5,10,15))
	key_out2 = compute_key_out((1,5,9,13),(1,6,11,12))
	key_out3 = compute_key_out((2,6,10,14),(2,7,8,13))
	key_out4 = compute_key_out((3,7,11,15),(3,4,9,14))
	
	nibbles_list = [(0,5,10,15), (1,6,11,12), (2,7,8,13), (3,4,9,14)]
	
	first_2B = solve_for_nibbles(key_out1,(0,4,8,12),(0,5,10,15), nibbles_list)
	second_2B = solve_for_nibbles(key_out2,(1,5,9,13),(1,6,11,12), nibbles_list)
	third_2B = solve_for_nibbles(key_out3,(2,6,10,14),(2,7,8,13), nibbles_list)
	fourth_2B = solve_for_nibbles(key_out4,(3,7,11,15),(3,4,9,14), nibbles_list)
	
	#join them in key
	key_nibbles = [0]*16
	update_key_nibbles(key_nibbles, (0,5,10,15), first_2B)
	update_key_nibbles(key_nibbles, (1,6,11,12), second_2B)
	update_key_nibbles(key_nibbles, (2,7,8,13), third_2B)
	update_key_nibbles(key_nibbles, (3,4,9,14), fourth_2B)
	key = from_nibbles(key_nibbles)
	print "key = "+str(key)
	
	lazy_sbox = recover_lazy_sbox(key_nibbles)
	
	second_half_of_key = solve_second_part(key_nibbles, lazy_sbox)
	key = key + second_half_of_key
	
	r.sendline("exit")
	r.recvuntil("key?")
	r.sendline("".join(map(to_hex,key)))
	print r.recv()
	print r.recv()
	
	print "key = "+str(key)
	
	print "time = "+str(int(time.time()-remote_start_time))


if __name__ == '__main__':
    solve()

 
