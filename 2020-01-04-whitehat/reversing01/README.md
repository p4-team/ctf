# Reversing01, RE

As usual, we have to reverse a binary ([whitehat.exe](whitehat.exe)).
We also have an additional file, [output.png](output.png).

We start reversing, and the relevant code in binary is basically:

```cpp
v17 = fopen("data", "rb");
data = (DwordyBoi **)operator new[](60u);
for ( i = 0; i <= 14; ++i )
  data[i] = (DwordyBoi *)operator new[](0x1000u);
for ( j = 0; j <= 14; ++j )
  chonk_count = fread(data[j], 1u, 0x1000u, v17);
fclose(v17);
for ( k = 0; k <= 6; ++k )
{
  if ( !((data[2 * k]->header + data[2 * k + 1]->header) & 1) )
    std::swap<unsigned char *>((int *)&data[2 * k], (int *)&data[2 * k + 1]);
}
if ( (*data)->funny_byte != 7 || data[13]->funny_byte != 12 )
  return 1;
for ( l = 1; l <= 6; ++l )
{
  p_sum = data[l]->funny_byte - 52;
  if ( p_sum > 9u )
    return 1;
}
for ( m = 7; m <= 11; ++m )
{
  p_sum = data[m]->funny_byte - 77;
  if ( p_sum > 9u )
    return 1;
}
if ( data[12]->funny_byte - 34 > 9 )
  return 1;
p1 = pow((long double)data[1]->funny_byte, 3.0);
p2 = pow((long double)data[2]->funny_byte, 3.0) + p1;
p_sum = (signed int)(pow((long double)data[3]->funny_byte, 3.0) + p2);
if ( p_sum != 0x62 )
  return 1;
p4 = pow((long double)data[4]->funny_byte, 3.0);
p5 = pow((long double)data[5]->funny_byte, 3.0) + p4;
p6 = pow((long double)data[6]->funny_byte, 3.0) + p5;
p_sum = (signed int)(pow((long double)data[7]->funny_byte, 3.0) + p6);
if ( p_sum != 0x6B )
  return 1;
p9 = pow((long double)data[9]->funny_byte, 3.0);
p10 = pow((long double)data[10]->funny_byte, 3.0) + p9;
p11 = pow((long double)data[11]->funny_byte, 3.0) + p10;
p_sum = (signed int)(pow((long double)data[12]->funny_byte, 3.0) + p11);
if ( p_sum != 0xBFu )
  return 1;
v14 = (unsigned __int8 *)operator new[](0xF000u);
for ( n = 0; (signed int)(chonk_count + 0xE000) > n; ++n )
  v14[n] = *(&data[n / 0x1000]->header + n % 4096);
v12 = SHF(v14, chonk_count + 0xE000);
flag(v12);
bytes[0] = 0;
bytes[1] = 27;
bytes[2] = 0xBAu;
bytes[3] = 0x30;
bytes[4] = 0x50;
bytes[5] = 0xB1u;
bytes[6] = 0x7E;
bytes[7] = 0xD4u;
bytes[8] = 0xF;
bytes[9] = 0x44;
bytes[10] = 0x31;
bytes[11] = 0x77;
bytes[12] = 0xD6u;
bytes[13] = 0xB5u;
for ( ii = 0; ii <= 13; ++ii )
  data[ii]->funny_byte = bytes[ii];
v17 = fopen("output.png", "wb");
for ( jj = 0; jj <= 13; ++jj )
  fwrite(data[jj], 1u, 0x1000u, v17);
fwrite(data[14], 1u, chonk_count, v17);
fclose(v17);
```

or, in other words:

```cpp
// 1. read data from file
DwordyBoi** data = read_file("data")

// 2. do some weird swaps
for ( k = 0; k <= 6; ++k )
{
  if ( !((data[2 * k]->header + data[2 * k + 1]->header) & 1) )
    std::swap<unsigned char *>((int *)&data[2 * k], (int *)&data[2 * k + 1]);
}

// 3. some easy checks
lots_of_checks(data);

// 4. final check, and maybe print flag
flag(v12); // with a final check

// 5. overwrite some bytes, and save result to file "output.png"
for ( ii = 0; ii <= 13; ++ii )
  data[ii]->funny_byte = hardcoded_bytes[ii];

v17 = fopen("output.png", "wb");
for ( jj = 0; jj <= 13; ++jj )
  fwrite(data[jj], 1u, 0x1000u, v17);
fwrite(data[14], 1u, chonk_count, v17);
fclose(v17);
```

