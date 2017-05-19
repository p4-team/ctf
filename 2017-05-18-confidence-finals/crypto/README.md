# ??? (crypto, 300p)

## ENG

We are given file with "crypto service (see attached [enc_service.c](enc_service.c) ).

There are 16 "slots" for encryption keys in binary, and we have four operations:
 - copy key from Ith slot to `"current_key"` slot (if Ith key is shorter than `current_key`, not all will be overwritten).
 - change Ith key to N random bytes
 - change `data`
 - encrypt `data` with 16 bytes of `current_key`.

My solution was not perfect, because it turned out that there was easier way, but i'll describe it anyway.

Code initially looks conceptually like this:
 - data = read('flag')
 - print `encrypt_data()`

data is memzeroed after this, and the original key is only in `current_key`.

So how can we solve this? First i tried overwritting first byte of `current_key`, until i get the same results.

So the situation looked like this:

```
current key:    [K0, K1, K2, K3, K4, ...]
K0:             [K0, ?,  ?,  ?,  ?,  ...]
```

and code more or less like this:

```python
good = encrypt()
while True:
    regenerate(0, 1)
    load(0)
    next = encrypt()

    if next == good:
        break
```

after that, i repeated this for next bytes, and situation looked like this:

```
current key:    [K0, K1, K2, K3, K4, ...]
K0:             [K0, ?,  ?,  ?,  ?,  ...]
K1:             [?,  K1, ?,  ?,  ?,  ...]
K2:             [?,  ? , K2, ?,  ?,  ...]
...
```

And code like this:

```python
for i in range(0, 15):
    print "and now, let's try to set KEYS[{}][{}] to VICTIM".format(i, i)

    while True:
        regenerate(i, i+1)

        for j in range(0, i+1)[::-1]:
            load(j)

        next = encrypt()
        print next, next == good
        if next == good:
            break
```

This was my first exploit, but it turned out not to be necessary (it only simplified next part a bit).

After that we noticed that overflow checking in functions is not correct:

```cpp
void regenerate_key(unsigned int index, unsigned int len) {
        unsigned int offset = index * ENTRY_SIZE;

        if (offset > STORAGE_SIZE - ENTRY_SIZE || len > MAX_KEY_LEN) {
                return;
        }

        int fd = open("/dev/urandom", O_RDONLY);
        read(fd, &keys[offset], len);
        close(fd);
        keys[offset + MAX_KEY_LEN] = len;
}
```

if offset was really large, it would overflow and in fact we could overwrite arbitrary byte to zero.
We used it to overwrite whole keys[15] to zeroes:

```python
def overwrite_keys15():
    print 'ok, now overwrite keys[15] to zeroes'
    print 'we want index * ENTRY_SIZE + 16 == 14*ENTRY_SIZE + j for j in range(16)'
    regenerate(15, 16)
    print 'good so far:'
    print encrypt()
    for j in range(16):
        index = (15*17 - 16 + j) * modinv(17, 2**32) % 2**32
        print 'for {} index {}'.format(j, index)
        regenerate(index, 0)

    print 'sanity...'
    loaddata('A'*16)
    load(15)
    sanity = encrypt()
    assert sanity == 'b49cbf19d357e6e1f6845c30fd5b63e3'
```

After that, solution was trivial: just encrypt anything with keys:

```
K0, 0, 0, 0, 0, ...
K0, K1, 0, 0, 0, ...
K0, K1, K2, 0, 0, ...
...
```

Like this:

```python
partials = []
for i in range(15):
    load(15)  # curkey = 0
    for j in range(i+1)[::-1]:
        load(j)

    next = encrypt()
    print 'next', next
    partials.append(next)


print 'ok, lets hope itll work'
for p in partials:
    print p

print 'and teh flag...'
print flag
```

And after that just recover the key and flag:

```
from Crypto.Cipher import AES

partials = [
'66dbd655bc51bab87329c3f6bdeb5aa0',
'fee1d80da69f2144f3a951c085c5bc64',
'7ceaf1c485e6703afc2334bd14b42268',
'52f684bebc5453ea6e76075c2e03e1ab',
'bdca9198d9691f0811b178749ee41202',
'e9667a0459c7da520b73279e6cf3fb42',
'056da1d9b0504b34f012a21b84e3cdc2',
'38029eb3e57569c3dd36f75142f58580',
'c22ce237ba0543f23f36c88aa79f3140',
'a475c86bb894b285c080a90b76383927',
'45bc0a0bb4f98cd4388bff76f058bd7a',
'846dbb2d1380d4513ad4ce2d376f206c',
'f6e81706b8ea2051b926698cc584c26e',
'4e3ef31fab662337d551aaf202d2c047',
'05f61ce44e216db3ad8264f031086dbb',
]
flag = 'cefff6adc9392ba7e6abe6513c6d4467'.decode('hex')
data = 'A' * 16

key = [0] * 16
print len(partials)
for i, p in enumerate(partials):
    p = p.decode('hex')
    for j in range(256):
        key[i] = j
        kk = ''.join(chr(c) for c in key)
        if AES.new(kk).decrypt(p) == data:
            print 'got', j
            break

for i in range(256):
    for j in range(256):
        key[15] = i
        key[0] = j
        kk = ''.join(chr(c) for c in key)
        ff = AES.new(kk).decrypt(flag)
        if all(20 < ord(c) < 0x7f for c in ff):
            print ff
```

Flag:

```
Drgns{f2Br#@!#d}
```
