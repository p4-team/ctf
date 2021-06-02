from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib 
from a2s import A2S, bytes2matrix, matrix2bytes, inv_mix_columns, xor_bytes, inv_shift_rows, shift_rows
from uuid import uuid4
from itertools import product
#key = uuid4().bytes
key = bytes.fromhex('7fc44782223349df83a16ceed8895a5c')
cipher = A2S(key)

#print(b''.join(cipher._key_matrices[1]).hex())

plaintexts =  list(map(bytes.fromhex, [ '0573e60e862b4c46bdc5fcea1d0316ea', '2dd6d234bfe14fb0a0c4786b3891698d', '533698ece7db47df82413aba5f4f0cfb']))
ciphertexts =  list(map(bytes.fromhex, ['42352473eeb42625210217a339dbc69f', 'b14c9d2d835c725e13598907a5b89165', 'f96b99b82fe4543150604d20e8cd5fda']))
#ciphertexts = list(map(lambda x: cipher.encrypt_block(x)[0], plaintexts))

def shift(st):
    mat = bytes2matrix(st)
    shift_rows(mat)
    return matrix2bytes(mat)

def unshift(st):
    mat = bytes2matrix(st)
    inv_shift_rows(mat)
    return matrix2bytes(mat)

def unmix(st):
    mat = bytes2matrix(st)
    inv_mix_columns(mat)
    inv_shift_rows(mat)
    return matrix2bytes(mat)

pre_delta1 = shift(xor_bytes(plaintexts[0], plaintexts[1]))
pre_delta2 = shift(xor_bytes(plaintexts[0], plaintexts[2]))

post_delta1 = xor_bytes(unmix(ciphertexts[0]), unmix(ciphertexts[1]))
post_delta2 = xor_bytes(unmix(ciphertexts[0]), unmix(ciphertexts[2]))

print(pre_delta1.hex())
print(pre_delta2.hex())
print(post_delta1.hex())
print(post_delta2.hex())

#print(cipher.encrypt_block(plaintexts[0])[2].hex())

output = """
067c20d3
1f473b29
--------
8a151475
d441a30c
--------
34a72235
d4eb9f89
--------
1e89501b
a0227d5b
336f0e52
f669b656
""".split('--------\n')

def options(s):
    return map(bytes.fromhex, s.strip().split())

for a in product(*map(options, output)):
    state = unshift(b''.join(a))
    k = xor_bytes(plaintexts[0], state)
    c = A2S(k)
    if c.encrypt_block(plaintexts[0])[0] == ciphertexts[0]:
        print(k.hex())
        sha1 = hashlib.sha1()
        sha1.update(str(k).encode('ascii'))
        new_key = sha1.digest()[:16]
        iv = bytes.fromhex('35a84c9bf33d40e8bfab6e7e62209b49')
        encrypted_flag = bytes.fromhex('ef14d5f8f4f51b34fb251bacf309e0c4386c33021903528b475d232a401aeeb49e23b3bc2a416b386590ae0d5580cbfebce4a40ed563f664f28d1cfa8e4cde02bfe077b1ef583bf2850cf0ac764182e7')
        cipher = AES.new(new_key, AES.MODE_CBC, IV=iv)
        print(unpad(cipher.decrypt(encrypted_flag), 16))
#c1, pre1 = cipher.encrypt_block(plaintexts[0])
#c2, pre2 = cipher.encrypt_block(plaintexts[1])
#
#print(xor_bytes(pre1, pre2).hex())
#print(xor_bytes(unmix(c1), unmix(c2)).hex())

# sub_bytes(plain_state)
# mix_columns(plain_state)
# add_round_key(plain_state, self._key_matrices[1])
# sub_bytes(plain_state)
