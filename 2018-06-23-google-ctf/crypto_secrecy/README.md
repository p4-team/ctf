# Perfect secrecy (crypto 158p, 74 solved)

In the task we get the [source code](challenge.py) of the server application, [encrypted flag](flag.txt) and RSA [public key](key_pub.pem).
The important part is just:

```python
    m0 = reader.read(1)
    m1 = reader.read(1)
    ciphertext = reader.read(private_key.public_key().key_size // 8)
    dice = RsaDecrypt(private_key, ciphertext)
    for rounds in range(100):
      p = [m0, m1][dice & 1]
      k = random.randint(0, 2)
      c = (ord(p) + k) % 2
      writer.write(bytes((c,)))
    writer.flush()
```

Other than that we've got textbook RSA decryption, with no padding, so we can use homomorphic properties of RSA.

The server reads from us 2 bytes and then message to decrypt.
Then the message gets decrypted via RSA and last bit of the plaintext is extracted.
Then the bit is used to get one of the bytes we provided, and value `(ord(our_byte)+random.randint(0, 2)) %2` is calculated.
We get back 100 such values.

The setup of the task is pretty obvious Least Significant Bit Oracle, which we described a couple of times already:
- https://github.com/p4-team/ctf/tree/master/2016-04-15-plaid-ctf/crypto_rabit
- https://github.com/p4-team/ctf/tree/master/2016-12-16-sharifctf7/crypto_150_lsb

The twist here is that we don't get the last bit directly.
However, in reality it's not an issue for us, if we consider this for a moment.
The trick is that `random.randint(0, 2)` returns values from `[0,1,2]`:

```
random.randint(a, b)
    Return a random integer N such that a <= N <= b.
```
https://docs.python.org/2/library/random.html#random.randint

Let's assume we send values `\1` and `\2` as input bytes, or any other values where one is even and one odd.
- If the last bit was `0` then we select `\1` and add to it one of the random values, getting as result one of `[1,2,3]`
- If the last bit was `1` then we select `\2` and add to it one of the random values, getting as result one of `[2,3,4]`

Now we apply modular division on those results and for bit `0` we get `[1,0,1]` and for bit `1` we get `[0,1,0]`.
If we assume that random values have good distribution, then either of those results have the same probability.

This means that in 100 attempts, if the bit was `0` we should get roughly 33 times `0` and 66 times `1`, and conversly for bit `1` we should get 33 times `1` and 66 times `0`.
We can, therefore, simply calculate which values are prevalent to decide which was the real LSB of plaintext:

```python
def check_bit(data):
    one = 0
    zero = 0
    for result in data:
        if result == '\1':
            one += 1
        else:
            zero += 1
    print("diff", abs(zero - one))
    if one - zero > 10:
        return 0
    elif zero - one > 10:
        return 1
    else:
        print("not sure for " + str(zero) + " " + str(one))
        return -1
```

Just to be sure, we introduce a threshold of 10% - if the difference is too small, we assume we're not sure of the real result, and we would rather repeat the test to make sure.

Now we can get back to the LSB oracle attack.
The whole idea behind the attack is quite simple, and boils down to binary search combined with homomorphic multiplication of the plaintext by modifying ciphertext.
We can multiply plaintext by `2` if we multiply ciphertext by `pow(2,e,n)`. 
Proof:

```
ct = pt^e mod n
ct' = ct * 2^e mod n = pt^e mod n * 2^e mod n = 2pt^e mod n
ct'^d = (2pt^e mod n)^d mod n = 2pt^ed mod n = 2pt mod n
```

LSB from oracle tells us if the plaintext is even or odd.
Modulus `n` is a product of 2 large primes, so it has to be odd. 
`2*x` has to be even, for any natural number `x`.

If we ask the oracle about `2*PT mod N` then:

- If LSB is `0` (number is still even) then the number was smaller than modulus and therefore `2*PT < N` which means `PT < N/2`
- If LSB is `1` then the number was greater than modulus and therefore `2*PT > N` which means `PT > N/2`

If we then ask about LSB of `4*PT mod N` we can again get one of two possible results:

