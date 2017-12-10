# Very Smooth (Crypto, 300p)

In the task we get a [pcap](s.pcap) with RSA encrypted SSL traffic.
The task name suggests that maybe the RSA modulus or primes are a smooth number and modulus can be factored in some simple way.

First we open the pcap in Network Miner in order to recover the [server certificate](SRL.cer).
Next we use openssl to dump just the RSA key from the certificate `openssl x509 -inform der -pubkey -noout -in SRL.cer > public_key.pem` which gives us [public key](public_key.pem).

Now we can proceed with factoring the key.
It turns out the Williams P+1 method works because one of the primes is of form `11807485231629132025602991324007150366908229752508016230400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001` so `prime-1` is a smooth number.

Once we factored the modulus we can generate a fake server private key:

```python
from Crypto.PublicKey import RSA
from primefac import williams_pp1, modinv


def main():
    pub = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDVRqqCXPYd6Xdl9GT7/kiJrYvy
8lohddAsi28qwMXCe2cDWuwZKzdB3R9NEnUxsHqwEuuGJBwJwIFJnmnvWurHjcYj
DUddp+4X8C9jtvCaLTgd+baSjo2eB0f+uiSL/9/4nN+vR3FliRm2mByeFCjppTQl
yioxCqbXYIMxGO4NcQIDAQAB
-----END PUBLIC KEY-----
"""
    pub = RSA.importKey(pub)
    print(pub.e, pub.n)
    p = long(williams_pp1(pub.n))
    q = pub.n / p
    print(p,q)
    assert pub.n == p * q
    priv = RSA.construct((pub.n, pub.e, modinv(pub.e, (p - 1) * (q - 1))))
    print(priv.exportKey('PEM'))


main()
```

We then use this key in Wireshark (Edit -> Preferences -> Protocols -> SSL -> RSA Key List) and it decrypts the SSL traffic for us.
We can see the webpage:

```html
<html>
<head><title>Very smooth</title></head>
<body>
<h1>
Answer: One of these primes is very smooth.
</h1>
</body>
</html>
```

And the flag is: `SECCON{One of these primes is very smooth.}`
