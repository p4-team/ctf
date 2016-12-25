# merces (re 100)

###ENG
[PL](#pl-version)

In the task we get an ELF [binary](merces) to work with.
W put it in ret-dec and we get a nice decompilation result:

```c
// Address range: 0x804842b - 0x804850a
int32_t flag(int32_t a1, int32_t a2) {
    // 0x804842b
    int32_t chars_printed; // 0x804850a_2
    if (a1 != 42 || a2 < 2) {
        // 0x8048452
        if (a1 == 42) {
            // 0x8048452
            chars_printed = g1;
            // branch -> 0x8048509
        } else {
            // 0x80484f5
            putchar(51);
            putchar(68);
            putchar(83);
            putchar(123);
            putchar(48);
            putchar(112);
            putchar(49);
            putchar(110);
            putchar(49);
            putchar(64);
            printf("_te_");
            chars_printed = printf("pr%dnd%d}\n", 3, 3);
            // branch -> 0x8048509
        }
        // 0x8048509
        return chars_printed;
    }
    // 0x804843d
    chars_printed = printf("3DS{c0ruj0u}");
    // branch -> 0x8048509
    // 0x8048509
    return chars_printed;
}

// Address range: 0x804850b - 0x804853f
int main(int argc, char ** argv) {
    int32_t v1 = argc;
    g1 = &v1;
    flag(42, argc);
    return 0;
}
```

We can see that simply running the binary will return a fake flag `3DS{c0ruj0u}` because the passed parameter is `42`.
We can also see that if we could modify the value passed to the `flag` function, for example with a debugger or by patching the binary, it would print the flag for us.
However, we don't even need that, considering we can see that that flag comes from:

```c
putchar(51);
putchar(68);
putchar(83);
putchar(123);
putchar(48);
putchar(112);
putchar(49);
putchar(110);
putchar(49);
putchar(64);
printf("_te_");
printf("pr%dnd%d}\n", 3, 3)
```

Which evaluates to `3DS{0p1n1@_te_pr3nd3}`.

###PL version

W zadaniu dostajemy ELFową [binarke](merces).
Po wrzuceniu jej do ret-dec dostajemy dość ładny zdekompilowany kod:

```c
// Address range: 0x804842b - 0x804850a
int32_t flag(int32_t a1, int32_t a2) {
    // 0x804842b
    int32_t chars_printed; // 0x804850a_2
    if (a1 != 42 || a2 < 2) {
        // 0x8048452
        if (a1 == 42) {
            // 0x8048452
            chars_printed = g1;
            // branch -> 0x8048509
        } else {
            // 0x80484f5
            putchar(51);
            putchar(68);
            putchar(83);
            putchar(123);
            putchar(48);
            putchar(112);
            putchar(49);
            putchar(110);
            putchar(49);
            putchar(64);
            printf("_te_");
            chars_printed = printf("pr%dnd%d}\n", 3, 3);
            // branch -> 0x8048509
        }
        // 0x8048509
        return chars_printed;
    }
    // 0x804843d
    chars_printed = printf("3DS{c0ruj0u}");
    // branch -> 0x8048509
    // 0x8048509
    return chars_printed;
}

// Address range: 0x804850b - 0x804853f
int main(int argc, char ** argv) {
    int32_t v1 = argc;
    g1 = &v1;
    flag(42, argc);
    return 0;
}
```

Widzimy od razu że samo uruchomienie aplikacji da nam fałszywą flagę `3DS{c0ruj0u}` ponieważ do funkcji flag przekazywany jest argument `42`.
Widzimy też, że moglibyśmy zmodyfikować tą wartość debugerem lub patchując aplikacje i wypisała by dla nas flagę.
Ale nie musimy robić nawet tego, ponieważ widać wyraźnie że prawdziwa flaga wychodzi z:

```c
putchar(51);
putchar(68);
putchar(83);
putchar(123);
putchar(48);
putchar(112);
putchar(49);
putchar(110);
putchar(49);
putchar(64);
printf("_te_");
printf("pr%dnd%d}\n", 3, 3)
```

Co ewaluuje się do `3DS{0p1n1@_te_pr3nd3}`.
