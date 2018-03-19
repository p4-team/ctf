# Awesome Mix 1 (Crypto)

In the task we get the source code:

```python
#!/usr/bin/python -u

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as RSAsign
from Crypto.Hash import SHA
from Util import PKCS1_pad as pad
from SECRET import flag
import sys

def verify(s,m,n,e):
	if pow(s,e,n) == pad(m):
		return True
	else:
		return False

key = RSA.generate(1024)

message = "super important information for admin only"

h = SHA.new(message)

signer = RSAsign.new(key)

signature = signer.sign(h)
s = int(signature.encode("hex"),16)

print "Welcome to admin's music portal.\nTo verify that you are the owner of this service\nsend the public key which will verify the following signature :\n"

print "Message   ->", message
print 
print "Signature ->", signature.encode("hex")
print 

sys.stdout.flush()

n = long(raw_input("Enter n:"))
e = long(raw_input("Enter e:"))
sys.stdout.flush()
input_key = RSA.construct((n,e))

if verify(s,h.hexdigest(),n,e):
	print flag
else:
	print "Music is only for admin's eyes."

sys.stdout.flush()
```

So the server generates a random RSA key, signs a certain message with it and asks us for a public key matching the signature.
The mistake here is that there are no restrictions on the values for the public key.

What we get is: 

`signature == message^d mod n`

And we want now values `(e,n)` for which holds:

`signature^e mod n == message`

If we take `e=1` then this equation becomes simply:

`signature mod n == message`

We can select any `n` we want, so we can choose the trivial case where `signature` is larger from `n` exactly by `message`, so that modulo operation will cut `signature` by `n`.

If now:

`n = signature-message` 

then 

`signature mod (signature-message) = message`

We used for that code:

```python
import re
from Crypto.Hash import SHA
from crypto_commons.netcat.netcat_commons import nc, send, interactive


def PKCS1_pad(data):
    asn1 = "003021300906052b0e03021a05000414"
    ans = asn1 + data
    n = len(ans)
    padding = '0001' + 'f' * (1024 / 4 - n - 4)
    return int((padding + ans), 16)


def main():
    port = 8082
    host = "51.15.73.163"
    s = nc(host, port)
    data = s.recv(99999)
    print(data)
    sig = re.findall("Signature ->(.*)", data)[0]
    signature = int(sig.strip(), 16)
    message = "super important information for admin only"
	
    h = SHA.new(message)
    m = PKCS1_pad(h.hexdigest())
    e = 1
    n = signature ** e - m
    print('n', n)
    print('e', e)
    send(s, str(n))
    send(s, str(e))
    interactive(s)


main()
```

And got `CTF{cryp70_5ur3_15_w13rd}`