We've guessed that the `output.png` we got is the output that the binary will
generate for a correct `data` file. Long story short, we just brute-forced the
checks (it's probably an intended solution):

```python
import struct
from typing import List


class DwordyBoi:
    def __init__(self, chonk) -> None:
        self.chonk = chonk

    @property
    def header(self):
        return self.chonk[0]

    @property
    def fun(self):
        return self.chonk[10]

    @fun.setter
    def fun(self, value):
        self.chonk[10] = value


def validate(data: List[DwordyBoi]):
    for k in range(7):
        if (data[k*2].header + data[k*2+1].header) & 1 == 0:
            data[k*2], data[k*2+1] = data[k*2+1], data[k*2]

    if data[0].fun != 7:
        raise RuntimeError("nope 1")

    if data[13].fun != 12:
        raise RuntimeError("nope 2")

    for l in range(1, 7):
        if not 0 <= data[l].fun - 52 <= 9:
            raise RuntimeError("nope 3")

    for m in range(7, 11):
        if not 0 <= data[m].fun - 77 <= 9:
            raise RuntimeError("nope 4")

    if not 0 <= data[12].fun - 34 <= 9:
        raise RuntimeError("nope 5")

    if (data[1].fun**3 + data[2].fun**3 + data[3].fun**3) & 0xFF != 98:
        raise RuntimeError("nope 6")
        
    if (data[4].fun**3 + data[5].fun**3 + data[6].fun**3 + data[7].fun**3) & 0xFF != 107:
        raise RuntimeError("nope 7")

    if (data[9].fun**3 + data[10].fun**3 + data[11].fun**3 + data[12].fun**3) & 0xFF != 0xBF:
        raise RuntimeError("nope 8")

    return True


def makei32(i: int) -> int:
    return struct.unpack('<i', struct.pack('<i', i))[0]


options0 = []
for i in range(52, 52+10):
    for j in range(52, 52+10):
        for k in range(52, 52+10):
            if (i**3 + j**3 + k**3) & 0xFF == 0x62:
                options0.append((i, j, k))

options1 = []
for i in range(52, 52+10):
    for j in range(52, 52+10):
        for k in range(52, 52+10):
            for l in range(77, 77+10):
                if (i**3 + j**3 + k**3 + l**3) & 0xFF == 0x6B:
                    options1.append((i, j, k, l))

options2 = []
for i in range(77, 77+10):
    for j in range(77, 77+10):
        for k in range(77, 77+10):
            for l in range(34, 34+10):
                if (i**3 + j**3 + k**3 + l**3) & 0xFF == 0xBF:
                    options2.append((i, j, k, l))


def hash_it(b: bytes):
    v4 = 0x2FD2B4
    for i in b:
        v4 ^= i
        v4 = (v4 * 0x66EC73) % 2**32
    return v4


def check_it(b: int):
    v0 = (b - 0x7D) & 0xFF
    v1 = (((b >> 8) & 0xFF) + 0x7C) & 0xFF
    v2 = (((b >> 16) & 0xFFFF) - 0x5100) & 0xFFFF
    if v0 != 0x46:  # F
        return False
    if v1 != 0x6C:  # l
        return False
    if v2 != 0x6761:
        return False
    return True


print(options0)
print(options1)
print(options2)

waszumfick = open('output.png', 'rb').read()

chonks = [bytearray(waszumfick[i*0x1000:(i+1)*0x1000]) for i in range(15)]

print(len(chonks[-1]))
assert len(chonks[-1]) == 3226

data = [
    DwordyBoi(chonk) for chonk in chonks
]

data[0].fun = 7
data[13].fun = 12
for i, j, k in options0:
    data[1].fun = i
    data[2].fun = j
    data[3].fun = k
    for i, j, k, l in options1:
        data[4].fun = i
        data[5].fun = j
        data[6].fun = k
        data[7].fun = l
        for b in range(77, 77+10):
            data[8].fun = b
            for i, j, k, l in options2:
                data[9].fun = i
                data[10].fun = j
                data[11].fun = k
                data[12].fun = l

                data0 = list(data)
                for k in range(7):
                    if (data0[k*2].header + data0[k*2+1].header) & 1 == 0:
                        data0[k*2], data0[k*2+1] = data0[k*2+1], data0[k*2]

                validate(list(data0))

                denkoo = b''.join(x.chonk for x in data)
                hashoo = hash_it(denkoo)
                if check_it(hashoo):
                    print('gasp')
                    open('denk.bin', 'wb').write(b''.join(x.chonk for x in data0))
```

Code probably could be much shorter but welp, at least i saved myself low level
byte operations and the code worked on the first try.

The flag was:

```
WhiteHat{8333769562446613979}
```
