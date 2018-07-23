# USSH (crypto, 31 solved, 138p)

```
We've developed a new restricted shell. It also allows to manage user access more securely. 
Let's try it nc crypto-01.v7frkwrfyhsjtbpfcppnu.ctfz.one 1337
```

In the task we get access to a blackbox restricted shell.
We can use command `help` to get list of available commands and there are:

```
abcd@crypto: $ help
Avaliable commands: ls, cat, id, session, help, exit
```

We can list the directory and there is a `flag.txt` there, but we can't use `cat` on it because we are not root.

First interesting function is `id`, which returns:

```
abcd@crypto: $ id
uid=3(regular) gid=3(regular) groups=3(regular)
```

The really interesting function is `session`.
We can get or set a session with this command.
Getting the session gives us:

```
abcd@crypto: $ session --get
avRMXhMPfzzwhK5WDJhE7w==:EP2QRrs0I0y9H3Zzen2V1t7cMPGxjIQGVZ/Y+STDo6M=
```

Both parts decode to some random bytes.
If we change username the blocks change - first one is always 16 bytes long, but the other one expands by 16 bytes.
This indicates some block crypto with 16 bytes blocks.
We can use `session --set` to play around with those parameters, and if we give fewer bytes for the first part, we get a nice error that `IV has to be 16 bytes long`.
This answer the question what those parts are - first part is IV and the second part is some encrypted payload.

Flipping bytes of the IV by 1 bit cause the session to be `invalid` for the first few bytes, but once we flip 10th byte our prompt change!

```python
    url = 'crypto-01.v7frkwrfyhsjtbpfcppnu.ctfz.one'
    s = nc(url, 1337)
    s.recv(9999)
    login = 'a' * 7
    send(s, login)
    receive_until_match(s, '\$ ')
    send(s, 'session --get')
    session = receive_until(s, "\n")[:-1]
    print(session)
    receive_until_match(s, '\$ ')
    iv, ct = map(base64.b64decode, session.split(":"))
    iv = xor_string(iv, "".join(map(chr, [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0])))
    new_session = base64.b64encode(iv) + ":" + base64.b64encode(ct)
    send(s, 'session --set ' + new_session)
    result = receive_until_match(s, '\$ ')
    print(result)
```

Which gives:

```
caaaaaa@crypto: $ 
```

And since `chr(ord('a')^2)) == 'c'`, we can confirm that in the payload we provide the 10th byte is where our `login` is stored.

For some reason flipping any bit of the first 9 bytes causes the `session is invalid` error, so we guess that the data have to be stored in some structure, most likely JSON, so prefix is something like `{'user':'`.

We can run:

```python
    url = 'crypto-01.v7frkwrfyhsjtbpfcppnu.ctfz.one'
    for i in range(1, 16):
        s = nc(url, 1337)
        s.recv(9999)
        login = 'a' * i
        send(s, login)
        receive_until_match(s, '\$ ')
        send(s, 'session --get')
        session = receive_until(s, "\n")[:-1]
        print(session)
        receive_until_match(s, '\$ ')
        iv, ct = map(base64.b64decode, session.split(":"))
        print(i, len(ct))
        s.close()
```

And we see that once our login name is 9 bytes long a 3rd ciphertext block appears, so at this point the whole payload takes 2 blocks (the new block is only PKCS padding).
So we've got 9 bytes of prefix, 9 bytes of login name, and suffix, and it all takes 32 bytes -> suffix is 14 bytes long.
We're lucky!
This means we can bitflip the whole suffix if we want to, because it never exceeds a single block.

Our guess is that the group name is stored in this suffix, so we need to find the position and then bitflip it to `root`.

We can't bitflip the first ciphertext block, because it has some fixed prefix, which would break.
We need to create a whole another block to work with.
For this we can send a long login, which will fill the first block (7 characters) and then fill whole another block as well (16 characters).
This way we can bitflip the second block, because it will only "break" the second part of our login name, and we don't care about it at all.

Again we can run a simple loop, just like we did flipping IV, but this time flipping second block of ciphertext, and we can observer the results of `id` function.
We know that the whole suffix has to fit in the third block of ciphertext, since we just pushed it there.

```python
    url = 'crypto-01.v7frkwrfyhsjtbpfcppnu.ctfz.one'
    s = nc(url, 1337)
    s.recv(9999)
    login = 'a' * (7 + 16)
    send(s, login)
    receive_until_match(s, '\$ ')
    send(s, 'session --get')
    session = receive_until(s, "\n")[:-1]
    print(session)
    receive_until_match(s, '\$ ')
    iv, ct = map(base64.b64decode, session.split(":"))
    real_ct = ct
    for i in range(48):
        xor_block = [0] * 48
        xor_block[i] = 2
        ct = xor_string("".join(map(chr, xor_block)), real_ct)
        new_session = base64.b64encode(iv) + ":" + base64.b64encode(ct)
        send(s, 'session --set ' + new_session)
        result = receive_until_match(s, '\$ ')
        if 'Invalid' not in result and "PKCS7" not in result:
            print(i, xor_block)
            send(s, 'id')
            print(receive_until_match(s, '\$ '))
```

From this we can see:

```
(23, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
uid=3(pegular) gid=3(pegular) groups=3(pegular)
(24, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
uid=3(rggular) gid=3(rggular) groups=3(rggular)
(25, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
uid=3(reeular) gid=3(reeular) groups=3(reeular)
(26, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
uid=3(regwlar) gid=3(regwlar) groups=3(regwlar)
(27, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
uid=3(regunar) gid=3(regunar) groups=3(regunar)
(28, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
uid=3(regulcr) gid=3(regulcr) groups=3(regulcr)
(29, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
uid=3(regulap) gid=3(regulap) groups=3(regulap)
(30, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
uid=3(regular) gid=3(regular) groups=3(regular)
```

So it's clear that flipping byte `23` changes the first letter of group name.
The only thing left is calculate the necessary xor block to change `regular` into `root`:

```python
import base64

from crypto_commons.generic import xor_string
from crypto_commons.netcat.netcat_commons import nc, send, receive_until_match, receive_until


def main():
    url = 'crypto-01.v7frkwrfyhsjtbpfcppnu.ctfz.one'
    s = nc(url, 1337)
    s.recv(9999)
    login = 'a' * (7 + 16)
    send(s, login)
    receive_until_match(s, '\$ ')
    send(s, 'session --get')
    session = receive_until(s, "\n")[:-1]
    print(session)
    receive_until_match(s, '\$ ')
    iv, ct = map(base64.b64decode, session.split(":"))
    real_ct = ct
    data = 'regular)'
    sp_xor_block = map(ord, xor_string(data, 'root)   '))
    for i in range(256): # brute force the last byte to close the string
        xor_block = [0] * 23 + sp_xor_block + [i] + [0] * 16
        ct = xor_string("".join(map(chr, xor_block)), real_ct)
        new_session = base64.b64encode(iv) + ":" + base64.b64encode(ct)
        send(s, 'session --set ' + new_session)
        result = receive_until_match(s, '\$ ')
        if 'Invalid' not in result and "PKCS7" not in result:
            print(i, xor_block, result)
            send(s, 'id')
            print(receive_until_match(s, '\$ '))
            send(s, 'cat flag.txt')
            result = receive_until_match(s, '\$ ')
            if 'ctfzone' in result:
                print(result)
                break


main()
```

And we get `ctfzone{2e71b73d355eac0ce5a90b53bf4c03b2}`
