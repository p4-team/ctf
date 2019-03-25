# Baby RSA (crypto, 74p, 137 solved)


In the challenge we get [code](rsa.sage), the [public key](pubkey.py) and the [result](flag.enc).

Encryption is rather simple:

```python
R.<a> = GF(2^2049)

def encrypt(m):
    global n
    assert len(m) <= 256
    m_int = Integer(m.encode('hex'), 16)
    m_poly = P(R.fetch_int(m_int))
    c_poly = pow(m_poly, e, n)
    c_int = R(c_poly).integer_representation()
    c = format(c_int, '0256x').decode('hex')
    return c
```

It seems the `n` here is a polynomial in PolynomialRing over GF(2).
The encryption basically changes the message into element of GF(2^2049) and then represent this as element of the ring P, then raises this polynomial representation of the message to the power of `e` mod polynomial `n`.

So it really boils down to the classic RSA, with the small twist that `m` and `n` are now polynomials and everything is calcualted in PolynomialRing over GF(2).

We found a very good paper describing this idea: http://www.diva-portal.se/smash/get/diva2:823505/FULLTEXT01.pdf (BSc thesis of Izabela Beatrice Gafitoiu).

If we follow this thesis we will find that in this setting the `d` decryption exponent can be calculated as modular multiplicative inverse of `e` mod `s`.
The special value `s` is the equivalent of `phi` from classic RSA, and is basically `(2^p_d-1)(2^q_d-1)` where `p_d` and `q_d` are degrees of polynomials `p` and `q` such that `p*q == n`.

So the idea is pretty simple:

1. Factor polynomial `n` into `p` and `q`
2. Calculate `s`
3. Calculate `d`
4. Decrypt the flag

```python
def decrypt(m, d):
    m_int = Integer(m.encode('hex'), 16)
    m_poly = P(R.fetch_int(m_int))
    c_poly = pow(m_poly, d, n)
    c_int = R(c_poly).integer_representation()
    c = format(c_int, '0256x').decode('hex')
    return c

if __name__ == '__main__':
    p,q = n.factor()
    p,q = p[0],q[0]
    s = (2^p.degree()-1)*(2^q.degree()-1)
    d = inverse_mod(e,s)
    with open('flag.enc', 'rb') as f:
        ctext = f.read()
        print(decrypt(ctext,d))
```

And we get `flag{P1ea5e_k33p_N_as_A_inTegeR~~~~~~}`
