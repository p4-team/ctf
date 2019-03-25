# Baby Sponge (crypto, 297p, 27 solved)


In the challenge we get [challenge code](task.py)and the [library](CompactFIPS202.py) that is used.

It's pretty clear what is the goal:

```python
def dohash(self, msg):
    return CompactFIPS202.Keccak(1552, 48, bytearray(msg), 0x06, 32)

(...)

self.dosend("first message(hex): ")
msg0 = self.recvhex(8000)
self.dosend("second message(hex): ")
msg1 = self.recvhex(8000)
if msg0!=msg1 and self.dohash(msg0) == self.dohash(msg1):
    self.dosend("%s\n" % FLAG)
else:
    self.dosend(">.<\n")
```

We're supposed to send 2 payloads, which will be different, and yet produce the same hash value.

The hashing algorithm is Keccak, and the library they use is legit.
However, if we inspect the default parameter values the library uses we can see:

```python
def SHAKE128(inputBytes, outputByteLen):
    return Keccak(1344, 256, inputBytes, 0x1F, outputByteLen)

def SHAKE256(inputBytes, outputByteLen):
    return Keccak(1088, 512, inputBytes, 0x1F, outputByteLen)

def SHA3_224(inputBytes):
    return Keccak(1152, 448, inputBytes, 0x06, 224//8)

def SHA3_256(inputBytes):
    return Keccak(1088, 512, inputBytes, 0x06, 256//8)

def SHA3_384(inputBytes):
    return Keccak(832, 768, inputBytes, 0x06, 384//8)

def SHA3_512(inputBytes):
    return Keccak(576, 1024, inputBytes, 0x06, 512//8)
```

You might notice that the second parameter is drastically smaller in our case.
This is the key observation here!

The parameter with the tiny value is called `capacity`.
It's not actually used in the code directly at all apart from a check that `rate+capacity == 1600`.

Capacity is the part of the hash state which can't be directly modified by our inputs.
Relevant part of Keccak algorithm can be simplified to:

```python
state = 0
for data_chunk in chunk(input_data, rate_size):
    state ^= data_chunk
    state = F(state)

# generate output, we don't care
```
We don't really care about the rest, and we can assume `F` here is some random permutation of the state.

The `state` here can be viewed ad split into 2 parts `r|c`, the `r` part is XORed with our data chunk, but the `c` part is modified only when `F` function shuffles the state.

In order to get a collision, we want the whole state to be identical at some point.

We can influence part of the state by our input, since they're getting XORed, but we can't directly change the `capacity` part.

The idea is to find a random collision on `c`, and then modify `r` by sending prepared data chunk, to get identical state.

Let's assume for a moment `c` size is just 8 bits.
Let's hash a random data block, and extract `c` value before the shuffle and output generation permutations.
Now we hash random blocks until we find one for which `c` value is the same.
For 8 bits there are only 256 possible values of `c`, so it should be easy to find a block like this fast.

Now that we have two such inputs, we want to add a second data chunk to each one of them, to force identical rest of the state.
This is trivial, since the algorithm XORs the state with input data chunk.

For example if we extend the first input with only 0 bytes, then after the XOR the `r` part of the state will not change.

We can extend the second input with XOR of the internal state from hashing both of the inputs.
XOR with internal state this input had before, would zero the state, and XOR with state of the other input, would set the internal state value to be identical.

We can verify this with a simple sanity check (rate set to 8):

```python
def sanity():
    msg = urandom(rate / 8)
    _, c, state1 = hash(msg)
    while True:
        msg2 = urandom(rate / 8)
        _, c2, state2 = hash(msg2)
        if c == c2:
            break
    zero = '\0' * (rate / 8)
    res1, _, _ = hash(msg + zero)
    fixer = xor_hex(state1, state2).decode("hex")[:-(capacity / 8)]
    res2, _, _ = hash(msg2 + fixer)
    print('res1', res1)
    print('res2', res2)
    assert res1 == res2
    assert msg != msg2
```

We're using here a modified version of the orignal hashing function, which leaks the `capacity` and `internal state`:

```python
def Keccak(rate, capacity, inputBytes, delimitedSuffix, outputByteLen):
    outputBytes = bytearray()
    state = bytearray([0 for i in range(200)])
    rateInBytes = rate // 8
    blockSize = 0
    if (((rate + capacity) != 1600) or ((rate % 8) != 0)):
        return
    inputOffset = 0
    # === Absorb all the input blocks ===
    while (inputOffset < len(inputBytes)):
        blockSize = min(len(inputBytes) - inputOffset, rateInBytes)
        for i in range(blockSize):
            state[i] = state[i] ^ inputBytes[i + inputOffset]
        inputOffset = inputOffset + blockSize
        if (blockSize == rateInBytes):
            state = KeccakF1600(state)
            blockSize = 0
        # we leak those values at the end
        state_hex = str(state).encode("hex")
        c = state[-capacity / 8:]
(...)
```

