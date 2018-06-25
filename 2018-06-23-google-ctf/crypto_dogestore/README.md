# Dogestore (crypto, 267p, 27 sovled)

In the task we get [server code](fragment.rs), [encrypted flag](encrypted_secret) and endpoint to connect to.
What the code does is pretty simple, even if you don't know Rust:

1. Read input bytes from user.
2. Decrypt the data using AES-CTR.
3. Deserialize the data by matching neighbouring bytes together in pairs, so for example [1,2,3,4,5,6] becomes [(1,2),(3,4),(5,6)].
4. Decode the data by treating the first byte in the pair as letter and second byte as number of repetitions of this letter to which 1 is added, thus for example pair ('A',3) becomes 'AAAA', then all those bytes are connected into a single vector.
5. Calculate sha3_256 hash over the resulting bytes.
6. Send calculated hash value to the user.

The main vulnerability here is quite obvious and simple to notice:
```
    iv = get_iv();
    openssl::symm::decrypt(
        openssl::symm::Cipher::aes_256_ctr(),
        &key,
        Some(&iv),
        data
    )
```

AES in CTR mode does not use IV, but a counter instead.
Counter should not be repeating in predictable manner, and in no circumstances should be constant, like in our code.
This is because AES-CTR is a stream cipher, which generates keystream by AES encryption using provided key and counter values.
For given key and counter, it will generate exactly the same keystream every time.
Therefore in reality, what we have here is simply XOR of the data we send, with some constant keystream.

This means, that in order to decrypt the flag we basically need to leak this keystream from the server.
Initially we though that `res.extend(vec![letter; size as usize + 1].iter())` is vulnerable, because if `size` would be `255` and it's `uint8` then `size+1` would overflow to `0`, but unfortunately we have `size as usize` so it won't work.

After some brainstorming we figured we could try to generate hash collisions and leverage birthday attack idea.
Let's imagine we set all payload bytes to 0 and focus only on the first 4 bytes of the payload.

By setting those 4 bytes to random values we get some data `AxBy` where `A` and `B` are `letters` and `x` and `y` are counters by which those letters will be multiplied during `decode` step.
We can calculate hash of this input and save it as reference.

Now if we bitflip the counters, there is a chance that we get two new counters `v` and `z` such that `x+y == v+z`.
If we were lucky and we initially got `A == B` then such scenario will give a collision of the hashes, because the hashed string will have the same prefix `lettter * (x+y+1)` in both cases.

If we were not so lucky, we create new `AxBy` payload and try again.
It takes a while, but we can generate collisions such way.

If this collision happens then we know the decrypted `A` and `B` were identical characters, so `payload[0]^KEY[0] == payload[2]^KEY[2]`.
And we know `payload` bytes we sent, so we can transform this to `KEY[0]^KEY[2] == payload[0]^payload[2]`.

We can then shift right by 2 bytes, and calculate collision for `KEY[2]^KEY[4]` and so on.

If we can now guess the first KEY byte, we can recover all even KEY bytes.

The described algorithm is:

```python
def find(key_byte_number, get_result_fun=get_result):
    payload = [0] * 110
    attempts = 0
    while True:
        attempts += 1
        if attempts % 5 == key_byte_number % 5:
            print(key_byte_number, attempts)
        payload[key_byte_number] = 0
        payload[key_byte_number + 1] = random.randint(0, 255)
        payload[key_byte_number + 2] = random.randint(0, 255)
        payload[key_byte_number + 3] = random.randint(0, 255)
        res = get_result_fun(payload)
        for i in range(4):
            pay2 = payload[:]
            pay2[key_byte_number + 1] ^= 1 << i
            pay2[key_byte_number + 3] ^= 1 << i
            r2 = get_result_fun(pay2)
            if res == r2:
                print("KEY[%d] ^ KEY[%d] = %d" % (key_byte_number, key_byte_number + 2, payload[key_byte_number + 2]))
                print(res, r2, payload, pay2)
                return payload[key_byte_number + 2]
```

As usual, we would like to test this offline in some sanity test scenario, to verify it works:

