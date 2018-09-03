# Mixed cipher (crypto, 233p, 39 solved)

In the challenge we get the [server source code](mixed_server.py)
The server gives us 4 options to choose from:

1. `encrypt` simply encrypts data we provide with AES-CBC (with random IV each time) and with RSA and we get back the ciphertexts.
2. `decrypt` performs RSA-decryption of the payload, and returns only the last byte of the result to us.
3. `get encrypted flag` returns AES-CBC encrypted flag to us, but with IV removed.
4. `get encrypted key` returns RSA encrypted AES key.

So in order to get the flag we need:
- Get the AES encrypted flag from the server
- Recover the missing IV for the flag
- Get encrypted AES key and RSA-decrypt it
- Use AES to decrypt the flag

## Recovering AES key by breaking RSA via LSB-oracle

Let's start with recovering AES key from the server.
We can grab RSA-encrypted version from the server right away.
The setup here is pretty straightforward - the server can decrypt the payload we provide, and return last byte of the plaintext.
In reality we only need the last bit to apply the RSA Least-Significant-Bit-Oracle attack, we described multiple times already in previous writeups.
In short, we can multiply the plaintext many times by `2` (by multiplying ciphertext by `pow(2,e,n)`) and check if the value overflows the modulus (in such case last bit is `1`), and use binary search to calculate upper and lower bounds for the plaintext. 
We have a ready solution in crypto-commons for this.

In order to run this, we need to be able to multiply the plaintext by 2, and this means we need to know the value `n`.
Theoretically we could simply ask the server to give us encrypted value of `2` and then multiply ciphertext with this, but without applying `mod n` to the result, the final value will be bigger than `n`, and the server refused to decrypt such value.

So we need to recover `n` first.

### Recovering RSA modulus

If we ask the server for encrypted value of `2` we get back a number `c1` such that `c1 = 2^e mod n`.
This means that `2^e - c1 = k1*n` for some value `k1`.
We can get another value `c2` from the server, this time for example for `3`, and this way we can get `3^e - c2 = k2*n` for some other `k2`.

Now if we calculate GCD of those 2 numbers we will most likely get back `n`, maybe multiplied by some small factor.
We can provide more inputs and calculate gcd on more values, or we can try to factor the result, to get rid of small factors.
Either way we get back `n`.
We can also verify that `e` on the server is equal to `65537`, because we can encrypt `2` via the server, and calculate `pow(2,e,n)` locally.

```python
def recover_n(s):
    send(s, '1')
    print(receive_until_match(s, "input plain text: "))
    send(s, '\2')
    r = receive_until_match(s, "4: get encrypted key\n")
    print(r)
    pow2e = int(re.findall('RSA: (.*)\n', r)[0], 16)
    send(s, '1')
    print(receive_until_match(s, "input plain text: "))
    send(s, '\3')
    r = receive_until_match(s, "4: get encrypted key\n")
    print(r)
    pow3e = int(re.findall('RSA: (.*)\n', r)[0], 16)
    n = gmpy2.gcd(2 ** 65537 - pow2e, 3 ** 65537 - pow3e)
    n = factor(n)[1]
    assert pow(2, 65537, n) == pow2e
    return n
```

### Size optimization

A small tweak we can apply here is to notice that the AES key is only 128 bits long, and no padding is added.
Modulus is 1024 bits long, and therefore first 895 multiplications by 2 can't possibly cause the plaintext value to overflow `n`.
So we can actually start from this point, instead from 0.

### LSB Oracle

```python
from crypto_commons.oracle.lsb_oracle import lsb_oracle_from_bits

def recover_aes_key(n, s):
    send(s, '4')
    r = receive_until_match(s, "here is encrypted key :\)\n.+\n")
    encrypted_aes_key = re.findall("here is encrypted key :\)\n(.*)\n", r)[0]
    print('aes key', encrypted_aes_key)
    decrypted_aes_key = lsb_oracle(int(encrypted_aes_key, 16), lambda ct: ct * pow(2, 65537, n) % n, n, lambda ct: oracle(s, ct))
    return long_to_bytes(int(decrypted_aes_key))


def oracle(s, ct):
    send(s, '2')
    print(receive_until_match(s, 'input hexencoded cipher text: '))
    payload = long_to_bytes(ct).encode("hex")
    print("Sending payload", payload)
    send(s, payload)
    r = receive_until_match(s, 'RSA: .*\n')
    receive_until_match(s, '4: get encrypted key\n')
    bit = int(re.findall('RSA: (.*)\n', r)[0], 16) & 1
    return bit


def lsb_oracle(encrypted_data, multiplicator, upper_bound, oracle_fun):
    def bits_provider():
        ciphertext = encrypted_data
        for i in range(895):  # 1024 - 128 = 896
            ciphertext = multiplicator(ciphertext)
            yield 0
        while True:
            ciphertext = multiplicator(ciphertext)
            yield oracle_fun(ciphertext)

    return lsb_oracle_from_bits(upper_bound, bits_provider())
```

## Recovering IV

Now we could decrypt the flag already, but the first block of the flag would be messed-up, because we don't know the proper IV.
If we look at the code, how IV is generated during encryption we can see:

```python
def aes_encrypt(s):
    iv = long_to_bytes(random.getrandbits(BLOCK_SIZE * 8), 16)
    aes = AES.new(aeskey, AES.MODE_CBC, iv)
    return iv + aes.encrypt(pad(s))
```

So the IV is random, but it's using python standard MT random generator.
This generator has less than 20000 bits of internal state, so if we can get 20000 consecutive bits from the generator, we can replicate the internal state and create a new generator which would yield identical results.

And we can do that, since we can simply encrypt random messages and grab IV server will send back.
For final recovery we used the code from https://github.com/eboda/mersenne-twister-recover/blob/master/MTRecover.py

```python
def get_iv(s):
    send(s, '1')
    print(receive_until_match(s, "input plain text: "))
    send(s, 'A')
    r = receive_until_match(s, "4: get encrypted key\n")
    print(r)
    aes_iv = re.findall('AES: (.*)\n', r)[0][:32].decode("hex")
    return aes_iv


def collect_outputs(s):
    out = []
    for i in range(160):
        aes_iv = get_iv(s)
        out.extend(map(bytes_to_long, chunk(aes_iv, 4))[::-1])
    return out


def recover_next_iv(s):
    outputs = collect_outputs(s)
    mtr = MT19937Recover()
    r2 = mtr.go(outputs)
    iv = long_to_bytes(r2.getrandbits(16 * 8))
    sanity = get_iv(s)
    assert sanity == iv
    return long_to_bytes(r2.getrandbits(16 * 8)).encode("hex")
```

Keep in mind that the recovery script we use expects to get at least 624 32-bit values from the generator.
We get them from server as a single 128 bit block, but this means the order is shifted!
This is why we need to do:

```
chunk(aes_iv, 4))[::-1]
```

So we split the IV into 4-byte blocks, invert the order, and then convert those 4-byte blocks into 32-bit values.

## Get flag

Now we can predict the next IV value, so we can grab encrypted flag from the server, attach the predicted IV, and decrypt it.
Once we do that we get back: `TWCTF{L#B_de#r#pti#n_ora#le_c9630b129769330c9498858830f306d9}`

Full recovery script [here](mixed.py)
