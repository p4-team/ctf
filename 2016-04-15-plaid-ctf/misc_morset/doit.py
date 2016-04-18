from pwn import *
import binascii
import hashlib

code = {'A': '.-',     'B': '-...',   'C': '-.-.', 
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
        'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',       
        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.' 
}
revcode={}
for c in code:
    revcode[code[c]]=c

def morse_dec(msg):
    res=""
    for word in msg.strip().split():
        res=res+revcode[word]
    return res
def morse_enc(msg):
    res=""
    for c in msg:
        res=res+code[c.upper()]+" "
    return res.strip()

def decrypt(s):
    h=hex(int(morse_dec(s), 36)).strip("L")[2:]
    if len(h)%2==1:
        h="0"+h
    h=binascii.unhexlify(h)
    return h
def base36encode(number):
    if not isinstance(number, (int, long)):
        raise TypeError('number must be an integer')
    if number < 0:
        raise ValueError('number must be positive')

    alphabet, base36 = ['0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', '']

    while number:
        number, i = divmod(number, 36)
        base36 = alphabet[i] + base36

    return base36 or alphabet[0]
def encrypt(s):
    h=morse_enc(base36encode(int(binascii.hexlify(s), 16)))
    return h


r=remote("morset.pwning.xxx", 11821)
context.log_level="DEBUG"
s=r.recvline()
h=decrypt(s)
print h
h=h.split("SHA256")[1][1:].split(")")[0]
print h

#r.sendline(morse_enc(hashlib.sha256(h).hexdigest()))
r.sendline(encrypt(hashlib.sha256(h).hexdigest()))

s=r.recvline()
print decrypt(s)

r.recvall()
