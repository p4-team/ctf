# My simple cipher (crypto)

In the task we get a simple encryption code:

```python
import sys
import random

key = sys.argv[1]
flag = '**CENSORED**'

assert len(key) == 13
assert max([ord(char) for char in key]) < 128
assert max([ord(char) for char in flag]) < 128

message = flag + "|" + key

encrypted = chr(random.randint(0, 128))

for i in range(0, len(message)):
  encrypted += chr((ord(message[i]) + ord(key[i % len(key)]) + ord(encrypted[i])) % 128)

print(encrypted.encode('hex'))
```

And resulting ciphertext: `7c153a474b6a2d3f7d3f7328703e6c2d243a083e2e773c45547748667c1511333f4f745e
`

We know that bytes of key and flag are < 128 and we of course know that the flag starts with `TWCTF{`.
It's clear that this can be inverted by hand, but we're too lazy for that and we simply used the code to generate constraints on the parameter and asked Z3 for the flag.

We know constraints:

- flag and key are < 128 and >= 0
- flag starts with `TWCTF{`
- one character is `|`

On top of that we can run the code and generate constraints on the way directly from encryption code:

```python
def read_data():
    return "7c153a474b6a2d3f7d3f7328703e6c2d243a083e2e773c45547748667c1511333f4f745e".decode("hex")


def decryptor():
    data = read_data()
    s = z3.Solver()
    flag = [z3.Int("flag_" + str(i)) for i in range(len(data) - 15)]
    key = [z3.Int("key_" + str(i)) for i in range(13)]
    pipe = z3.Int("pipe")
    s.add(pipe == ord("|"))
    for var in flag:
        s.add(var < 128)
        s.add(var >= 0)
    for i, c in enumerate("TWCTF{"):
        s.add(flag[i] == ord(c))
    for var in key:
        s.add(var < 128)
        s.add(var >= 0)
    message = flag + [pipe] + key
    for i in range(1, len(data)):
        index = i - 1
        byte = ord(data[i])
        s.add((message[index] + key[index % 13] + ord(data[index])) % 128 == byte)
    print(s.check())
    print(s.model())
    print("".join([chr(int(str(s.model()[var]))) for var in message]))
```

Which gives us `TWCTF{Crypto-is-fun!}|ENJ0YHOLIDAY!`
