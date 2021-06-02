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

However, `sub_bytes` is a byte-wise transformation, while `shift_rows` simply performs
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
mix_columns(S ^ K) = mix_columns(S) ^ f(K)
```

(what `f` is exactly is not relevant to the solution, but it is the linear part of the
affine transformation)

This allows out to swap the final `mix_columns` with `add_round_key`, if we're willing
to imagine a different key expansion procedure.

Long story short, we can calculate the XOR between internal states at the beginning and
end of this part of the cipher:

```python
sub_bytes(plain_state)
mix_columns(plain_state)
add_round_key(plain_state, self._key_matrices[1])
sub_bytes(plain_state)
```

Namely, the following code does the trick:

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

Notice how each of these four operations are either byte-wise or column-wise:

```python
sub_bytes(plain_state)      # byte-wise
mix_columns(plain_state)    # column-wise
add_round_key(plain_state, self._key_matrices[1])  # byte-wise
sub_bytes(plain_state)      # byte-wise again
```

We will therefore consider this as four independent transformations of each of the 32-bit columns.
Let's look at the state at this moment:

```python
# Call the state here P1, P2, P3 for each of the pt-ct pairs.
sub_bytes(plain_state)
mix_columns(plain_state)
add_round_key(plain_state, self._key_matrices[1])
# Call the state here S1, S2, S3 for each of the pt-ct pairs.
sub_bytes(plain_state)
# Call the state here C1, C2, C3 for each of the pt-ct pairs.
```

When you look at it bytewise, `(S1 ^ S2, S1 ^ S3)` has very little possibilities.

1. There are 256 possible values for `C1[i]`.
2. This determines `C2[i]` and `C3[i]` because of the known `post_delta`.
3. The inverse S-box determines the possible values for `S1[i]`, `S2[i]`, `S3[i]`.

```rust
fn expected_deltas(d1: u8, d2: u8) -> DeltaSet {
    let mut deltas = DeltaSet(BitArray::zeroed());
    for a in 0..=255 {
        let p = INV_SBOX[a as usize] ^ INV_SBOX[(a ^ d1) as usize];
        let q = INV_SBOX[a as usize] ^ INV_SBOX[(a ^ d2) as usize];
        deltas.add([p, q]);
    }
    deltas
}

// ...
    let expected: [DeltaSet; 4] = array_init(|i| expected_deltas(post_delta1[i], post_delta2[i]));
```

The reason why we're interested in the deltas is that `add_round_key` won't change them. Now we just
bruteforce the input P1, determine P2 and P3, calculate `sub_bytes` and `mix_columns`, and check
whether the differences match what we expect. The chance of a false positive for any specific attempt
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

All that's left to do is try out the 32 candidates, compute the corresponding key for each, and see if
the ciphertexts match. Calculating said key essentially amounts to a single XOR.
