# Bazik (crypto, 74 solved, 100p)

In the challenge we can connect to a remote server.
Session is basically:

```
Choose one:
1. Test the OTP
2. Get the public key
3. Get flag
1
otp should be: 687845634
encrypted dat: 764a18c52802f763f721b6b2d7fd82738e08dc660d039f1a3ee9dff84159cc102de36537d659e26e6a6e9b1088239b4db6bce64929183e8bfd93ad2acef6b3bfe30e53c59f9f205260de5fe149bdeb486a01ed61ca9e574b8807a3a466275c5c2b118015e538eb4bf81a28fc6d51469cde0e441d8348844a3984e35aedfd69f0
decrypted dat: Your OTP for transaction #731337 in ABCXYZ Bank is 687845634.
decrypted otp: ['687845634']

Choose one:
1. Test the OTP
2. Get the public key
3. Get flag
2
-----BEGIN PUBLIC KEY-----
MIGdMA0GCSqGSIb3DQEBAQUAA4GLADCBhwKBgQCh+QbIPzbKDr8U/+sxHxr9I2vs
352vWIMlGHa1UNx9nvH0PQT8FsaXv0n5mmWwcL6qDxWL/JDRPdN6GrWuYrGTHlEY
qrrMu29K6vUjBlEh91OI1reC/I+ifSk9wPJEqaIW7IQKmlUVCbNyx5nEJ0PDHjLo
pFbCdFW45x5OWu56QwIBAw==
-----END PUBLIC KEY-----

Choose one:
1. Test the OTP
2. Get the public key
3. Get flag
3
encrypted dat: 013137fd49bcccd5cb123102231a46b2047f043431295112c748fd8bad840a5fcf46ed1a07c5e1eeebd380e73a0e827798c76ae0c69a3cef6b161d4acd14c5799fd1e36063e009571fb2314c2e619ea98754c3b908d3f52bbf2522069fac574ccb7562b08e563e030eaf1d381fbc5e26294e2f5e6bb09077333598cc9abfb996
send me otp to get flag >>>
```

What happens here is:

1. We have RSA public key. Worth noticing that `e=3` so is very small.
2. We can "test OTP", which just shows us how the value is encrypted. The value for encryption is `Your OTP for transaction #731337 in ABCXYZ Bank is XXXX.` where XXXX is the random OTP value. We can verify this by encrypting the payload with given public RSA key.
3. When we request the flag it will ask us for OTP value of some encrypted payload.

It is important to notice that the encrypted messages differ only very slightly.
We can abuse this by using `Stereotyped Messages Attack` which can decrypt such messages using Coppersmith method:

- We have encrypted message `c`
- We have `similar` message for which we know plaintext, in our case `m = bytes_to_long("Your OTP for transaction #731337 in ABCXYZ Bank is 000000000.")`
- We can build a polynomial `((m + x)^e - c) mod N` and root of such polynomial would be the difference between our known message and the encrypted message we have.
- This can be efficiently calculated as long as the difference doesn't exceed `N^1/e`.

```python
import time
import sys

def long_to_bytes(data):
    data = str(hex(long(data)))[2:-1]
    return "".join([chr(int(data[i:i + 2], 16)) for i in range(0, len(data), 2)])
    
def bytes_to_long(data):
    return int(data.encode('hex'), 16)

def main():
    e,N = (3L, 101100845141156293469516586973179461987930689009763964117872470309684853512775295312081121501322683984914454311655512983781714534411655378725344931438891842226528067586198216797211681076517718505980665732445770547794541814618131322049740520275847849231052080791884055178607671253203354019327951368529475389269L)

    c = 0x20375ebbb61e4841c9cb223fbbdd3bfc271fdfc581680ea1e8e6232b7a37a8d34e9979c0e0f44dac09efa840d8c3d74e59ec6477a2378221e7130d3b82602be37472df51621cc3e4b4be845c8c320051c9a712eafb50fe738c07bf01901d889981b3b0cea2abd3ef9771ae06de089791e83700627e2f8e5f83f17c082542a3da
    m = bytes_to_long("Your OTP for transaction #731337 in ABCXYZ Bank is 000000000.")
    P.<x> = PolynomialRing(Zmod(N), implementation='NTL')
    pol = (m + x)^e - c
    roots = pol.small_roots(epsilon=1/30)
    print("Potential solutions:")
    for root in roots:
       print(root, long_to_bytes(m+root))
	
main()
```

This code for given public key and ciphertext returns the decrypted value.
Once we submit the OTP to the server we get `MeePwnCTF{blackbox-rsa-is-0xd34d}`
