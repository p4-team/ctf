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

Wygląda to na skomplikowane działania, nawet nie próbowaliśmy tutaj nic reversować. Za to po prostu napisaliśmy bruferorcer w C++, który generował możliwe flagi, i sprawdzał dla każdej czy przechodzi ona funkcję 'check'. W ten sposób dość szybko znaleźliśmy "prawdziwą" flagę, przyjmowaną przez stronę (która również nie była unikalna).

