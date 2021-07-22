# Google CTF - Comlink (394pt / 7 solves)

> We have captured a spy. They were carrying this device with them. It seems to be some kind of Z80-based processor connected to an antenna for wireless communications. We also managed to record the last message they sent but unfortunately it seems to be encrypted. According to our research it seems like the device has an AES hardware peripheral for more efficient encryption. You need to help us recover the message. We have extracted the firmware running on the device and you can also program the device with your own firmware to figure out how it works. I heard that a security researcher at ACME Corporation found some bugs in the hardware but we haven't managed to get hold of them for details and we need this solved now! Good luck!

## 1. Initial plan

We are provided with 2 files and a netcat connection:
 - `captured_transmission.dat` - clearly contained some raw bytes, we attempted to decode it as a radio transmission, but based on results, entropy and file sized we concluded that it's encrypted raw output from the device
 - `firmware.ihx` - dumped firmware from the device in Intel HEX format.
 - netcat connection where we can upload our own custom firmware in Intel HEX format

The description mentions a hardware bug, which is the key to this challenge. So our plan was to reverse the firmware, find the hardware bug and decrypt the message.

## 2. Reversing the firmware

After converting Intel HEX to binary firmware using hex2bin.py from z80asm, we used ghidra to reverse the binary:

We can see that entrypoint calls `init_hex_chars` and `main`.
```
                             start
        ram:0100 31 00 00        LD         SP,0x0
        ram:0103 cd 46 05        CALL       init_hex_chars
        ram:0106 cd ca 02        CALL       main
        ram:0109 c3 04 02        JP         infinite_loop
```

`init_hex_chars` was a function which copied a buffer of hex characters. We believe it was planned to be used as part of the challenge, as firmware doesn't use this buffer at all. `main` was quite big, but it mostly performed operation of xoring input buffer with static IV buffer of `XXXXXXXXXXXXXXXX`, so skipping to the interesting parts:

```
                             aes_interface:
        ram:02a4 c1              POP        BC
        ram:02a5 e1              POP        HL
        ram:02a6 e5              PUSH       HL
        ram:02a7 c5              PUSH       BC
        ram:02a8 11 10 80        LD         DE,0x8010
        ram:02ab 01 10 00        LD         BC,0x10
        ram:02ae ed b0           LDIR
        ram:02b0 db 30           IN         A,(0x30)
        ram:02b2 4f              LD         C,A
        ram:02b3 cb c1           SET        0x0,C
        ram:02b5 79              LD         A,C
        ram:02b6 d3 30           OUT        (0x30),A
                             wait_bit
        ram:02b8 db 30           IN         A,(0x30)
        ram:02ba 0f              RRCA
        ram:02bb 38 fb           JR         C,wait_bit
        ram:02bd c1              POP        BC
        ram:02be d1              POP        DE
        ram:02bf d5              PUSH       DE
        ram:02c0 c5              PUSH       BC
        ram:02c1 21 20 80        LD         HL,0x8020
        ram:02c4 01 10 00        LD         BC,0x10
        ram:02c7 ed b0           LDIR
        ram:02c9 c9              RET
```

Encryption key is nowhere to be found in the firmware, so it has to be embedded in the AES device. Memory region from `0x8000` to `0x8100` are mapped to respective ports:
 - port 10 (`0x8010`) - AES input buffer of 16 bytes
 - port 20 (`0x8020`) - AES output buffer of 16 bytes
 - port 30 (`0x8030`) - AES control bit, used for both starting AES and polling the status
 - `0x8100` - was used in firmware, however we concluded that modifying this value doesn't change the result of AES operation

## 3. Writing custom firmware

