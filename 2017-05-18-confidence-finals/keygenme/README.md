# Keygenme (RE, 400p)

This challenge took me a lot of time, but it was worth it (both because it was fun, and because it was worth a lot of points).

So we had a binary with simple key checking. Entered key was simply treated as number in base36, and converted to usual base 256 (bytes). After that, we saw a big handcrafted assembly function.

It was one of the rare cases when assembly code was **much** more readable than HexRays decompiler results, so we sticked to asm (refreshing!). I added a lot of comments to assembly, resulting with [rawasm.asm](rawasm.asm).

Reversing this step was fun, but rather easy (but quite time consuming). For example:

```
  ;; CF = SHL([GGG; HHH])
shl     dword ptr [edi], 1
rcl     dword ptr [edi+4], 1
rcl     dword ptr [edi+8], 1
rcl     dword ptr [edi+0Ch], 1
rcl     dword ptr [edi+10h], 1
rcl     dword ptr [edi+14h], 1
rcl     dword ptr [edi+18h], 1
rcl     dword ptr [edi+1Ch], 1
```

As comment says, this all instructions is simple SHL of two concatenated registers.

Another popular operation was of course zeroing 128bit int:


```
  ;; [EEE] = 0
mov     edx, [ebp+mag_consts]
xor     eax, eax
mov     [esi], eax
mov     [esi+4], eax
mov     [esi+8], eax
mov     [esi+0Ch], eax
```

And adding them:


```
  ;; [GGG; HHH] += [0; DDD]
mov     eax, [edx]
add     [edi], eax
mov     eax, [edx+4]
adc     [edi+4], eax
mov     eax, [edx+8]
adc     [edi+8], eax
mov     eax, [edx+0Ch]
adc     [edi+0Ch], eax
adc     dword ptr [edi+10h], 0
adc     dword ptr [edi+14h], 0
adc     dword ptr [edi+18h], 0
adc     dword ptr [edi+1Ch], 0
```


After adding all that comments, i executed:

```
cat rawasm.asm  | grep ";;" | cut -c 6-
```

And get quite readable pseudo-asm code (where most instructions was performed on 128bit integers). It looked like this:


```
[BBB] == [ARG]
loc_F4102F:
[DDD] = [BBB]
[EEE] = 0
[FFF] = [MAG[1]]
loc_F41081:
ZF = TEST [FFF] & 1
IF ZF GOTO loc_F4116A
[HHH] = 0
[GGG] = [EEE]
 ECX = 0x80
loc_F410BD:
CF = SHL([GGG; HHH])
IF NOT CF GOTO loc_F410FC
 [GGG; HHH] += [0; DDD]
loc_F410FC:
LOOP loc_F410BD
[EEE] = 0
 ECX = 0x100
loc_F41116:
 CF = SHL [EEE; GGG; HHH]
IF CF GOTO      loc_F41152
CF = CARRY [EEE] - [*MAG]
IF CF GOTO loc_F41168
loc_F41152;
[EEE] -= [*MAG]
loc_F41168
LOOP    loc_F41116
loc_F4116A:
[HHH] = 0
[GGG] = [DDD]
ECX = 0x80
loc_F4119C:
CF = SHL [GGG; HHH]
IF NOT CF GOTO loc_F411DB
[GGG; HHH] += [0; DDD]
loc_F411DB
LOOP    loc_F4119C
[DDD] = 0
ECX = 0x100
loc_F411F5:
CF = SHL [DDD; GGG; HHH]
IF CF GOTO loc_F41231
CF = [DDD] - [*MAG]
IF CF GOTO loc_F41247
loc_F41231
[DDD] -= [*MAG]
loc_F41247:
LOOP loc_F411F5
SHR [FFF]
ZF = [FFF] == 0
IF NOT ZF GOTO loc_F41081
[BBB] = [EEE]
MAG++
CF = MAG < DRG
IF CF GOTO loc_F4102F
[AAA] = 0
[AAA; BBB] += 0x31337
[CCC] = 0
ECX = 0x100
loc_F412E9:
CF = SHL [CCC; AAA; BBB]
IF CF GOTO loc_F41325
CF = [CCC] - [DRG]
IF CF GOTO loc_F4133B
loc_F41325:
[CCC] -= [DRG]
loc_F4133B:
LOOP    loc_F412E9
RETURN [CCC] == 0
```

