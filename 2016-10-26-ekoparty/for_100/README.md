# Hacker In Disguise(for, 100 points, solved by 27)


```
r2C +17 d17 
rF0 r2C -17 u17 
r33 +0B d0B 
r43 +0C d0C 
rF0 r33 -0B u0B 
rF0 r43 -0C u0C 
r1B +16 d16 
rF0 r1B -16 u16 r29 +2C d2C 
r43 +0C d0C rF0 r29 -2C u2C 
rF0 r43 -0C u0C r1B +16 d16 
rF0 r1B -16 u16 r29 +2C d2C 
rF0 r29 -2C u2C 
r35 +1C d1C 
rF0 r35 -1C u1C r44 +12 d12 
r3C +18 d18 
rF0 r44 -12 u12 
rF0 r3C -18 u18 r2D +15 d15 
r29 +2C d2C rF0 r2D -15 u15 
rF0 r29 -2C u2C r2B +09 d09 
rF0 r2B -09 u09 r4B +0F d0F 
rF0 r4B -0F u0F r1C +04 d04 
r34 +0A d0A rF0 r1C -04 u04 
rF0 r34 -0A u0A 
r29 +2C d2C 
rF0 r29 -2C u2C 
r59 +E5 dE5 
r24 +08 d08 
rF0 r24 -08 u08 
r42 +0E d0E 
r44 +12 d12 rF0 r42 -0E u0E 
rF0 r44 -12 u12 
rF0 r59 -E5 uE5 
r12 +E1 dE1 
r54 +2F d2F 
rF0 r54 -2F u2F 
rF0 r12 -E1 uE1 
r33 +0B d0B 
r44 +12 d12 rF0 r33 -0B u0B 
rF0 r44 -12 u12 
r4B +0F d0F 
rF0 r4B -0F u0F r1C +04 d04 
rF0 r1C -04 u04 
r4D +13 d13 
r43 +0C d0C 
rF0 r4D -13 u13 rF0 r43 -0C u0C r1C +04 d04 
rF0 r1C -04 u04 r31 +11 d11 r44 +12 d12 
rF0 r31 -11 u11 rF0 r44 -12 u12 
r4B +0F d0F 
r1C +04 d04 rF0 r4B -0F u0F 
rF0 r1C -04 u04 
r12 +E1 dE1 
r5B +30 d30 
rF0 r5B -30 u30 
rF0 r12 -E1 uE1 
r11 +E0 dE0 
r21 +06 d06
```


The key element in solving this task is obtainting a HID keyboard mapping like [this one](https://github.com/nazywam/ctf-stuff/blob/master/usb-pcap/HIDKeyboardMappings.py)

The flag format `EKO{`, encoded, looks like this: `08 0e 12 2f` after a quick investigation we find a part of the ciphertext that corresponds to it:

```
rF0 r24 -08 u08  //E
r42 +0E d0E //K
r44 +12 d12 rF0 r42 -0E u0E  //K
rF0 r44 -12 u12  //O
rF0 r59 -E5 uE5 //shift
r12 +E1 dE1  //
r54 +2F d2F  //{
rF0 r54 -2F u2F 

```

Using some trivial deduction, we can figure out that `dHEX` signals a key-down and a `uHEX` key-up

We were able to get the flag using a simple script in python

`EKO{holapianola}`
