# A2S [355 points] (10 solves)

The challenge is to recover the key of a reduced AES variant (only 2 rounds), given only
3 ciphertext-plaintext pairs. While we are also given two bytes of the key, I only noticed
this after I've already solved the challenge. I don't see how to use these to achieve a
significant speedup with my approach, though.

The following sequence of operations is performed to encrypt a block:

```python
add_round_key(plain_state, self._key_matrices[0])
sub_bytes(plain_state)    # nonlinearity only here...
shift_rows(plain_state)
mix_columns(plain_state)
add_round_key(plain_state, self._key_matrices[1])
sub_bytes(plain_state)    # ...and here
shift_rows(plain_state)
mix_columns(plain_state)
add_round_key(plain_state, self._key_matrices[2])
```

However, `sub_bytes` is a byte-wise transformation, while `shift_rows` simply permutes
the bytes. We can therefore write it down in this order:

```python
add_round_key(plain_state, self._key_matrices[0])
shift_rows(plain_state)   # now before the sub_bytes
sub_bytes(plain_state)
mix_columns(plain_state)
add_round_key(plain_state, self._key_matrices[1])
sub_bytes(plain_state)
shift_rows(plain_state)
mix_columns(plain_state)
add_round_key(plain_state, self._key_matrices[2])
```

The `mix_columns` at the end was explicitly added by the author of the challenge. I don't
see why, as it is an affine operation, meaning:

```
mix_columns(x) = f(x) ^ c         where f linear
```

and so

```
mix_columns(S ^ K) = f(S ^ K) ^ c = f(S) ^ f(K) ^ c = mix_columns(S) ^ f(K)
```

This allows out to swap the final `mix_columns` with `add_round_key`, if we're willing
to imagine a different key expansion procedure:

```python
add_round_key(plain_state, self._key_matrices[0])
shift_rows(plain_state)
sub_bytes(plain_state)
mix_columns(plain_state)
add_round_key(plain_state, self._key_matrices[1])
sub_bytes(plain_state)
shift_rows(plain_state)
add_round_key(plain_state, f(self._key_matrices[2]))
mix_columns(plain_state)
```

At this point, we can perform differential cryptanalysis. For two given `(plaintext, ciphertext)` pairs,
we

1. Calculate the XOR of the plaintexts. 
2. This is also the XOR of the cipher states after the first `add_round_key`
3. We apply the `shift_rows` permutation to get the difference in cipher states after the first `shift_rows`.

This gives us the XOR between internal states at the beginning of this part of the cipher:

```python
sub_bytes(plain_state)
mix_columns(plain_state)
add_round_key(plain_state, self._key_matrices[1])
sub_bytes(plain_state)
```

The difference at the end can be calculated from the known ciphertexts through a similar process.

This is the part of the code that does this:

```python
def shift(st):
    mat = bytes2matrix(st)
    shift_rows(mat)
    return matrix2bytes(mat)

def unmix(st):
    mat = bytes2matrix(st)
    inv_mix_columns(mat)
    inv_shift_rows(mat)
    return matrix2bytes(mat)

pre_delta1 = shift(xor_bytes(plaintexts[0], plaintexts[1]))
pre_delta2 = shift(xor_bytes(plaintexts[0], plaintexts[2]))

post_delta1 = xor_bytes(unmix(ciphertexts[0]), unmix(ciphertexts[1]))
post_delta2 = xor_bytes(unmix(ciphertexts[0]), unmix(ciphertexts[2]))
```

Let's focus on the part of the cipher we still need to analyze.
Notice how each of these four operations are either byte-wise or column-wise:

```python
sub_bytes(plain_state)      # byte-wise
mix_columns(plain_state)    # column-wise
add_round_key(plain_state, self._key_matrices[1])  # byte-wise
sub_bytes(plain_state)      # byte-wise again
```

This means that each column of the cipher state is transformed independently.
Let's introduce the following names:

```python
# Call the state here P1, P2, P3 for each of the pt-ct pairs.
sub_bytes(plain_state)
mix_columns(plain_state)
# Call the state here Q1, Q2, Q3 for each of the pt-ct pairs.
add_round_key(plain_state, self._key_matrices[1])
# Call the state here S1, S2, S3 for each of the pt-ct pairs.
sub_bytes(plain_state)
# Call the state here C1, C2, C3 for each of the pt-ct pairs.
```

When you look at it bytewise, `(S1 ^ S2, S1 ^ S3)` has few possibilities — at each position,
about 256 out of the 65536 values are possible.

1. There are 256 possible values for `C1[i]`.
2. This determines `C2[i]` and `C3[i]` because of the known `post_delta`.
3. The inverse S-box determines the possible values for `S1[i]`, `S2[i]`, `S3[i]`.

Notice that this is also the same set of possible values of `(Q1 ^ Q2, Q1 ^ Q3)`. This allows us
to bruteforce `P1`, calculating `P2`, `P3`, `Q1` through `Q3`, and checking whether the XORs
are what we expect. The chance of a false positive for any specific attempt
is `2**-32`, so we should expect about one spurious result. And indeed, this is the result produced:

```
067c20d3
1f473b29
--------
8a151475
d441a30c
--------
d4eb9f89
34a72235
--------
a0227d5b
1e89501b
f669b656
336f0e52
--------

real    2m29.248s
user    9m52.629s
sys     0m0.020s
```

Internally, I am representing the `DeltaSet` as a bit array of `2**16` bits. After the CTF, I've also
tried storing a sorted array and either binary or linear searching, but as I estimated, the bit array
is fastest, as memory bandwidth is nowhere near saturated.

All that separates `P1` from the actual plaintext is
```python
add_round_key(plain_state, self._key_matrices[0])
shift_rows(plain_state)
```
...and so we can calculate the key in use. Thus we obtain 32 candidates for the key and check each of them.
