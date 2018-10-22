# Lost modulus (crypto, 230p, 42 solved)

In the task we can connect to a service running [python code](paillier_hitcon.py).
We can easily deduce that it's a textbook implementation of Paillier cryptosystem.
We get encrypted flag from the server and then we can perform two operations:

- encryption of selected payload
- decryption of selected payload, but only least significant byte is returned

We can perform 2048 operations in total.
The twist here is that we don't know the public key.

## Recover public key modulus

This is the key part here.
Once we have the modulus, we can easily recover the flag using homomorphic properties of the encryption.

In order to recover the modulus we exploit the encryption-decryption oracle.
If we encrypt a number bigger than `n` and then decrypt it back, the number will be cut by `mod n`.
This way we know the number was too big, and `n` is smaller.
We can use this property to recover all bits of the modulus, but it would cost us exactly 2048 operations, leaving no requests for flag recovery.
But we know the whole least significant byte, so we recover all upper bits of `n` bit by bit, and then recover last byte of `n` at once, leaving us with 14 operations to work on the flag.

The recovery operations is quite simple.
First we recover the highest set bit in modulus.
We encrypt-decrypt `2**1024` and check if the last decrypted byte is still `00`, if not then we send `2**1023` and check again, and so on:

```python
    for bit in range(bitsize - 1, -1, -1):
        payload = 2 ** bit
        e = enc(long_to_bytes(payload)).decode("hex")
        result = dec(e)
        if result == '00':
            start_bit = bit
            break
```

Once we know the highest set bit we can proceed to recover rest of the bits.
We set next highest bit to 1 and perform encrypt-decrypt operation.
If last byte is still `00` then our value was smaller than `n`, and therefore this bit in modulus has to be set.
If last byte is not `00` then the number was bigger than `n` already, and therefore this bit in modulus has to be `0`, and we flip it back.
We move downwards to the next bits recovering their real value:

```python
    payload = 2 ** start_bit  # 100000...
    for bit in range(start_bit - 1, 7, -1):
        payload ^= 2 ** bit
        print(bin(payload))
        e = enc(long_to_bytes(payload)).decode("hex")
        result = dec(e)
        if result != '00':  # didn't work, set the bit back to 0
            payload ^= 2 ** bit
```

After this we have `payload` which is equal to `n` up to the last byte.
Recovering the last byte requires one more encrypt-decrypt operation.
We send the `payload` data with last byte set to `0xff`, which is most likely too big for `n` and result will be cut by `mod n`.
Now we simply loop over all possible values for the last byte and check for which one `payload % potential_n` gives the same remainder:

```python
    too_large = payload ^ 0xff
    e = enc(long_to_bytes(too_large)).decode("hex")
    result = int(dec(e), 16)
    for i in range(256):
        potential_n = payload ^ i
        mod = too_large % potential_n
        if mod == result:
            return potential_n
```

This way we managed to recover entire modulus, and we still have 14 operations to spare!

## Recover the flag

We can easily recover the flag byte-by-byte using homomorphic properties of Paillier cryptosystem.
We can get back the last byte simply by sending encrypted flag for decryption.
Now we want to `shift` the decrypted flag back one byte, so if our ciphertext decrypts to `alamakota` we want to somehow change the ciphertext so it will decrypt to `alamakot`.
It can be done if we first subtract the value of the last byte making the plaintext `alamakot\x00` and then if we divide the value by 256 making it `alamakot`.

Paillier cryptosystem allows for those operations via:

- `paillier_decrypt(pow(ct, multiplier, n**2)) = pt*multiplier % n`
- `paillier_decrypt(pow(ct, modinv(divisor,n), n**2)) = pt*modinv(divisor,n) % n`
- `paillier_decrypt(ct*encrypt(addend, g, n, n**2)) = (pt + addend) % n`
- `paillier_decrypt(ct*encrypt(n-subtract, g, n, n**2)) = (pt - subtract) % n`

In our case `g = n + 1` so we have all data we need:

```python
    f = ''
    divisor = modinv(2 ** 8, n)
    g = n + 1 
    for i in range(14):
        last_byte = dec(long_to_bytes(flag)).decode("hex")
        f += last_byte
        print(f[::-1])
        sub = paillier_encrypt_simple(n - bytes_to_long(last_byte), g, n)
        flag = flag * sub % (n * n)
        flag = pow(flag, divisor, n * n)
```

This way we can recover last bytes of the flag.
Sadly the flag is longer, so we need to run this a couple of times.
Since we want to shift the flag farther forward to recover more characters, we need to strip known characters:

```python
    divisor = modinv(2 ** 8, n)
    for last_byte in known_suffix[::-1]:
        sub = paillier_encrypt_simple(n - bytes_to_long(last_byte), n + 1, n)
        flag = flag * sub % (n * n)
        flag = pow(flag, divisor, n * n)
```

Which is pretty much the same opration as above.
After a couple of runs we recover whole: `hitcon{binary__search__and_least_significant_BYTE_oracle_in_paillier!!}`

Entire solver [here](paillier_solver.py)
