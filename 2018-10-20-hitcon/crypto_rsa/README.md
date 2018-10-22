# Lost key (crypto, 257p, 29 solved)

In the task we can connect to a service running [python code](rsa_hitcon.py).
We can easily deduce that it's a textbook implementation of RSA cryptosystem.
We get encrypted flag from the server and then we can perform two operations:

- encryption of selected payload
- decryption of selected payload, but only least significant byte is returned

Contrary to the similar Paillier task, here we can perform only 150 operations in total.
Similarly, we don't know the public key.

## Recover public key modulus

We could perform a similar trick as in Paillier task to recover modulus bit by bit, but we don't have enough operations for that.
If we knew `e` we could ask server to encrypt for us `2` and `3` to get back `2**e mod n` and `3**e mod `n and then calculate `gcd(2**e - (2**e mod n), 3**e - (3**e mod n))`.
The trick here is that if we substract `x**e - (x**e mod n)` we get a number which is a multiply of `n`, and thus `gcd(k1*n, k2*n)` most likely will give back `n` or `n` multiplied by some small factor `k`.

Here we don't know `e`, so this won't work, but we figured a very similar construction.
We can ask server to encrypt `2` and 2**2`, and also `3` and `3**2`.
Now we can square encrypted `2` to get `(2**e mod n)**2` and subtract `(2**e mod n)**2 - (2**2**e mod n)`.
This operation similarly as above, gives us some multiply of `n`.
We do the same for `3` and calculate `gcd` of those two numbers, which should result in `n` possibly multiplied by some small factor:

```python
def recover_pubkey(enc):
    two = int(enc('\x02'), 16)
    three = int(enc('\x03'), 16)
    power_two = int(enc('\x04'), 16)
    power_three = int(enc('\x09'), 16)
    n = gmpy2.gcd(two ** 2 - power_two, three ** 2 - power_three)
    while n % 2 == 0:
        n = n / 2
    while n % 3 == 0:
        n = n / 3
    return n
```

Just in case we divide the result by 2 and 3, in case those are the small factors.
We could run some simple factorization on the number to be sure it's `n` and not `k*n` but it was not necessary.

## Recover the flag

Now that we have `n` we can try to recover the flag from the server.
Sadly RSA is only homomorphic with multiplication, and not with addition, so we can't use the same trick as with Paillier.

We could run a classic Least-Significant-Bit Oracle attack here, but we lack the number of necessary operations.
It would take us 1024 queries to narrow the flag down bit by bit, especially that we know that the flag is on the small bytes part of the data.
However, we know the whole least significant byte of the decryption, not just the single bit!
It turns out we can use this byte to recover the state of 8-LSB bits which we would see if we were using the classic LSB Oracle and multiplying the plaintext by 2.
So instead we multiply by `2**8` and recover all 8 bits for this step:

```python
    x = flag
    real_x = int(dec(long_to_bytes(flag)), 16)
    multiplier = int(enc(long_to_bytes(2 ** 8)), 16)
    x = x * multiplier
    expected_value = int(dec(long_to_bytes(x)), 16)
    for configuration in itertools.product([0, 1], repeat=8):
        res = real_x % 256
        for bit in configuration:
            res = res * 2
            if bit == 1:
                res = res - n
        res = res % 256
        if res == expected_value:
            print(configuration)
            bits.extend(configuration)
            break
```

We literally brute-force all combinations of LSB Oracle bits state and check for which one of them the resulting LSB byte is the same as what we got from the server.
We run this in a loop for each character to recover entire flag: `hitcon{1east_4ign1f1cant_BYTE_0racle_is_m0re_pow3rfu1!}`

Whole solver [here](rsa_solver.py)
