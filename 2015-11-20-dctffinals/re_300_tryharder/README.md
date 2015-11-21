## Try Harder (re, 300p)

### PL
[ENG](#eng-version)

Dostajemy [program](./re300) (elf), do zbadania.

W przeciwieństwie do poprzedniego programu tutaj wiemy (czyżby?) od razu co powinniśmy zrobić - podajemy jakiś tekst (flagę) jako parametr w linii poleceń, a program wykonuje kilka sprawdzeń i odpowiada czy flaga jest OK czy nie.

Zaczynamy więc analizę testów przeprowadzanych na fladze (od teraz będę używać sformułowań "flaga" i "wprowadzony parametr" zamiennie), jak leci:

```c++
if ( argc != 2 || strlen(argv[1]) > 0x64 ) {
    tryharder(); // wypisanie błędu i zakończenie działania
}
```

Test zerowy, sprawdzenie czy flaga nie jest dłuższa niż 0x64 znaki. Oczywiście trywialnie go spełnić (nie podawać dłuższej flagi).

```c++
bool check_1(char *flag) {
  int i;
  for (i = 0; flag[i]; ++i);
  return i == 37;
}
```

Test pierwszy - sprawdzenie czy flaga ma dokładnie 37 znaków długości. Również banalnie go spełnić, starczy podać programowi flagę o odpowiedniej długości.

Kolejny test (za dużo kodu jak na prosty koncept) - sprawdza czy flaga matchuje do wzorca `DCTF{[A-Za-z0-9]`.

I trzeci test podobny - dzieli 32 znaki flagi znajdujące się za `DCTF{` na 4bajtowe fragmenty, i każdy z nich matchuje z regexem - każdy 4bajtowy blok musiał pasować do odpowiedniego z tych regexów (w kolejności):

    '^9[0-2]6[4-7]'
    '^[0-5][0-6][b-c]5'
    '^0[1-6][1-6][1-6]'
    '^[6-9]0b0'
    '^a[0-6]'
    '^47[e-f]c'
    '^47[2-f][2-3]'
    '^5[e-f]8[e-f]'

Zaimplementowaliśmy nawet generator wszystkich możliwych flag w pythonie, co okazało sie kompletnie niepotrzebne.

To był ostatni test - w tym momencie program mówi "Well done" po podaniu flagi. Niestety, co nas bardzo zaskoczyło, strona odrzucała dalej naszą flagę.

Dopiero po chwili zorientowaliśmy się, że program nie kończy sie od razu po wyjściu z funkcji 'main' - są jeszcze destruktory.

A w destruktorach leżał kod odpowiadający czemuś takiemu:

```c++
int check(char *s) {
  signed int i;
  uint32_t v2_0 = 0;
  uint64_t v2_1 = 0;

  v2_0 = strlen(s);
  for ( i = 5; i < v2_0; ++i ) {
    v2_1 += -3 * s[i] + 36 + (int64_t)(s[i] ^ 0x2FCFBA);
  }
  int64_t result = v2_1
       - 74431661
       * (((int64_t)((unsigned __int128)((unsigned __int128)8315950649585666743LL * (unsigned __int128)v2_1) >> 64) >> 25) 
        - (v2_1 >> 63));
  return result == 25830287;
}
```

Wygląda to na skomplikowane działania, nawet nie próbowaliśmy tutaj nic reversować. Za to po prostu napisaliśmy bruferorcer w C++, który generował możliwe flagi, i sprawdzał dla każdej czy przechodzi ona funkcję 'check'. W ten sposób dość szybko znaleźliśmy "prawdziwą" flagę, przyjmowaną przez stronę (która również nie była unikalna):

    DCTF{906400b5011160b0a19f47ec47b35f8f

### ENG version

We get a [binary](./re300) (elf), do work with.

Unlike in previous task, this time we know (do we really?) what to do from the beginning - we input some text (we assume a flag) as a parameter in command line and the program checks it and tells us if the flag is good or not.

We start the analysis of the tests that are performed on the flag (from now on I will use `flag` and `input parameter` to name the same thing), as follows:


```c++
if ( argc != 2 || strlen(argv[1]) > 0x64 ) {
    tryharder(); // print error and exit
}
```

Test zero, we check if the flag is not longer than 0x64 characters. Trivial to do (just don't input longer flag).

```c++
bool check_1(char *flag) {
  int i;
  for (i = 0; flag[i]; ++i);
  return i == 37;
}
```

Test one - check if the flag has exactly 37 characters. Easy to fulfill, we just need to input flag with exactly the right length.

Next test (too much code for this simple rule, we just provide the pattern) - check if the flag matches `DCTF{[A-Za-z0-9]`.

Third test is similar - splits 32 characters of the flag that are after `DCTF{` into 4-byte parts and each one of them is matched with a regular expression - each part had to match following pattern (in order):

    '^9[0-2]6[4-7]'
    '^[0-5][0-6][b-c]5'
    '^0[1-6][1-6][1-6]'
    '^[6-9]0b0'
    '^a[0-6]'
    '^47[e-f]c'
    '^47[2-f][2-3]'
    '^5[e-f]8[e-f]'

We even implemented a generator for all possible flags in python, which turned out not useful in the end.

This was the lats test - now the binary was printing `Well done` after we put the flag. Unfortunately, surprisingly for us, the website was rejecting our flag.

After a while we realised that the program in fact does not end right after leaving `main` function - there are destructors.

In the destructors there was a code:

```c++
int check(char *s) {
  signed int i;
  uint32_t v2_0 = 0;
  uint64_t v2_1 = 0;

  v2_0 = strlen(s);
  for ( i = 5; i < v2_0; ++i ) {
    v2_1 += -3 * s[i] + 36 + (int64_t)(s[i] ^ 0x2FCFBA);
  }
  int64_t result = v2_1
       - 74431661
       * (((int64_t)((unsigned __int128)((unsigned __int128)8315950649585666743LL * (unsigned __int128)v2_1) >> 64) >> 25) 
        - (v2_1 >> 63));
  return result == 25830287;
}
```

This looks like some complex calculations, so we didn't even try to reverse this. We just wrote a brute-force code in C++ which was generating possible flags and checking this condition on them. This was we found the real flag quite fast (it was still not really unique):

    DCTF{906400b5011160b0a19f47ec47b35f8f