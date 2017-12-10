# Simon and Speck Block Ciphers (Crypto, 100p)

```
Simon_96_64, ECB, key="SECCON{xxxx}", plain=0x6d564d37426e6e71, cipher=0xbb5d12ba422834b5 
```

In the task we get the plaintext, ciphertext and the information what is the encryption.
We also get the key with 4 missing characters.
It seems like a good target to simply brute-force, because 4 bytes is not much.

We found the Simon algorithm at https://github.com/inmcm/Simon_Speck_Ciphers/blob/master/Python/simon.py and we prepared a simple brute-force script:

```python
from crypto_commons.brute.brute import brute
from crypto_commons.generic import bytes_to_long

dataset = string.uppercase + string.lowercase + string.digits + string.punctuation + " "

def worker(a):
    print(a)
    for b in dataset:
        for c in dataset:
            for d in dataset:
                # Simon_96_64, ECB, key = "SECCON{xxxx}", plain = 0x6d564d37426e6e71, cipher = 0xbb5d12ba422834b5
                key = "SECCON{" + a + b + c + d + "}"
                w = SimonCipher(bytes_to_long(key), key_size=96, block_size=64)
                t = w.encrypt(0x6d564d37426e6e71)
                if t == 0xbb5d12ba422834b5:
                    print(key)
                    sys.exit(0)


if __name__ == "__main__":
    brute(worker, dataset, 7)
```

Nothing special here, we simply try every 4 character combination as the key, until the ciphertext matches.

It was pretty slow so we used PyPy and multiprocessing to run in paralell on multiple cores.
After a while we got: `SECCON{6Pz0}`
