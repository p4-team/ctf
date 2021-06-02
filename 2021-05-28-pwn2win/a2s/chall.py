from a2s import A2S 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib 
from uuid import uuid4


key = uuid4().bytes
cipher = A2S(key)

p = []
c = []

for _ in range(3):
    plaintext = uuid4().bytes
    p.append(plaintext.hex())
    ciphertext = cipher.encrypt_block(plaintext)
    c.append(ciphertext.hex())

flag = open("flag.txt", "rb").read()   
sha1 = hashlib.sha1()
sha1.update(str(key).encode('ascii'))
new_key = sha1.digest()[:16]
iv = uuid4().bytes
cipher = AES.new(new_key, AES.MODE_CBC, IV=iv)
encrypted_flag = cipher.encrypt(pad(flag, 16))

print('plaintexts = ', p)
print('ciphertexts = ', c)
print('iv = ', iv.hex())
print('encrypted_flag = ', encrypted_flag.hex())
print(hex(key[0]), hex(key[-1]))
