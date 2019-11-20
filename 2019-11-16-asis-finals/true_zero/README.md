# True zero (RE, 477p, 2 solved)

In this challenge we get a [binary](truezero) and [encrypted flag](flag.enc).

After reversing the binary, we can see that the input is a PNG file, and that the encryption is doing basically:

```python
def encrypt(flag, key, rounds_number):
    for i in range(rounds_number):
        flag = xor(flag, key)
        flagbin = "".join("{:08b}".format(ord(c)) for c in flag)
        flag = "\x01" + xor(flagbin[1:], flagbin[:-1])
        flag = xor(flag, "0" * len(flag))
        flag = "".join(chr(int(flag[i:i + 8], 2)) for i in range(0, len(flag), 8))
    return flag
```

So it's xoring the `flag` bytes with `key`, then xors this with flag shifted by 1 bit, repeats this for many rounds, and at the end puts `1` at the highest bit.
Number of rounds is unknown, up to 1337.
Key has unknown length, but it's repeated many times to match the plaintext.

First observation we can make is about the encrypted file itself.
At one point of the file we have a long repeating pattern of bytes.
Once we compared this with the flag PNG from `helix` challenge, we noticed that at pretty much the same offsets the file has palette definition, which in that case was all `0`.

Our assumption is that also in this case, those pattern bytes are basically encrypted zeros.
Since this part has only `0` as flag, it means it contains only the `key` part.
We can use this, to unxor the `key` from the encrypted flag.

See sanity test:

```python
def sanity2():
    flag = os.urandom(512)
    key = os.urandom(16)
    while len(key) < len(flag):
        key += key
    flag_stream = encrypt(flag, '\0' * 512)
    zero_stream = encrypt('\0' * 512, '\0' * 512)
    keystream = encrypt('\0' * 512, key)
    enc_flag = encrypt(flag, key)
    assert xor(xor(flag_stream, zero_stream), keystream) == enc_flag
```

This means that if we xor `enc_flag` with `keystream` (which is pretty much `0` encrypted with the key), we can get back `xor(flag_stream, zero_stream)`.
And `zero_stream` is simply `0` encrypted with `0` key, so we can create this as well, and recover the `flag_stream`, which is flag encrypted with `0` key.

Now our approach is:

1. Use the encrypted palette as `keystream`
2. Unxor key from the encrypted flag to get back flag_stream
3. Encrypt "forward" part of the plaintext and compare with ciphertext we have, byt brute-force. Encrypt `zeros+'a', zeros+'b', ...` and check which one matches the ciphertext we have.

Since we don't really know the plaintext prefix (apart from the PNG header), we can't really encrypt part of the file at this point.
But remember that we have the long `0` palette!
We can therefore encrypt something right `behind` the palette, since we know lots of bytes before that.
It's enough if the part we know has more bits than the number of rounds, because we can safely shift this part during encrypt.

We still don't know how many rounds there were, but we know that if the palette is all `0`, we can predict the CRC value which is right behind that.
Also, if we're right that the PNG looks a lot like the one from `helix`, then there should be very particular `transparency` definition in the file, and 256 bytes further `IDAT` chunk.

We can, therefore, test every possible number of rounds, brute-forcing only a handful of bytes, just to see if the right CRC is there and if `tRNS` is there:


```python
def encrypt_fast(flag, flag_len, rounds_number):
    flagi = bytes_to_long(flag)
    for i in range(rounds_number):
        flagi = flagi ^ (flagi >> 1)
    one = (1 << (8 * flag_len - 1))
    return long_to_bytes(flagi | one)

def worker(data):
    known, byte, length, flag_stream, round_number = data
    payload = known + chr(byte)
    flag_stream_prefix = encrypt_fast(payload, length + 1, round_number)[256:]
    if flag_stream.startswith(flag_stream_prefix):
        return byte


def solve(rounds, condition, bytes_to_recover):
    offset = 0x329  # palette
    start = offset
    flag_enc = open("flag.enc", 'rb').read()[start:]
    flag_len = start + len(flag_enc)
    keystream = "B2 70 90 79 15 96 AB 15 35 44 04 AB C9 8B E0 B3 D8 81 66 CB BD 6E 2E 86 36 24 4A F3 85 96 10 7B D8 01 21 5E 24 32 F7 2F".replace(" ", "")
    keystream = keystream.decode("hex") * 1000
    keystream = keystream[start - 256:]
    for round_number in rounds:
        print('testing', round_number)
        zero_stream = encrypt_fast('\0' * flag_len, flag_len, round_number)[start:]
        flag_stream = xor(xor(keystream, flag_enc), zero_stream)
        flag_s = flag_stream
        known = '\0' * offset
        full_result = known
        working_len = 256  # more than enough, 1337 rounds need 167 bytes
        length = len(known[start - working_len:])
        known = known[start - working_len:]
        for index in range(bytes_to_recover):
            results = brute(worker, [(known, i, length, flag_s, round_number) for i in range(256)], processes=6)
            results = [k for k in results if k is not None]
            if len(results) > 1:
                print(results)
                break
            known = known + chr(results[0])
            known = known[1:]
            flag_s = flag_s[1:]
            full_result += chr(results[0])
            if condition(full_result):
                print('match for', round_number)
                break


if __name__ == '__main__':
    freeze_support()
    solve(range(1,1338), lambda x: "tRNS" in x, 64)
```

From this we know that it matched for rounds `116+k*128`.
For those rounds we now extend the search 256 bytes further to look for `IDAT`, and we find that `IDAT` was found for `244` rounds -> `solve([116 + k*128 for k in range(10)], lambda x: "IDAT" in x, 64+260)`.

Now we can finally recover the real plaintext (except for the part before palette), using the same code, just this time going all the way to the end, with no stop conditions.
It takes a while, but eventually we get back [the file](out.bin).

Now what's left is to recover the actual PNG, eg. by decopressing the IDAT, guessing the sizes and displaying the raw pixels.
Eventually we get:

![](flag.png)