So the solver is quite simple, the same as in the sanity check:

```python
def collide():
    msg, msg2 = collision_search()
    zero = '\0' * (rate / 8)
    _, _, state1 = hash(msg)
    res1, _, _ = hash(msg + zero)
    _, _, state2 = hash(msg2)
    fixer = xor_hex(state1, state2).decode("hex")[:-(capacity / 8)]
    res2, _, _ = hash(msg2 + fixer)
    print(msg, msg2)
    assert msg != msg2
    assert res1 == res2
    return msg + zero, msg2 + fixer
```

The tricky part is now the `collision_search` function.
For the sanity check we assumed the capacity to have only 8 bits, but in reality it's 48.

Fortunately we don't really need a collision with any selected input, it can be random collision between two random inputs.
This means we can use birthday paradox -> generate lots of inputs and `c` for them, and check if any of them collide.
This means we should be able to get a collision in about `2**24` which is doable.

We made a simple paralell solver for this:

```python
def worker(msgs):
    return [(msg, hash(msg)[1]) for msg in msgs]


def collision_search():
    bytes_no = rate / 8
    space = {}
    stage = 1000
    start = 0
    processes = 7
    print("generate space")
    while True:
        print(str(100 * start / (2.0 ** (capacity / 2 + 1))) + "%")
        start += stage
        results = brute(worker, [[urandom(bytes_no) for _ in range(stage)] for _ in range(processes)], processes=processes)
        results = reduce(lambda x, y: x + y, results)
        for (msg, c) in results:
            c = str(c)
            if c in space:
                print(len(space))
                return space[c], msg
            else:
                space[c] = msg
```

Each worker function gets `stage` number of inputs to calcualte hashes for, then results are combined and we check for the collisions, extending the set of known `c` values on the way.

It takes a long while to get solution for capacity of 48 bits, but eventually we got two messages:


```
msg1 = '2ac79b239ee01b3da93a9ed8edf4d035240d03360ab7f2a90fd7797135bde103b35e08e0a60b49694d8d02acc896261f589e3320e2d7ec55d3661d3dc57716f6047b26b47d2c22fe5a8d17de4c7e9dd98d2b45f3add9503b1797d225df55116a9d4f4105442145af5d2eed582b3b2812d70eea058faeab04245b762c6993f705685e3c5e2d6488f92068b5c23b9df115938fe512cf4b24ffb80b73a45b492d1360e9de6263d8d8effd3cb2c04b5f80eb2cb8dcab0f6bba8319ba327dfc447937fd870000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
msg2 = '4cf30b4f6c5bea3644e4f7093365fc9808dec255b7930c76d4609b41edac3b3c27ab9330684f5cd6c2ab110f982ba8bf218a8a186a90bb9dbaa0f8592c64d9b4979d76b06f66660bb25fc7ec35ed57d02b53350a976fef12b902e867a4d0ac3b5f22e1571b278e5fd2c38fcce79a6e55d5ab8cc1b1e25ea245e395db388e7e0837215f253448c514049780a448c62793c01740123d5a4d6725787130c89b6b53e6fb92398f082d94301f9d6be304cada2cec6537a1db810e2d47d433e85691b209aabf987d2680385b78405abbc0b0fc8315b39d991b13c6b0f13697e1010b1e1da9b482fe966760b4322aa1f5912cfe4e86eb8addc626182d9b2cdb6f4e512e0ab8cff95b51008b5c0003fc64c38c25ab0a3b9e2ba6d959fb781d26472303cdd3404aa0b8552e5c5698837430ca5fd6600a65268e35c002e876f85ecd25a425997dbb8e35f325019cc5777d3ed65f96ce91a2d9b5f6b0e42a9946465c71104c18e067693469b347c48ad429034f7e7d2d87fd97a4fa0bc631b3440b38bdaa1edd0f694c'
```

They're different, but their hashes match.
Once we send this to the server we get back: `flag{I_wAs_th3_sh4d0w_Of_the_waXwing_sLAin__By_the_fAlse_@4zure9_in_the_window_pan3}`

Complete solver [here](solver.py)
