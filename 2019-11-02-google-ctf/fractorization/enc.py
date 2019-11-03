from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from secrets import my_rsa_key_generator, key, flag

def pad(data):
  pad_size = AES.block_size - len(data) % AES.block_size
  return data + pad_size * bytes([pad_size])

n, e, d, p, q = my_rsa_key_generator(nbits = 4096)
rsa_key = RSA.construct((n, e, d, p, q))

pub_der = rsa_key.publickey().exportKey('DER')
priv_der = rsa_key.exportKey('DER')

# AES-ECB is safe, right? :)
aes_ecb = AES.new(key, AES.MODE_ECB)
priv_der_enc = aes_ecb.encrypt(pad(priv_der))
flag_enc = rsa_key.encrypt(flag, None)[0]

open('pub.der', 'wb').write(pub_der)
open('priv.der.enc', 'wb').write(priv_der_enc)
open('flag.enc', 'wb').write(flag_enc)
