## Serial (Reverse, 150p)

    Run and capture the flag!
    
    Download serial

###ENG
[PL](#pl-version)

We were given a binary, asking for a serial and telling us whether it's correct. Disassembling it gave a weird result - 
for example:
```
0x00400a2c      je 0x400a3c
0x00400a2e      mov ax, 0x5eb
0x00400a32      xor eax, eax
0x00400a34      je 0x400a30
0x00400a36      call 0x424a24
0x00400a3b      add byte [rdi], cl
0x00400a3d      mov dh, 0x85
```
We can see jumps into the middle of instruction, which misaligned further disassembled code. Thankfully, debugger was 
still working just fine. Stepping through the code we can see a number of checks being done on our input.
I decided to set registers manually to expected values whenever there was a `cmp` validating our input, which allowed me
to do the task in a single run. The checks were pretty basic - for example:
```
movzx eax, byte [rbp - 0x1ff]
movsx edx, al
movzx eax, byte [rbp - 0x1f2]
movsx eax, al
add eax, edx
cmp eax, 0x9b
```
This checked whether sum of two particular letters of our password are equal to 0x9B.

After collecting all the checks like this one, we manually
calculated every character. Typing it into the binary confirms it's correct, so we submitted it as a flag.

###PL version

Dostaliśmy binarkę proszącą o podanie hasła i odpowiadającej, czy jest ono poprawne. Deasemblacja niestety daje
dziwne rezultaty, na przykład:
```
0x00400a2c      je 0x400a3c
0x00400a2e      mov ax, 0x5eb
0x00400a32      xor eax, eax
0x00400a34      je 0x400a30
0x00400a36      call 0x424a24
0x00400a3b      add byte [rdi], cl
0x00400a3d      mov dh, 0x85
```
Widzimy nietypowe skoki w środek instrukcji, które powodują nieprawidłową deasemblację kodu. Na szczęście debugger
takiego problemu nie ma, wiec mogliśmy przejść instrukcja po instrukcji i obserwować jak nasze hasło jest sprawdzane.
Postanowiłem ręcznie ustawiać rejestry na oczekiwane wartości przed każdą instrukcją `cmp`, dzięki czemu wystarczyło
pojedyncze przejście przez binarkę. Na szczęście kod sprawdzający był dość prosty, na przykład:
```
movzx eax, byte [rbp - 0x1ff]
movsx edx, al
movzx eax, byte [rbp - 0x1f2]
movsx eax, al
add eax, edx
cmp eax, 0x9b
```
Ten fragment sprawdzał, czy suma pewnych dwóch znaków hasła jest równa 0x9B.

Po zebraniu wszystkich takich porównań, ręcznie ułożyliśmy hasło przechodzące je wszystkie. Binarka potwierdzała jego
poprawność, zatem wysłaliśmy je jako flagę.
