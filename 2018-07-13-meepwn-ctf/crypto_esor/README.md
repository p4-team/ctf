# ESOR (crypto, 130 solved, 100p)

In the challenge we get the [source code](testpoodle.py) and socket address of the server.
Judging by the challenge name, it was supposed to be some kind of POODLE attack scenario, but it was actually broken.

In this challenge we could connect to the server and get flag AES-CBC-encrypted with prefix and suffix selected by us.
There would also be HMAC included in the ciphertext.
We could also try decrypting given payloads, but it would only tell us if the decryption and HMAC was ok.

The mistake is here:

```python
encrypt_key = '\xff' * 32
```

The actual encryption key was hardcoded in the application and not changed, which means we could simply get the encrypted flag from the server and decrypt it using the code provided in the task.

```python
def main():
    s = nc("206.189.92.209", 12345)
    receive_until_match(s, "3\. quit")
    send(s, '1')
    receive_until_match(s, "prefix:")
    send(s, 'x')
    receive_until_match(s, "suffix:")
    send(s, 'y')
    flag = receive_until_match(s, "\n").strip()
    print(decrypt(flag))


main()
```

And get back `xMeePwnCTF{pooDL3-this-is-la-vie-en-rose-P00dle!}`