```python
def sanity_test():
    secret = "alamakotaa"

    def decrypt(data):
        return xor_string(secret, data)

    def deserialize(decrypted):
        return chunk(decrypted, 2)

    def decode(secret):
        return "".join([a * (ord(b) + 1) for a, b in secret])

    def mimick_server(data):
        import sha3
        decrypted = decrypt(data)
        secret = deserialize(decrypted)
        expanded = decode(secret)
        return sha3.sha3_256(expanded).digest()

    def fake_get_result(data):
        payload_bytes = "".join(map(chr, data))
        return base64.b64encode(mimick_server(payload_bytes))

    flag = xor_string("CTF{XXXXX}", secret)
    found = []
    for i in range(0, len(secret) - 2, 2):
        found.append(find(i, fake_get_result))
    print(found)
```

We mimick the server code in python, replacing AES with simple xor, and instantly we get all the collisions and the result: `[0, 0, 14, 14]`.
Which is true since `'a'^'a' == 0` and `'a'^'o' == 14`.

We can therefore run this code against the real server to recover the even KEY bytes, we simply need to use a different `get_result` function:
```
from crypto_commons.netcat.netcat_commons import nc, send


def get_result(payload):
    url = "dogestore.ctfcompetition.com"
    port = 1337
    while True:
        try:
            s = nc(url, port)
            payload_bytes = "".join(map(chr, payload))
            send(s, payload_bytes)
            result = s.recv(9999)
            return result
        except:
            pass
```

And after some long while we recover: `[191, 119, 132, 188, 171, 242, 33, 15, 50, 0, 32, 130, 110, 51, 57, 36, 108, 223, 132, 48, 58, 47, 190, 144, 54, 115, 250, 91, 13, 16, 25, 193, 178, 26, 115, 140, 231, 65, 99, 180, 221, 121, 92, 206, 16, 64, 152, 181, 231, 228, 136, 149, 177, 237, 0]`

Now we need to guess the first KEY character.
We can actually brute-force it locally, because half of the keystream should already recover some reasonable flag part from the payload we have.
We can therefore simply check every possible value for `KEY[0]`, fill odd bytes with `\0` and decrypt the flag:

```python
def brute_first():
    found = [191, 119, 132, 188, 171, 242, 33, 15, 50, 0, 32, 130, 110, 51, 57, 36, 108, 223, 132, 48, 58, 47, 190, 144, 54, 115, 250, 91, 13, 16, 25, 193, 178,
             26,
             115, 140, 231, 65, 99, 180, 221, 121, 92, 206, 16, 64, 152, 181, 231, 228, 136, 149, 177, 237, 0]
    with codecs.open("encrypted_secret") as flag_file:
        flag = flag_file.read()
        for first in range(256):
            real_even_keystream = [chr(first)]
            for c in found:
                real_even_keystream.append(chr(ord(real_even_keystream[-1]) ^ c))
            with_zeros = reduce(lambda x, y: x + y, map(list, zip(real_even_keystream, ['0'] * len(found))))
            xored = xor_string(flag, "".join(with_zeros))
            even_chars = "".join([xored[i] for i in range(0, len(xored), 2)])
            print(first, even_chars)

brute_first()
```

We get a nice string:
```
(174, 'HFHFHDHDHDSAaACTF{SADASDSDCTF{L_E_R_OY_JENKINS}ASDCTF{\n')
```

This looks like a good one, so the initial KEY byte is 174.

Now we can proceed to recover odd bytes of the keystream.
The idea here is pretty simple:

1. Let's pre-calculate sha3_256 hashes for strings `A`, `AA`, `AAA`,... and so on, for very large lengths, specifically for 55*256, because this is the longest string we can get in the task to hash, because counter 256 for each letter. We store those hashes in a list in order.
2. Let's set all letters to the same one, for example 'A'. We can do that since we already know the keystream for all of them, and we can  simply set value `'A'^KEY[i]` for `i-th` byte and once it's xored with `KEY[i]` during decryption it will become `A`.
3. Let's calculate reference hash for the letters `A` and original counters. We can now check where on the hash list this value is, and therefore how many `A` it has.
4. Now let's XOR the first counter with `1<<1`, basically flipping the lowest bit, and calculate new hash. We can now look for index of this hash in our list, and this will tell us how many `A` it has. If it's less then initially, then we flipped the bit from 1 to 0, and if it's more, then we flipped from 0 to 1, either way we know the original bit value. We can now do the same for `1<<2` and other bits, to recover the whole counter value.
5. We proceed like this for next counters, until we recover all of them.