- If LSB is `0` then either `4*PT < N` which means `PT < N/4` if `PT < N/2` was true, or `PT < 3*N/4` if `PT > N/2` was true in previous step
- If LSB is `1` then either `4*PT > N` which means `PT > N/4` if `PT < N/2` was true, or `PT > 3*N/4` if `PT > N/2` was true in previous step

We can extend this using binary search approach to get upper and lower bounds of the flag in relation to `n`.
Fortunately we've got LSB oracle implemented in our [crypto-commons](https://github.com/p4-team/crypto-commons)

Since we don't want to waste time running the code against the server, until we're sure it works, we can make a simple sanity test to verify if our approach works:

```python
def sanity_test():
    import gmpy2
    import random
    from crypto_commons.generic import bytes_to_long, long_to_bytes
    from crypto_commons.oracle.lsb_oracle import lsb_oracle
    from crypto_commons.rsa.rsa_commons import modinv

    def server_oracle(c):
        dice = pow(c, d, n) & 1
        result = ""
        for rounds in range(100):
            p = ['\1', '\2'][dice & 1]
            k = random.randint(0, 2)
            c = (ord(p) + k) % 2
            result += chr(c)
        return result

    def test_oracle(c):
        while True:
            response = server_oracle(c)
            bit = check_bit(response)
            if bit != -1:
                return bit

    p = gmpy2.next_prime(2 ** 512)
    q = gmpy2.next_prime(p)
    n = p * q
    e = 65537
    d = modinv(e, (p - 1) * (q - 1))
    flag = "CTF{ala ma kota a sierotka ma rysia}"

    long_flag = bytes_to_long(flag)
    ct = pow(long_flag, e, n)
    multiply_plaintext_by_2 = lambda c: (c * pow(2, e, n)) % n
    result = lsb_oracle(ct, multiply_plaintext_by_2, n, lambda c: test_oracle(c))
    print(long_to_bytes(result))


sanity_test()
```

In this test we generate some RSA private and public keys, encrypt a random flag and then respond in the same manner as the server.
If we run this we instantly get the right flag, which means it works fine.

Now we can run the real code:

```python
from Crypto.PublicKey import RSA

from crypto_commons.generic import bytes_to_long, long_to_bytes
from crypto_commons.netcat.netcat_commons import nc
from crypto_commons.oracle.lsb_oracle import lsb_oracle


def check_bit(data):
    one = 0
    zero = 0
    for result in data:
        if result == '\1':
            one += 1
        else:
            zero += 1
    print("diff", abs(zero - one))
    if one - zero > 10:
        return 0
    elif zero - one > 10:
        return 1
    else:
        print("not sure for " + str(zero) + " " + str(one))
        return -1


def oracle(payload):
    data = ""
    while True:
        try:
            url = "perfect-secrecy.ctfcompetition.com"
            port = 1337
            s = nc(url, port)
            s.settimeout(5)
            bytes_payload = long_to_bytes(payload).zfill(128)
            s.sendall("\1\2" + bytes_payload)
            data = ""
            for i in range(100):
                data += s.recv(1)
            try:
                s.close()
            except:
                pass
            print(len(data), data)
            if len(data) == 100:
                bit = check_bit(data)
                if bit != -1:
                    return bit
        except Exception as e:
            print('retry ' + str(e) + " data received=" + data + " payload=" + str(payload))
            pass


def main():
    import codecs
    with codecs.open("key_pub.pem", "r") as key_file:
        with codecs.open("flag.txt", "rb") as flag_file:
            flag_data = bytes_to_long(flag_file.read())
            data = key_file.read()
            key = RSA.importKey(data)
            n = key.n
            e = key.e
            multiply_plaintext_by_2 = lambda c: (c * pow(2, e, n)) % n
            result = lsb_oracle(flag_data, multiply_plaintext_by_2, n, oracle)
            print(long_to_bytes(result))

main()
```

The main code is the same as in the sanity test really - we get the encrypted flag and public key, and we pass arguments to the lsb oracle code.
The only new function here is the `oracle` function, which simply connects to the server, and sends payload.
It has some simple fallback mechanisms to handle disconnects and timeouts.

Once we run this code after some time we can finally recover: `CTF{h3ll0__17_5_m3_1_w45_w0nd3r1n6_1f_4f73r_4ll_7h353_y34r5_y0u_d_l1k3_70_m337}`
