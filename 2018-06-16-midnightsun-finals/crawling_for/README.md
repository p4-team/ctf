# Crawling Code Creature (re/for)

This was marked as Reverse challenge, but we solved it like a forensics problem.
In the task we get a coredump of python process.

We tried loading this into gdb, but with not much luck.
The symbols didn't match and we couldn't really navigate much over what we had.

As a result we decided to use classic tools like `vi, grep, regex, strings`.
Going over the strings in the file we noticed a couple of things.
The user was sending http requests to some application running on localhost with:
```
r1 = requests.get('http://localhost:5000/message')
```
and
```
r2 = requests.get('http://localhost:5000/key')
```

There was also `from Crypto.Cipher import AES` which would suggest that something is encrypted with AES.
Finally we also found some interesting long hex-encoded strings, which were not coming from the documentation:

`f0623892bc68e01d3206407fa3a84a2bf0d68d57dc3b97a31b1952a8227348a9`
and 
`f8fa35b181005f76b9eb1f867dd85ea35d4049db6e24cc92b15bbc2abed1d7b0afc8238afd7a2f7384e4becff92ce9fc`

First one is 32 bytes long, so could be AES key, the other one could then be a ciphertext.

```python
from Crypto.Cipher import AES


def main():
    key = 'f0623892bc68e01d3206407fa3a84a2bf0d68d57dc3b97a31b1952a8227348a9'.decode("hex")
    msg = 'f8fa35b181005f76b9eb1f867dd85ea35d4049db6e24cc92b15bbc2abed1d7b0afc8238afd7a2f7384e4becff92ce9fc'.decode("hex")
    encrypt = AES.new(key, AES.MODE_ECB, '\0' * 16)
    decrypted = encrypt.decrypt(msg)
    print(decrypted)


main()
```

Which gives us `midnight{c4n_you_r3v1ve_4_d34d_snek}`