In code it looks like this:
```python
def recover_counters(keybytes, get_result_fun=get_result):
    hashes = []
    with codecs.open("hashes", 'r') as hashes_file:
        for line in hashes_file:
            hashes.append(line[:-1])
    # prepare payload with 'A' on even positions
    payload = [0] * (len(keybytes) * 2)
    for i in range(0, len(keybytes) * 2, 2):
        payload[i] = ord(xor_string(keybytes[i / 2], 'A'))
    counter_bytes = []
    for counter in range(1, len(keybytes) * 2, 2):
        print('recovering counter', counter)
        reference_hash = get_result_fun(payload)
        reference_number_of_A = hashes.index(reference_hash)
        bits = []
        for bit in range(8):
            new_payload = payload[:]
            new_payload[counter] ^= 1 << bit
            new_hash = get_result_fun(new_payload)
            new_A_number = hashes.index(new_hash)
            if new_A_number > reference_number_of_A:  # we set a bit so it was 0
                bits.append('0')
            else:
                bits.append('1')
        original_counter = int("".join(bits[::-1]), 2)
        print('original counter', original_counter)
        counter_bytes.append(original_counter)
    return map(chr, counter_bytes)
```

We can now extend our sanity test to include this code:

```python
def sanity_test():
    secret = "alamakotaa"

    def decrypt(data):
        return xor_string(secret, data)

    def deserialize(decrypted):
        return chunk(decrypted, 2)

    def decode(secret):
        return "".join([a * (ord(b) + 1) for a, b in secret])

    def mimick_server(data):
        import sha3
        decrypted = decrypt(data)
        secret = deserialize(decrypted)
        expanded = decode(secret)
        return sha3.sha3_256(expanded).digest()

    def fake_get_result(data):
        payload_bytes = "".join(map(chr, data))
        return mimick_server(payload_bytes).encode("base64")

    flag = xor_string("CTF{XXXXX}", secret)
    found = []
    for i in range(0, len(secret) - 2, 2):
        found.append(find(i, fake_get_result))
    print(found)

    real_found = [chr(ord(flag[0]) ^ ord('C'))]
    for c in found:
        real_found.append(chr(ord(real_found[-1]) ^ c))
    print(real_found)
    counters = recover_counters(real_found, fake_get_result)
    print(counters)
    print(reduce(lambda x, y: x + y, map(lambda x: x[0] + x[1], zip(real_found, counters))))
```

And once we run this we get the `secret` value back, so it all works.
We can therefore plug the counter recovery to the real data:

```python
def recover_from_letters():
    found = [191, 119, 132, 188, 171, 242, 33, 15, 50, 0, 32, 130, 110, 51, 57, 36, 108, 223, 132, 48, 58, 47, 190, 144, 54, 115, 250, 91, 13, 16, 25, 193, 178,
             26, 115, 140, 231, 65, 99, 180, 221, 121, 92, 206, 16, 64, 152, 181, 231, 228, 136, 149, 177, 237, 0]
    with codecs.open("encrypted_secret") as flag_file:
        flag = flag_file.read()
        real_found = [chr(174)]
        for c in found:
            real_found.append(chr(ord(real_found[-1]) ^ c))
        print(real_found)
        counters = recover_counters(real_found)
        print(counters)
        keystream = reduce(lambda x, y: x + y, map(lambda x: x[0] + x[1], zip(real_found, counters)))
        print(keystream)
        print(decode(deserialize(xor_string(flag, keystream))))


recover_from_letters()
```

We use also the `decode` and `deserialize`, just as the server does when decrypting the flag.
After a while we finally get: `CTF{LLLLLLLLL___EEEEE____RRRRRRRRRRR_OYYYYYYYYYY_JEEEEEEENKKKINNSSS}`
