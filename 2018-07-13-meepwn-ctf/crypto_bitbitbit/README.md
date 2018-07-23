# BitBitBit (crypto, 8 solved, 860p)

In the task we get the [server code](server.py).
What happens is we get RSA-encrypted flag from the server, along with the public key and some parameters based on the private key primes.
The inteded solution was to analyse the key generation algorithm and recover the private key.
But we figured that there is an easier way to solve the problem.

Look at the code:

```python
from flag import FLAG

N, delta, gamma = gen_key()
m = int(FLAG.encode('hex'), 16)
c = powmod(m, 0x10001, N)
```

If we look at the challenge again we can see that the challenge with every connection gives us public key and encrypted flag.
Public key exponent is always the same 65537, and the modulus changes every time.
Apart from large `e`, this is pretty much a textbook setup for Hastad Broadcast Attack.
The flag doesn't seem to get padded in the code, and it's unlikely to be super long, so maybe we don't even need all 65537 values to recover the flag.
There is a PoW to solve when we connect to the server, so it took a while to grab all the necessary data, but once it's done we can proceed to calculate Chinese Remainder Theorem.

We even did a parallel solver for that: https://github.com/p4-team/crypto-commons/blob/master/crypto_commons/rsa/crt.py since the calculations can be easily separated into map-reduce steps.

Initially we were hoping for a flag around 32 bytes long, so only 10k messages would be enough, but it turned out we needed to get 20k because the flag was: `MeePwnCTF{It_is_the_time_to_move_to_Post_Quantum_Cryptography_DAGS}`
