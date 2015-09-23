## wyvern (re, 500p, 96 solves)

To zadanie prawdopodobnie byłoby bardzo trudne do zrobienia "klasycznie" (w końcu 500 punktów), ale nam udało się je zrobić bardzo szybko za pomocą statycznej analizy (i odrobiny intuicji, a.k.a. zgadywania).

Otwieramy [binarkę](wyvern), i wita nas ściana kodu napisanego w C++ (tzn. ściana asemblera, która pewnie powstała ze średniej ilości kodu napisanego w C++ z szablonami, ale tak czy inaczej dość przytłaczająca). Zamiast zabierać się na ślepo do analizy krok po kroku przeglądamy kod statycznie, i znajdujemy ciekawy fragment:

    secret_100      dd 64h 
    secret_214      dd 0D6h
    secret_266      dd 10Ah
    secret_369      dd 171h
    secret_417      dd 1A1h
    secret_527      dd 20Fh
    secret_622      dd 26Eh
    secret_733      dd 2DDh
    secret_847      dd 34Fh
    secret_942      dd 3AEh
    secret_1054     dd 41Eh
    secret_1106     dd 452h
    secret_1222     dd 4C6h
    secret_1336     dd 538h
    secret_1441     dd 5A1h
    secret_1540     dd 604h
    secret_1589     dd 635h
    secret_1686     dd 696h
    secret_1796     dd 704h
    secret_1891     dd 763h
    secret_1996     dd 7CCh
    secret_2112     dd 840h
    secret_2165     dd 875h
    secret_2260     dd 8D4h
    secret_2336     dd 920h
    secret_2412     dd 96Ch
    secret_2498     dd 9C2h

Co w nim takiego ciekawego? No więc mamy trochę liczb, ułożonych rosnąco. Pierwsza liczba < 0x80, i każda kolejna jest większa od poprzedniej o mniej niż 0x80.

A gdyby tak zrobić ślepy strzał i sprawdzić narzucającą się rzecz?:

    >>> nums = [
    ...     0x64, 0x0D6, 0x10A, 0x171, 0x1A1, 0x20F, 0x26E, 0x2DD,
    ...     0x34F, 0x3AE, 0x41E, 0x452, 0x4C6, 0x538, 0x5A1, 0x604,
    ...     0x635, 0x696, 0x704, 0x763, 0x7CC, 0x840, 0x875, 0x8D4,
    ...     0x920, 0x96C, 0x9C2, 0xA0F
    ... ]
    >>> print ''.join(chr(b - a) for a, b in zip([0] + nums, nums))
    dr4g0n_or_p4tric1an_it5_LLVM

Szybko poszło, jesteśmy 500 punktów do przodu

