# Baby Pinhole (crypto)

In the task we get [ciphertext](ciphertext), [publickey](publickey), [crypto generator](generate.py) and [server code](server.py).

The encryption used here is Paillier cryptosystem.
Crypto parameters generation if flawless, there are large strong primes and unfactorizable 1024 bit modulus.
The encryption code is also correct.
We also know nothing about the plaintext, since plaintext is totally random and the flag is `TWCTF{sha1(plaintext)}`.

Let's focus the analysis on the server code.
Server does:

```python
cbits = size(n2)
mbits = size(n)
b = mbits//2

def run(fin, fout):
    alarm(1200)
    try:
        while True:
            line = fin.readline()[:4+cbits//4]
            ciphertext = int(line, 16) # Note: input is HEX
            m = decrypt(ciphertext, sk1, sk2, n, n2)
            fout.write(str((m >> b) & 1) + "\n")
            fout.flush()
    except:
        pass
```

So as indicated in the task name, the server provides us with a pinhole - we get to know the value of 512-th bit of the plaintext for ciphertext we send.

If we send the ciphertext we got, we can recover one bit, now only 1023 to go...

Paillier cryptosystem has a special property, similarly to unpadded RSA - it's homomorphic and thus it's possible to use `blinding attack`.
We can modify the ciphertext to get a predictable change of the decrypted plaintext.

Specifically:

- `paillier_decrypt(pow(ct, multiplier, n2)) = pt*multiplier`
- `paillier_decrypt(pow(ct, modinv(divisor,n), n2)) = pt*modinv(divisor,n)` which is basically modular division
- `paillier_decrypt(ct*encrypt(addend, g, n, n2)) = pt+addend`
- `paillier_decrypt(ct*encrypt(n-subtract, g, n, n2)) = pt-subtract`

It was not obvious how to recover the whole plaintext in this task.
It's simple enough to recover half of the bits once we know the other half.
To get low bits we could simply multiply the plaintext by `2` and thus shift the bits to the left, and then recovery of 512-th bit would give us in fact 511-th bit, but only assuming that `plaintex*2 < n` because otherwise the value would be cut by modulo.
So we would need to know the highest bit and subtract it from the plaintext before multiplication if it's set.

On the other hand to get high bits we could simply divide the plaintext by `2` and thus shift the bits to the right, so that the recovery of 512-th bit would in fact give us 513-th bit, but only assuming `pt % 2 == 0` because otherwise the multiplication by modinv(2,n) is not a simple division, and to make sure that `pt` is even we would need to subtract the lowest bit if it's set, but for that we would need to know the lowst bit first!

Finally we figured that we can actually recover low bits without any prior knowledge by using addition and integer overflows.

Let's assume that we have bits:

`...[0]0101...`

where the marked bit is actually the 512-th bit we can recover from the pinhole.
If we add bit `1` to the 511-th bit (so we add `1<<511`) we can get two cases:

- If the pinhole bit flipped, then there was overflow and thus bit 511 must have been `1`
- If the pinhole bit is still the same, then there was no overflow and thus bit 511 must have been `0`

In our example the bit was `0` so no overflow was observed.

Of course if we try to do this with bit 510 it won't work that easily because regardless of overflow we won't notice anything in bit 512, because it would only overflow to 511 which was 0.
But we already know that 511 is 0 so we can simply add `1<<511` and effectively set this bit to be high.
If we do this then we can again observe overflow of bit 510 directly in bit 512 pinhole.

In general: we need to set all the bits we know below 512 to be 1 and then we can always observe the overflow in bit 512.

So we proceed with a simple python code:

```python
def recover_low_bits(oracle, n, n2, g, ct):
    print('cracking low bits')
    mbits = size(n)
    bits_to_recover = mbits // 2
    result_bits = []
    initial_state = oracle.get_lsb(ct)
    for i in range(bits_to_recover):
        filling = ['0' if known_bit == '1' else '1' for known_bit in result_bits]
        add = int("".join(filling + ['1']), 2) << (bits_to_recover - i - 1)
        payload = (ct * encrypt(add, g, n, n2)) % n2
        lsb = oracle.get_lsb(payload)
        if lsb != initial_state:
            result_bits.append('1')
        else:
            result_bits.append('0')
    result = "".join(result_bits)
    return result
```

And after a while we recover the low bits.

Now that we know low bits we can use the division idea mentioned earlier.
We can now make sure that `pt % 2 == 0` because if we subtract all low bits from the pt then it will have all 512 low bits set to 0, so we can safely divide 512 times.
So we proceed by subtracting low bits and then dividing plaintext in a loop by 2 (shifting the bits right) and recovering bits 513, 514, 515...:

```python
def recover_high_bits(low, oracle, n, n2, g, ct):
    print('cracking high bits')
    mbits = size(n)
    b = mbits // 2
    result_bits = []
    subtractor = n - low
    sub = encrypt(subtractor, g, n, n2)
    ct_sub = (ct * sub) % n2
    for i in range(b):
        divisor = inverse(2 ** i, n)
        payload = pow(ct_sub, divisor, n2)
        lsb = oracle.get_lsb(payload)
        result_bits.append(str(lsb))
    return "".join(result_bits[::-1])
```

Once we recovered all bits we can glue both parth together and calculate the flag: `TWCTF{ccb71c01f350cf0bc844e87d161f84b9b479b439}`

Whole solver script [here](solver.py).
It contains also sanity check on how to use the homomorphic properties of the cipher and a local set of random tests to verify the solution concept.
