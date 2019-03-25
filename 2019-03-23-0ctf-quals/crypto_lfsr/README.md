# zer0lfsr (crypto, 207p, 47 solved)


In the challenge we get [code](chall.py)and the [keystream](keystream).

Upon inspection of the code it's clear that it's a basic implementation of a Linear Feedback Shift Register algorithm.
The algorithm uses 3 independend LFSRs and combines their outputs into a single keystream.
Our goal is to recover the initial states of each of the generators.

First interesting thing to notice is that the state length is rather short, only 48 bits.
The other thing is that there are only 2 bits set in the mask, which means each output bit of the LFSR depends on the state of only 2 bits from the state.
The the state is shifted and the last bit is set to the output each round.

Let's first focus on breaking a single LFSR.
It's clear that if bits `k` and `m` are set in the mask, then each output bit tells us the value of `state[k]^state[m]`.
The state is shifted each time and last bit is set to the output bit.
This is interesting, because we actually know the value of this bit, from the output keystream.

If we now follow this bit when it propagages over the register, at some point it's going to have index `k` and get xored with bit at index `m`.
But the bit at index `m` is part of the initial state we're trying to recover!
So we can directly recover value of this bit.

We're lazy, so we can simply ask Z3 to follow all the bit correspondence, instead of doing this by hand:

```python
def solve_lfsr(results, index1, index2, length):
    s = z3.Solver()
    x = init_recovered = z3.BitVec('x', length)
    for result in results:
        relevant_bit1 = init_recovered & (1 << index1)
        bit1_value = z3.LShR(relevant_bit1, index1)

        relevant_bit2 = init_recovered & (1 << index2)
        bit2_value = z3.LShR(relevant_bit2, index2)

        s.add(bit1_value ^ bit2_value == result)

        init_recovered = ((init_recovered << 1) & (2 ** (length + 1) - 1)) ^ result
    s.check()
    return long_to_bytes(int(str(s.model()[x])))
```

To make things faster we omit the loop over all state bits, since we know only the `1` bits in the mask count.
We recover the value of those 2 relevant bits (masks in the task have always only 2 bits up), and add constraint that XOR of those bits should be the same as in the result.

It's enough to go over as many bits as are in the initial state, because after that the state comprises of output bits we already know.

We can check this with a simple sanity check:

```python
def sanity1():
    init = random.choice(string.lowercase)
    print('target', init)
    size = len(init) * 8
    i = bytes_to_long(init)
    target = lfsr(i, 0b11000000, size)
    results = [target.next() for _ in range(size)]
    print('result', solve_lfsr(results, 7, 6, size))
```

We succesfully proven that it's trivial to break a single LFSR.
The actual challenge uses 3 of those and combines their results via:

```python
def combine(x1, x2, x3):
    return (x1 * x2) ^ (x2 * x3) ^ (x1 * x3)
```

Since inputs to this function are single bit values it's actually:

```python
def combine(x1, x2, x3):
    return (x1 & x2) ^ (x2 & x3) ^ (x1 & x3)
```

Although there are now 3 LFSRs, it doesn't really make the challenge any harder.
The idea is still the same, but we don't know the exact value of output bits, but with enough input keystream there should be enough clear relations between the bits to make this work.

We extend the previous solver to include 3 states:


```python
def solve_3_lfsr(keystream, relevant_bit_indices, length, mask_length):
    len_mask = (2 ** (mask_length + 1) - 1)
    result_bits = map(long, "".join([bin(ord(c))[2:].zfill(8) for c in keystream]))
    s = z3.Solver()
    x = z3.BitVec('x', length)
    y = z3.BitVec('y', length)
    z = z3.BitVec('z', length)
    inits = [x, y, z]
    for result in result_bits:
        combs = []
        new_inits = []
        for index in range(3):
            relevant_bit1 = (inits[index] & (1 << relevant_bit_indices[index][0]))
            bit1_value = z3.LShR(relevant_bit1, relevant_bit_indices[index][0])
            relevant_bit2 = inits[index] & (1 << relevant_bit_indices[index][1])
            bit2_value = z3.LShR(relevant_bit2, relevant_bit_indices[index][1])
            single_lfsr_result = bit1_value ^ bit2_value
            combs.append(single_lfsr_result)
            new_init = ((inits[index] << 1) & len_mask) ^ single_lfsr_result
            new_inits.append(new_init)
        s.add(combine(combs[0], combs[1], combs[2]) == result)
        inits = new_inits
    s.check()
    model = s.model()
    print(model)
    x_res = int(str(model[x]))
    y_res = int(str(model[y]))
    z_res = int(str(model[z]))
    return x_res, y_res, z_res
```

We follow the algorithm just like previously, but now we add constraints on the result of `combine` function of 3 outputs.

We can verify that this actually works via simple sanity check:

```python
def sanity2():
    bit_size = 48
    byte_size = bit_size / 8
    init1 = urandom(byte_size)
    init2 = urandom(byte_size)
    init3 = urandom(byte_size)
    target = map(bytes_to_long, [init1, init2, init3])
    print('target', target)
    streamlen = bit_size
    mask1 = (47, 22)
    mask2 = (47, 13)
    mask3 = (47, 41)
    target1 = lfsr(bytes_to_long(init1), 0b100000000000000000000000010000000000000000000000, bit_size)
    target2 = lfsr(bytes_to_long(init2), 0b100000000000000000000000000000000010000000000000, bit_size)
    target3 = lfsr(bytes_to_long(init3), 0b100000100000000000000000000000000000000000000000, bit_size)
    keystream = ""
    for i in range(streamlen):
        b = 0
        for j in range(8):
            b = (b << 1) + combine(target1.next(), target2.next(), target3.next())
        keystream += chr(b)
    x, y, z = solve_3_lfsr(keystream, [mask1, mask2, mask3], bit_size)
    print('result', x, y, z)
    assert (target == [x, y, z])
```

It works just as expected.
Now we can plug the original inputs:

```python
def solve():
    with codecs.open("keystream", 'rb', 'utf8') as input_file:
        data = input_file.read()
        mask1 = (47, 22)
        mask2 = (47, 13)
        mask3 = (47, 41)
        x, y, z = solve_3_lfsr("".join(map(chr, map(ord, data)))[:48], [mask1, mask2, mask3], 48)
        print(x, y, z)
        init1, init2, init3 = map(long_to_bytes, [x, y, z])
        print("flag{" + hashlib.sha256(init1 + init2 + init3).hexdigest() + "}")
```

And we get back `flag{b527e2621131134ec22250cfbca75e8c9f5ae4f40370871fd55910927f66a1b4}`
