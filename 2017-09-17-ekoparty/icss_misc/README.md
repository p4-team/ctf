# ICSS (Misc/Crypto, 471p, 18 solved)

A blackbox crypto challenge.
We get a base64 encoded ciphertext `ypovStywDFkNEotWNc3AxtlL2IwWKuJA1qawdvYynITDDIpknntQR1gB+Nzl` and access to a service which can encrypt for us up to 6 characters of input.

First we need to understand how this encryption works, and for this we played a bit with it, sending specially crafted payloads.
We can notice some things:

1. Encryption goes character by character, there are no blocks. It's easy to see when we add or remove characters.

2. Ciphertext for a character depends on the character itself and on the position where it is in the input. The same character on a different position encrypts differently, but the same character at the same position, even for different plaintexts gives the same encrypted value.
For example:
aaa -> a060a2
aba -> a063a2

So the encryption for the last `a` stayed the same.

3. An exception to above rule is the first character. It affects how rest of the string is encrypted.

Another set of tests we did gave some interesting results. 
By sending `\x00\x00\x00\x00\x00\x00` bytes we got `010102030508` which looks like a Fibonacci sequence!
It got even better when we sent `\x01\x00\x00\x00\x00\x00` because we got `00020305080d` which is the same sequence just shifter 1 position further (disregarding the first byte).
If we now send `\x01\x05\x00\x00\x00\x00` we will get `00070305080d` so the sequence is the same but second byte is bigger by 5, which is the value we tried to encrypt.
First byte encryption is unknown, but it depends only on this character, so we don't really care, it can be brute-forced.

We did a bit more checking and it was quite clear that the encryption does something like:
1. Encrypt first byte in some special way
2. Every other byte in position `k` is encrypted as `Fibonacci(first_byte + k) + kth_byte_value`

However, there is some weird stuff happening when overflow is reached, and it seemed some other special cases are present as well for even/odd numbers.

Instead of trying to figure out how to handle those issues, we decided to go the "easy" way instead.
We know that by changing the first byte we can "shift" the Fibonacci sequence for the rest of the encryption, but it means that we basically shift the positions!
By sending `Xa` we can get encrypted byte `a` at positon `1` with starting byte `X`, but if we send `(X+1)a` we will shift the sequence and the result will be the same as encrypted `a` at position `2` with starting byte `X`.

This means that we can pretty much get any encrypted byte at any position we want by encrypting only 2 bytes at a time!
We use this approach with the server as "oracle" serving us the encrypted bytes and we brute-force the flag.

What we want to do:
1. Take a single encrypted character from the encrypted flag we have at k-th position.
2. Encrypt via server every possible character at k-th position and compare it with the one we have. Once they match we know what was the plaintext character.
3. Repeat until we get whole flag.

So we run:

```python
import base64
import string

from crypto_commons.netcat.netcat_commons import nc, send


def brute_character_at_position(position, expected):
    for c in string.letters + "{_" + string.digits + string.punctuation:
        if int(get_encrypted_char_at_position(c, position), 16) == ord(expected):
            return c
    return "?"


def get_encrypted_char_at_position(character, position):
    return get_ciphertext(chr(ord('E') + position) + character)[2:4]


def get_ciphertext(c):
    url = 'icss.ctf.site'
    port = 40112
    s = nc(url, port)
    s.recv(9999)
    s.recv(9999)
    send(s, c)
    s.recv(9999)
    result = s.recv(9999)
    return base64.b64decode(result).encode("hex")


def main():
    flag_ciphertext = base64.b64decode("ypovStywDFkNEotWNc3AxtlL2IwWKuJA1qawdvYynITDDIpknntQR1gB+Nzl")
    flag_plaintext = "E"
    for i in range(len(flag_ciphertext) - 1):
        expected_encrypted_byte = flag_ciphertext[i + 1]
        flag_plaintext += brute_character_at_position(i, expected_encrypted_byte)
        print(flag_plaintext)
    print(flag_plaintext)


main()
```

After a while we finally get: `EKO{Mr_Leon4rd0_PisAno_Big0770_AKA_Fib@nacc!}`
