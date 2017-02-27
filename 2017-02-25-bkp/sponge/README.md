# sponge (crypto, 200)

> I've written a hash function. Come up with a string that collides with "I love
> using sponges for crypto".

The hash function we were given in this task, was simply xoring the 16-byte state with 10-byte input block, and then
encrypting with AES. If the blocks were 16-byte, the collision would be trivial to find, as we know the AES key:
```
result = state2 = AES(block1 xor AES(block0 xor state0)) = AES(block1 xor AES(block0))
AESd(result) = block1 xor AES(block0)
block1 = AESd(result) xor AES(block0)
```
So, we would be able to choose any `block0` other than original, and xor it with AES-decrypted final state to get needed
block1 for collision.

Unfortunately, the blocks were 10-byte long, which meant we did not control the top 6 bytes supplied to the AES.
While the attack above would still work in some cases, we would have to calculate approximately `2**48` AES en- or decryptions.
This is not unreasonable, but we would probably run out of time during the CTF anyway. So, we wrote the state
of the hash after three blocks: (`a`, `b` and `c` are first three blocks, `D` is the final state)
```
AES(AES(a) xor b) xor c = D
AES(AES(a) xor b) =       D xor c
    AES(a) xor b  = AESd( D xor c )
               b  = AESd( D xor c ) xor AES(a)
```
So the middle block is a xor of two pseudorandom values. We control most of `a` and `c`, so we can generate a lot of values
of `AESd(D xor c)` and `AES(a)`. If they somehow end up with the same last 6 bytes, their xor with have 6 zeroes at the
end, so we will find colliding `b`.

Naive random generation of `c` and `a` would still take too long (no speed improvement in fact), but we can use 
*meet in the middle* technique. We precalculate `2**24` values of `AESd(D xor c)` and remember them in an efficient
data structure, such as hashmap, and then proceed to randomly genrating `AES(a)`, checking for each value (in constant time!)
if there is any corresponding element in the map that ends with the same 6 bytes. This takes reasonable amount of time
(although implemented in Python, only around a minute or so). Finally, we paste together `a`, `b`, `c` and `'o'` (the last
character of the original text) to get a final collision to submit.
