# Decrypt message (Crypto, 700p)

In the task we get access to a webpage where we can put username and it stores some encrypted string in our cookie.
The value from cookie must store our username since it's later displayed on the webpage.

We start off by trying to play around with the encryption oracle and with the ciphertext we have.
We can notice quickly that:

- It's a 16 byte block crypto - we can see alignment by 16 bytes
- It is using some block chaining method, because many blocks of identical input  are encrypted differently

Fortunately errors are printed to the screen so we can get some information about the code running there by changing the ciphertext we have.

- It's actually AES CBC with random IV stored as first block of the ciphertext
- Data are stored as JSON and there is some more data behind our input
- Data are being decoded into ascii before printing out on the screen, so if the data decrypt into some non-ascii values then we get encoding error

First we recover the whole data, using the encoding error messages.
We can change k-th byte of the IV until the decryption fails with encoding error and it will tell us how the k-th data byte in first block was finally decrypted.
Since we know how we changed the IV we can recover the initial plaintext value on the server.
This was we know that the plaitext is `{"name": "our_input","show_flag": false}`.

It's clear now that we need to set the parameter `show_flag` to `true` to get the flag.

It's AES CBC so we can easily influence decryption of a single block by changing the IV, but here we need to work with 2 blocks, because the code checks for `name` parameter before it checks the `show_flag` parameter.
So we need to have both and this means 2 blocks.

This is tricky, because to force decryption of second block we need to change the first block, and this will make this first block to decrypt into some garbage values.
However, we can use the IV to "fix" the first block decryption afterwards.
We can again use the fact that server tells us when it can't decode a certain value, so we know how certain byte was decrypted on the server, and we can change the IV byte accordingly.

Since we know exactly the plaintext and ciphertext, and we know what plaintext we want to get, we can right away use xor to get the first block ciphertext we need.
Rest is just using the IV to force this first block to decrypt to expected value.

```python
import base64

import requests
from crypto_commons.generic import xor_string


def get_ciphertext(plaintext):
    url = "http://95.85.51.183/?name=" + plaintext
    result = requests.get(url)
    return result.cookies['user_info'].decode("base64").encode("hex")


def get_plaintext(ciphertext):
    url = "http://95.85.51.183/"
    payload = base64.b64encode(ciphertext.decode("hex"))
    result = requests.get(url, cookies={'user_info': payload})
    return result.content


def main():
    forged_ct = get_ciphertext("a" * 22).decode("hex")
    ct_block_1 = forged_ct[16:32]
    ct_block_2 = forged_ct[32:48]
    orig = """{"name": "aaaaaaaaaaaaaaaaaaaaaa"""
    want = """{"name": "aaaaa","show_flag":1}\1"""
    pt_block_2 = orig[16:32]
    expected_pt_block_1 = want[:16]
    expected_pt_block_2 = want[16:32]
    c1 = xor_string(xor_string(pt_block_2, expected_pt_block_2), ct_block_1)
    new_iv = ""
    for index in range(16):
        for i in range(256):
            print('testing value %d at index %d' % (i, index))
            forged_ct = new_iv + chr(i)
            forged_ct += (16 - len(forged_ct)) * "a"
            forged_ct += c1 + ct_block_2
            pt = get_plaintext(forged_ct.encode("hex"))
            if "t decode byte" in pt:
                decrypted_byte = pt.split("t decode byte")[1].split()[0].strip()
                position = pt.split("position")[1].split(":")[0]
                if int(position.strip()) != index:
                    continue
                print index, new_iv.encode("hex"), pt
                decrypted_byte = int(decrypted_byte, 16)
                real = decrypted_byte ^ ord(expected_pt_block_1[index]) ^ i
                new_iv += chr(real)
                break
    print get_plaintext((new_iv + c1 + ct_block_2).encode("hex"))


main()
```

And we get: `Flag: KLCTFFDA616A6DAF4E63A9F7B55B43124E548`
