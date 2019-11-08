# Crypto (crypto, 136p, 12 solved)

In the challenge we get an [encryption code](enc.py) and encrypted flag `a22d0fb9f707b153ab68472082d1f3e977a23f3dc0de469388ec3a56131943eba1873071f7fc01b5fc31b5335056286f5d7634735f35776a74`

One we analyse the code we can clearly see the vulnerability -> there are 2 things which are supposed to encrypt the data, subtraction and XOR.
However the parameters are created by:

```python
a, b, c = (int(key[i:i + 8], 16) for i in range(0, len(key), 8))
```

The values `b` and `c` are both rotated left as 64 bit values, while they're were in fact created from 8 bits values only. This means very quickly both of them will become `0`.
This leaves the subtraction step.
We could try to invert the encryption knowing the flag prefix, and recover the parameters one by one.
But we're too lazy for that.
The operations are really only `+-` and `&^`, so we can just ask Z3 to do the work for us.

We port the encryption function to make it easier to use from Z3:

```python
def encryptx(data, key):
    encrypted = []
    a, b, c = key
    for d in data:
        keystream = (b & 0xff) ^ (c & 0xff)
        d = (d - (a & 0xff)) ^ keystream
        d = d & 0xff
        encrypted.append(d)
        a = rotr(a)
        b = rotl(b)
        c = rotl(c)
        # print(a, b, c)
    return encrypted
```

No we can run Z3 on this:

```python
def decrypt(ct):
    key = tuple([BitVec('k%d' % i, 64) for i in range(3)])
    flag = [BitVec('x%d' % i, 64) for i in range(len(ct) / 2)]
    s = Solver()
    for x in flag:
        s.add(x > 0, x < 128)
        s.add(Or(x == 32, x > 32))
    result = encryptx(flag, key)
    for i, x in enumerate(ct.decode("hex")):
        s.add(result[i] == ord(x))
    for i, c in enumerate("Congrats! Flag is: "):
        s.add(flag[i] == ord(c))
    s.check()
    model = s.model()
    solution = [model[x].as_long() for x in flag]
    print("".join(map(chr, solution)))
    return "".join(map(chr, [model[x].as_long() for x in flag]))
```

Initially we didn't know the prefix so we didn't have the `Congrats! Flag is: ` value and the encryption was ambigious, so in the end we looped over this and instructed Z3 to enumerate other solutions (by rejecting the solution and adding more constraints on characters not matching the charset).

This way we arrive at the flag prefix and most of the flag as well.
However, for some reason the suffix was wrong.
Since we know the sha1 of the whole payload, we could brute-force the missing few last characters:

```python
    ct = 'a22d0fb9f707b153ab68472082d1f3e977a23f3dc0de469388ec3a56131943eba1873071f7fc01b5fc31b5335056286f5d7634735f35776a74'
    h = ct[:40]
    flag = "Congrats! Flag is: DCTF{th1s_w4s_"
    for a in range(128):
        for b in range(128):
            for c in range(128):
                data = flag + chr(a) + chr(b) + chr(c) + "}"
                digest = hashlib.sha1(data).hexdigest()
                if digest == h:
                    print(data)
```

Evetually we get the flag: `Congrats! Flag is: DCTF{th1s_w4s_4un}`