For that we have used [z80asm](https://www.nongnu.org/z80asm/). We started with printing back our own buffer to confirm our reversing results:

```asm
    ld b, 0x10
    ld hl, input
    call send_buf
infi:
    jr infi

; e = byte
send_byte:
    in a, (1)
    rrca
    jr c, send_byte

    ld a, e
    out (0), a

    in a, (1)
    or 1
    out (1), a
    ret

; b = count
; hl = ptr
send_buf:
    ld e, (hl)
    inc hl
    call send_byte
    djnz send_buf
    ret

input: db "AAAAAAAAAAAAAAAA"
```

And later decided to use the AES (skipping utility functions from above):

```asm
    ; send input bytes to AES device
    ld bc, 0x10
    ld de, 0x8010
    ld hl, input
    ldir

    ; start encryption
    ld a, 0x01
    out (0x30), a

    ; wait for encryption end
wait:
    in a,(0x30)
    rrca
    jr c, wait

    ld hl, 0x8020
    ld b, 0x10
    call send_buf

infi:
    jr infi

input: db "AAAAAAAAAAAAAAAA"
```

Which returned our encrypted buffer.

## 4. Finding the bug

We had a few ideas:
 - description of the challenge says *z80 based*, so maybe there's a bug in one of the obscure instructions?
 - AES module has a bug and doesn't perform *real* AES, but one with a bug, so maybe fewer rounds?
 - there might be a bug in communication between the devices?

It took us some time to confirm / refute those ideas, but while testing communication issues, we attempted this payload:

```asm
    ;call encrypt
    ld hl, input
    ld de, 0x8010
    ld bc, 0x10
    ldir

	ld a, 0x01
    ld b, 0xff
wait:
    out (0x30), a
    djnz wait

    ld hl, 0x8020
    ld de, 0x9000
    ld bc, 0x10
    ldir

    ld hl, 0x8020
    ld de, 0x9010
    ld bc, 0x10
    ldir

    ld hl, 0x9000
    ld b, 0x20
    call send_buf

infi:
    jr infi
```

It performs AES, while spamming port `0x30` with the value `0x01`, so it attempts over and over to start encryption process. After that it copies the buffer twice and sends both copies to us.

```
[+] Opening connection to comlink.2021.ctfcompetition.com on port 1337: Done
[*] 00000000  2a 45 a9 67  6d 00 47 16  0c 72 69 b2  cf 4a c3 f1  │*E·g│m·G·│·ri·│·J··│
    00000010  8c f0 46 67  6d 00 47 16  0c 72 69 b2  cf 4a c3 f1  │··Fg│m·G·│·ri·│·J··│
```

As you can see, first 3 bytes differ between outputs! We were quite baffled. What did it mean? We tried counting how many cycles it takes to perform encryption, but then realised the entire buffer differs, but only for a short time. By starting the read process with different offset we could read entire value of this "modified" buffer.

```asm
    ;call encrypt
    ld hl, input
    ld de, 0x8010
    ld bc, 0x10
    ldir

    ld hl, 0x8020
    call attack

    ld hl, 0x8024
    call attack

    ld hl, 0x8028
    call attack

    ld hl, 0x802c
    call attack

infi:
    jr infi

attack:
    ld de, 0x9000
    ld bc, 0x4

    ld a, 0x01
    out (0x30), a
    out (0x30), a

    ldir

    ld hl, 0x9000
    ld b, 0x4
    jr send_buf

input: db 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
```

And the output:

```
[+] Opening connection to comlink.2021.ctfcompetition.com on port 1337: Done
[*] 00000000  1d 05 ef e8  63 c3 d9 92  a8 f1 7b ce  93 47 59 5b  │····│c···│··{·│·GY[│
```

## 5. Putting pieces together

We deduced, that perhaps the AES device handles interrupts incorrectly and exposes to us internal buffer when we perform multiple writes to port `0x30`. This lead us to believe, that if we can read the state of internal buffer after first round - which is xoring the input buffer with key - we could then recover the key. Since we used inbut buffer of null bytes - we already had the key! All that we needed to do is perform the decryption:

```py
from Crypto.Cipher import AES

a = AES.new(key=bytes.fromhex("1d05efe863c3d992a8f17bce9347595b"), mode=AES.MODE_CBC, iv=b"X"*16)
with open("captured_transmission.dat", "rb") as f:
    print(a.decrypt(f.read()))
```

Output:
```
This is agent 1337 reporting back to base. I have completed the mission but I am being pursued by enemy operatives. They are closing in on me and I suspect the safe-house has been compromised. I managed to steal the codes to the mainframe and sending it over now: CTF{HAVE_YOU_EVER_SEEN_A_Z80_CPU_WITH_AN_AES_PERIPHERAL}. If you do not hear from me again, assume the worst. Agent out!
```

Final flag: `CTF{HAVE_YOU_EVER_SEEN_A_Z80_CPU_WITH_AN_AES_PERIPHERAL}`
