# Easy pub (crypto)

In the task we get [source code](easypub.py) of a service.
We can `register` there and we get some kind of ticket with signatures, which we can use to login.
If we login as admin, we will get the flag, but this requires some `secret admin key`.

This secret key is embedded in ticket we get:

```python
msg = name + b'\x00' + bytes(admin_k, 'ISO-8859-1')
if size(bytes_to_long(msg)) > 700:
	print('Too long username')
	continue
msg = msg + urandom(120 - len(msg))
msg = bytes_to_long(msg)
if msg % 2 == 1:
	msg += 1
sig = cry.sign(msg)
ticket = cry.encrypt(msg)
print(ticket)
print(sig[0])
print(sig[1])
```

So if we could decrypt the ticket, we would get the necessary `admin_k` value.
There are two things to notice here already:

- We can cause an error when `name + b'\x00' + bytes(admin_k, 'ISO-8859-1')` is longer than 700 bits, and therefore we can easily recover the length of `admin_k` by iteratively sending longer names. From this we get that the length of the secret key is 45 bytes long.
- The script makes sure that the `msg` is an even number.

When we try to login we're asked for the ticket and signatures:

```
elif choice[0] == 'l':
	ticket = int(input('ticket:>>'))
	sig0 = int(input('sig[0]'))
	sig1 = int(input('sig[1]'))
	msg = cry.decrypt(ticket)
	if msg % 2 == 1:
		print('A bit is wrong, may be something is wrong.')
		continue
	if cry.verify(msg, (sig0, sig1)) == cry.verify(msg, (sig1, sig0)):
		print('Wrong signature!')
```

The script checks if the decrypted message is still even (as it should be), and if it's not there is an error message.

If we look at how the ticket encryption works it's simply:

```python
    def encrypt(self, msg):
        return self.rsa.encrypt(msg, None)[0]
```

So a textbook RSA encryption.
When we connect to the challenge we get the public key (e,n) values.

I don't really know what was the purpose of the ElGamal signature here, because we already have all that we need.
We have a Least-Significant-Bit Oracle here.
We can send encrypted payload to the server, and the server tells us if the LSB is 1 (error message) or 0 (no error message).

We've already described the approach for such case:

- https://github.com/p4-team/ctf/tree/master/2016-04-15-plaid-ctf/crypto_rabit
- https://github.com/p4-team/ctf/tree/master/2016-12-16-sharifctf7/crypto_150_lsb

So we won't go into much details here.
Long story short, we can use binary search to narrow-down the value of decrypted plaintext.

We know that `n` is a product of some prime numbers, which are all `odd` (except for 2, but we can see it's not the case).
Therefore `n` itself has to be `odd` as well.
Textbook RSA is simply: 

`msg^e mod n` 

and therefore if we multiply this by 

`2^e mod n`

we get

`(msg^e * 2^e) mod n = (msg*2)^e mod n`

And `2*x` has to be `even` number.

Now if `msg*2` is smaller than `n` the `mod n` operation does nothing, and the result is still `even`.
But if `msg*2` is bigger than `n` then `mod n` operation will cut the number, and since `n` is `odd` the result will be `odd` as well.

If we therefore use our LSB Oracle and check the last bit of `msg*2` we will know if `msg` is smaller or bigger than `n/2`.
Then we can repeat the whole process using `msg*4` again narrowing down the upper or lower limit for the `msg`.

We have a solver for this in crypto-commons: https://github.com/p4-team/crypto-commons/blob/master/crypto_commons/oracle/lsb_oracle.py

So we can run:

```python
from crypto_commons.netcat.netcat_commons import nc, send, receive_until_match
from crypto_commons.oracle.lsb_oracle import lsb_oracle


def oracle(s, payload):
    send(s, 'l')
    receive_until_match(s, "\:\>\>", None)
    send(s, str(payload))
    send(s, str(1))
    send(s, str(1))
    data = receive_until_match(s, "\:\>\>", None)
    return "bit is wrong" in data


def multiplicate(x, e, n):
    return (pow(2, e, n) * x) % n


def main():
    url = "47.75.53.178"
    port = 9999
    s = nc(url, port)
    data = receive_until_match(s, "\:\>\>", None).split("\n")
    e = int(data[1])
    n = int(data[2])
    print(e, n)
    send(s, 'r')
    receive_until_match(s, "\:\>\>", None).split("\n")
    send(s, 'test')
    data = receive_until_match(s, "\:\>\>", None).split("\n")
    ct = int(data[0])
    lsb_oracle(ct, lambda x: multiplicate(x, e, n), n, lambda ct: oracle(s, ct))


main()
```

The server was very slow and the timeout was 200s, so we could not recover the full `msg` but we managed to get:

```
bit = 841
upper = 4430931344985544684813124199015272502018314572043348981999211916350388629990315386099138633492940320015200000014369473301421041939195746043762808791461201289927287863927440625964711109289704498508938867370891142910412212369289674088889782436698592352015196254176928757848616673440497064363
upper flag = test1qsxcvghyu89olkmnbvd2#$%^&*()_OKMNBFRT:"><~&*m~?<???e?Ki???6??v?k??w??f?g?He)?ztҐ???4?xÆ?fJ?V???+u?å?٫
lower = 4430931344985544684813124199015272502018314572043348981999211916350388629990315386099138633492940320015200000014369473301421041939195746043762808791461201289927287863927440625964711109289704498508938867370891142910412212369289674088880817920880377586923723058411773091162928984722671831723
lower flag = test1qsxcvghyu89olkmnbvd2#$%^&*()_OKMNBFRT:"><~&*m~?<???e?Ki???6??v?k??w??f?g?He)?ztҐ???4?õ????    7ݤU?T)?Ɗ?
```

We used username `test`, and we know that we need 45 bytes after `\x00` marker, and we can see that already both upper and lower approximation are equal for more than that so the secret key we need is `1qsxcvghyu89olkmnbvd2#$%^&*()_OKMNBFRT:"><~&*`

We can now try to login as admin and recover the flag: `HITBXCTF{easy_pub_so_c000l}`
