# Bad Computations (Crypto, 800p)

In the task we get [crypto code](crypt.py) and encrypted flag: `hnd/goJ/e4h1foWDhYOFiIZ+f3l1e4R5iI+Gin+FhA==`

We proceed with labelling the poorly obfuscated functions.
It's quite clear we have there something like: `primes_in_range`, `prime_sieve`, `extended_gcd` and `mod_inv`.
Next we proceed to label the flag encryption procedure and it's easy to notice that it's Paillier Cryptosystem.
So once we label the code we end up with:

```python
flag_bytes = [ord(x) for x in flag]
paillier_encrypted_constant = paillier_encrypt(b, g, n, r)

for i in range(len(flag_bytes)):
	flag_bytes[i] = (paillier_encrypt(flag_bytes[i], g, n, r) * paillier_encrypted_constant) % (n * n)
	flag_bytes[i] = paillier_decrypt(flag_bytes[i], [p, q], g)

flag_bytes = b64encode(bytearray(flag_bytes))
print(str(flag_bytes)[2:-1])
```

So in reality encrypted flag byte is multiplied by encrypted constant and later decrypted.
But Paillier has homomorphic properties.
We can calculate `encrypt(plaintext1 * plaintext2)` by doing `encrypt(plaintex1)^plaintext2 mod n^2` and we can calculate `encrypt(plaintext1 + plaintext2)` by doing `encrypt(plaintex1) * encrypt(plaintex2)`.
Here we have the second option, so in reality the encryption code is just doing:

`decrypt(encrypt(flag[i]) * encrypt(22)) = decrypt(encrypt(flag[i]+22)) = flag[i] + 22`

So we can simply run:
```python
print("".join([chr(ord(c) - 22) for c in 'hnd/goJ/e4h1foWDhYOFiIZ+f3l1e4R5iI+Gin+FhA=='.decode("base64")]))
```

to get the flag: `paillier_homomorphic_encryption`

I fail to see how this is worth 800p.
