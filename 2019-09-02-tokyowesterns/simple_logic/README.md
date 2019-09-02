# Simple logic (crypto, 95p, 167 solved)

In the challenge we get [source code](encrypt.rb) and some plaintext-ciphertext pairs plus encrypted flag [outputs](output).
Encryption ported to python is:

```python
def encrypt(msg, key, bits=BITS):
    enc = msg
    mask = (1 << bits) - 1
    for i in range(ROUNDS):
        enc = (enc + key) & mask
        enc = enc ^ key
    return enc
```

This could have been solved in 2 ways.
The lazy way was to put this directly into Z3 and wait a while for it to recover the key using the known pt-ct pairs:

```python
def solvez3():
    s = Solver()
    pt = [0x29abc13947b5373b86a1dc1d423807a,
          0xeeb83b72d3336a80a853bf9c61d6f254,
          0x7a0e5ffc7208f978b81475201fbeb3a0,
          0xc464714f5cdce458f32608f8b5e2002e,
          0xf944aaccf6779a65e8ba74795da3c41d,
          0x552682756304d662fa18e624b09b2ac5]
    ct = [0xb36b6b62a7e685bd1158744662c5d04a,
          0x614d86b5b6653cdc8f33368c41e99254,
          0x292a7ff7f12b4e21db00e593246be5a0,
          0x64f930da37d494c634fa22a609342ffe,
          0xaa3825e62d053fb0eb8e7e2621dabfe7,
          0xf2ffdf4beb933681844c70190ecf60bf]
    key = BitVec('key', 128)
    for msg, result in zip(pt, ct):
        s.add(encrypt(msg, key) == result)
    print(s.check())
    model = s.model()
    return model[key].as_long()
```

But this takes quite some time, so in the meantime we can just solve this directly.
The key thing to notice here is that suffix of the encryption result depends only on the suffix of the key, and that we have `odd` number of rounds.

Let's assume the key is only 1 bit long. 
In such case `^` will cause the last bit of the encryption result to flip each round.
Of course `+` will have exactly the same result on the last bit, so they will cancel each other -> that's not very interesting.
But `+` causes as well overflow into the higher bit if we're adding `1`.
So it will flip the second bit each round, assuming there was overflow, and we have `odd number of rounds`.

Last bit is preserved by this encryption (as mentioned above `^` cancels `+` on the last bit).
Now if we look at the next bit in the plaintext and in the ciphertext we can clearly see if it flipped or not, and this tells us if the last key bit was 0 (no flip) or 1 (flip present).

If we try to expand this idea further it becomes a bit cumbersome to track all previous carries, but we don't need to do that by hand.
We can simply use the encrypt method assuming another key bit is 0 or 1 and just compare the results from ct-pt pairs we have, to determine which key bit value was the correct one.
In each round we encrypt the plaintext data using suffix of the key extended with 0 and then with 1, extract the next bit and compare it with corresponding bit in real cipheretxts.
So for recovery of 1st bit we encrypt all plaintexts with keys `0b0` and `0b1` and check in which case second LSB is the same as in result cipheretxts we have.
Then we do the same, but we use 1 bit long key, first bit is the real one we recovered above, and next bit is `0` and then `1` and we repeat the whole process.


```python
    known_key_suffix = 0b0
    for recover_bit in range(127):
        result_test_bit = [bin(result)[-2 - recover_bit] for result in ct]
        for candidate_prefix in range(2):
            candidate_key_suffix = known_key_suffix + (candidate_prefix << recover_bit)
            calculated_test_bit = [bin(encrypt(plain, candidate_key_suffix, recover_bit + 2))[-2 - recover_bit] for plain in pt]
            if result_test_bit == calculated_test_bit:
                known_key_suffix = int(bin(candidate_key_suffix)[-(recover_bit + 1):], 2)
                break
```

And almost immediately we get back the key `62900030173734087782946667685685220617` which we can now use to decrypt the flag `TWCTF{ade4850ad48b8d21fa7dae86b842466d}`
