# OTS (misc, 105 pts, 51 solved)

This challenge is a pretty easy crypto challenge. What makes it surprising is
that it's very similar to WOTS which is a real world signature scheme.

We get a plaintext (something like `My favorite number is 123123123`) and a
valid signature. Our goal is to forge the signature.

The code (with my refactoring and some debug prints sprinkled in) looks like this:

```python
class OTS:
    def __init__(self):
        self.key_len = 128
        self.priv_key = token_bytes(128 * 16)
        self.pub_key = b"".join(
            [self.hash_iter(chonk, 255) for chonk in chonks(self.priv_key, 16)]
        ).hex()

    def hash_iter(self, msg, n):
        assert len(msg) == 16
        for i in range(n):
            msg = hashlib.md5(msg).digest()
        return msg

    def wrap(self, msg):
        raw = msg.encode("utf-8")
        assert len(raw) <= self.key_len - 16
        raw = raw + b"\x00" * (self.key_len - 16 - len(raw))
        raw = raw + hashlib.md5(raw).digest()
        return raw

    def sign(self, msg):
        raw = self.wrap(msg)
        signature = b"".join(
            [
                self.hash_iter(chonk, 255 - raw[i])
                for i, chonk in enumerate(chonks(self.priv_key, 16))
            ]
        ).hex()
        self.verify(msg, signature)
        return signature

    def verify(self, msg, signature):
        raw = self.wrap(msg)
        print(raw)
        signature = bytes.fromhex(signature)
        assert len(signature) == self.key_len * 16
        calc_pub_key = b"".join(
            [
                self.hash_iter(chonk, raw[i])
                for i, chonk in enumerate(chonks(signature, 16))
            ]
        ).hex()

        print("===")
        for r, a, b in zip(raw, chonks(self.pub_key, 32), chonks(calc_pub_key, 32)):
            print(a, b, chr(r if 32 < r < 128 else 0x20), a == b)

        assert hmac.compare_digest(self.pub_key, calc_pub_key)
```

Basically, every byte B is signed by hashing privkey 255-X times, and verified by
hashing the result of the above X times and comparing it with privkey hashed 255
times (aka the pubkey).

After understanding what's going on, we immediately notice that we can decrease
any byte in the message and still forge a valid signature (by computing a
hash once). So we can take a valid signature for `My favorite number is 1299072346121938061`
and change it for a signature for `My faflagte number is 1299072346121938061`.

The only problem is the checksum - there is a md5 sum at the end of the input
that must match the data. We bruteforced the number at the end, so that
every byte of the new md5 will be smaller than the old one, and solved the
challenge.

Core of the exploit looks like this:

```python

def fixup(sign, n, fromwhat, towhat):
    frag = chonks(sign, 32)
    for i, c in enumerate(towhat):
        off = n + i
        for _ in range(fromwhat[i] - c):
            frag[off] = hashlib.md5(bytes.fromhex(frag[off])).hexdigest()
    return "".join(frag)


def wrap(raw):
    raw = raw + b"\x00" * (128 - 16 - len(raw))
    return hashlib.md5(raw).digest()

origmd5 = wrap(msg)
podpis = fixup(podpis, 5, b"vori", b"flag")
msg = msg[:5] + b"flag" + msg[9:]

N = 6
for rndchrs in itertools.product(string.ascii_uppercase, repeat=N):
    rndfrag = ''.join(rndchrs).encode()
    msg = msg[:12] + rndfrag + msg[18:]

    newmd5 = wrap(msg)
    for a, b in zip(origmd5, newmd5):
        if a < b:
            break
    else:
        break

podpis = fixup(podpis, 12, b"number", rndfrag)
podpis = fixup(podpis, 112, origmd5, newmd5)
```

It's unnecessarily complicated, but still got the job done.

```
SaF{better_stick_with_WOTS+}
```