This may not look really pretty, but in fact we are only 10 minutes from getting quite readable code. When we change GOTOs to structural loops, we end up with this reasonable piece of pseudocode:

```
[BBB] == [ARG]

for MAG, MMM in CONSTS:
    [DDD] = [BBB]
    [EEE] = 0
    [FFF] = [MMM]

    while [FFF] != 0:
        IF [FFF] & 1:
            [HHH] = 0
            [GGG] = [EEE]
            for ECX in range(0x80):
                CF = SHL([GGG; HHH])
                IF CF:
                    continue
                [GGG; HHH] += [0; DDD]

            [EEE] = 0
            for ECX in range(0x100):
                CF = SHL [EEE; GGG; HHH]
                IF NOT CF:
                    IF [EEE] < [MAG]:
                        continue
                [EEE] -= [MAG]

        [HHH] = 0
        [GGG] = [DDD]
        for ECX in range(0x80):
            CF = SHL [GGG; HHH]
            IF CF:
                continue
            [GGG; HHH] += [0; DDD]

        [DDD] = 0
        for ECX in range(0x100):
            CF = SHL [DDD; GGG; HHH]
            IF NOT CF:
                IF [DDD] < [MAG]:
                    continue
            [DDD] -= [MAG]

        SHR [FFF]

    [BBB] = [EEE]

[AAA] = 0
[AAA; BBB] += 0x31337
[CCC] = 0

for ECX in range(0x100):
    CF = SHL [CCC; AAA; BBB]
    IF NOT CF:
        IF [CCC] < [DRG]:
            continue
    [CCC] -= [DRG]

RETURN [CCC] == 0
```

But this is not over yet. We can see that few pieces of code are repeating themselves. For example:

```
for ECX in range(0x100):
    CF = SHL [CCC; AAA; BBB]
    IF NOT CF:
        IF [CCC] < [DRG]:
            continue
    [CCC] -= [DRG]
```

Haven't I seen this one before? Hmm... Wait, this is just binary long division (throwing away quotient, so in fact it's modulo).

And this one:?

```
[HHH] = 0
[GGG] = [DDD]
for ECX in range(0x80):
    CF = SHL [GGG; HHH]
    IF CF:
        continue
    [GGG; HHH] += [0; DDD]
```

Hmm, adding, dividing/multiplying by 2 and checking outermost bit. Almost like multiplication? In fact, exactly like binary multiplication.

After recognising all those idioms, I ended up with this:

```
[BBB] == [ARG]

for MAG, MMM in CONSTS:
    [DDD] = [BBB]
    [EEE] = 0
    [FFF] = [MMM]

    while [FFF] != 0:
        IF [FFF] & 1:
            [EEE] = ([DDD] * [EEE]) % [MAG]
        [DDD] = ([DDD] * DDD]) % [MAG]

        SHR [FFF]

    [BBB] = [EEE]

[AAA; BBB] = [0; BBB] + 0x31337
return [AAA; BBB] % DRG == 0
```

So pretty! But wait, squaring and multiplying in loop? We have a name for that - `square and multiply`, fast exponentation algorithm. So... everything reduced to this in the end:

```
for mag, mmm in consts:
    print b, mmm, mag
    b = pow(b, mmm, mag)
assert (b + 0x31337) % drgns == 0
```

Reversing it should be easy enough, right? Well, not for me - I wasted around 40 minutes, because I forgot -1 inside modinv. But leaving small mishappens aside, this code worked pretty well:

```
def get_for(b):
    for mag, mmm in consts[::-1]:
        b1 = pow(b, modinv(mmm, mag-1), mag)
        if pow(b1, mmm, mag) != b:
            return
        b = b1
    return b
```

And after few tries gave us the key:

```
base = -0x31337
while True:
    base += drgns
    b = get_for(base)
    if b:
        print dump128(b).encode('hex')
        print int2base(b, 36)
        break
```

One of valid keys was
`2S6JE-L492K-M8II0-KNU1M-XAXDV`
