# UFF (crypto, 100+25p, 12 solved)

In the challenge we get [source code](vuln.c) of the application running on the server.

The application lets us sign messages via Ed25519.
The code is quite simple:

- It shows us 10 different ECC public keys
- We can then 1000 times sign a unique message of our choosing using selected key
- We select the key by providing the whole key, not by choosing some index
- After that we are supposed to provide a signature for a message different from all messages signed via server in this session

The signature and verification code itself is correct, and there are strict checks on the input lengths.

The vulnerability comes from 2 places:

```c
unsigned find(unsigned char const *pk)
{
    unsigned idx;
    for (idx = 0; idx < K; ++idx)
        if (!strncmp(pk, keys[idx].pk, 32))
            break;
    return idx;
}
```

The issue here is `strncmp`.
Public keys are binary random data, so there is a high chance of nullbytes.
Comparing with `strncmp` stops at nullbyte so we can actually fool this function for such keys.
We can send any data after the `00` byte in the key and the function would still `find` the key.

Second piece of the puzzle is here:

```c
printf("public key> "); fflush(stdout);
if (sizeof(pk) != read_hex(pk, sizeof(pk)) || K == (idx = find(pk)))
    break;
//
print_hex(m, sign(m, n, keys[idx].sk, pk));
```

So the signature is generated using the key we provided, not the `real` key from the array.

This means we can generate a signature with `invalid` public key, and it brings to mind `fault injection` class of attack.

Let's see how exactly the signature is done:

```python
def signature(m, sk, pk):
    h = H(sk)
    a = 2 ** (b - 2) + sum(2 ** i * bit(h, i) for i in range(3, b - 2))
    r = Hint(''.join([h[i] for i in range(b / 8, b / 4)]) + m)
    R = scalarmult(B, r)
    S = (r + Hint(encodepoint(R) + pk + m) * a) % l
    return encodepoint(R) + encodeint(S)
```

This means that if we know `m` and `pk` then the only missing part is `a`.
This is because the value of `r` can by any random value, not necessarily generated as here.
This is only certain security precaution, but makes no difference for us.
And the only other parameter of the signature derived from `sk` is `a`.

If we can recover `a` we can forge a signature simply by:

```python
def forge_signature(m, pk, a):
    from ed import encodepoint, Hint, scalarmult, encodeint, B, l
    r = 42  # why not? ;)
    R = scalarmult(B, r)
    S = (r + Hint(encodepoint(R) + pk + m) * a) % l
    return encodepoint(R) + encodeint(S)
```

If we create a signatures with two different public keys and the same private key for the same message then:

```
S1 = (r + h1 * a) mod L
S2 = (r + h2 * a) mod L
S1 - S2 = a(h1-h2) mod L
a = (S1 - S2) * modinv(h1 - h2, L)
```

We can then easily recover `a` and forge a new signature:

```python
def recover(pk1, sig1, pk2, sig2, message1, message2):
    from ed import decodepoint, decodeint, encodepoint, Hint, b, l
    R1 = decodepoint(sig1[0:b / 8])
    S1 = decodeint(sig1[b / 8:b / 4])
    h1 = Hint(encodepoint(R1) + pk1 + message1)

    R2 = decodepoint(sig2[0:b / 8])
    S2 = decodeint(sig2[b / 8:b / 4])
    h2 = Hint(encodepoint(R2) + pk2 + message1)

    a = (S1 - S2) * modinv(h1 - h2, l)
    print('a', a)
    forged_signature = forge_signature(message2, pk1, a)
    checkvalid(forged_signature, message2, pk1)
    return (forged_signature + message2).encode("hex")
```

We use this approach and get the flag: `hxp{Th3_m0sT_f00lpr00f_sYsT3m_br34kz_1f_y0u_4bU5e_1t_h4rD_eN0u9h}`
