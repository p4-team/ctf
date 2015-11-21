## Time is not your friend (re, 200p)

### PL

[ENG](#eng-version)

Dostajemy [program](./re200) (elf), do zbadania, i rozpoczynamy analizę działania.

Ciekawe w programie jest to, że czyta żadnych plików, ani nie chce nic od użytkownika, ani nie bierze żadnych parametrów z linii poleceń - po prostu sie wykonuje.

Trzon programu opiera się na następującym kodzie:

```c++
bool test(int a1) {
  int v3 = a1;
  int v4 = 0;
  while (v3) {
    v1 = clock();
    sleep(5);
    v4 += v3 % 10;
    if (clock() - v1 <= 19) {
      v3 *= 137;
    }
    v3 /= 10;
  }
  return v4 == 41;
}

int getint() {
  v0 = clock();
  sleep(5);
  if (clock() - v0 > 19)
    result = 49000000;
  else
    result = 33000000;
  return result;
}

int main() {
  int v2 = 2;
  int v4 = 2;
  while(true) {
    int i;
    for ( i = 2; v4 - 1 >= i && v4 % i; ++i );
    if (i == v4) {
      v0 = clock();
      ++v2;
      sleep(3);
      if ( clock() - v0 <= 19 )
      exit(0);
      if(getint() <= v2 && test(v4)) {
          printf("Well done\n", v4);
          break;
      }
    }
    v4++;
  }
}
```

Widać masę bezsensownego kodu i sleepów. Ale przede wszystkim, co tu się dzieje? Program testuje liczby (w v4) od 2 do nieskończoności, aż znajdzie taką która mu się "podoba" (przechodzi dwa testy). Wtedy wypisuje "well done". Założyliśmy więć, że v4 jest flagą (całkiem słusznie).

Pierwszym naszym krokiem było usunięcie wszystkich sleepów (jako że zachowanie kodu zależy od szybkości w kilku miejscach, zakładamy że poprawna ścieżka to ta gdzie kod wykonuje się długo), żeby przyśpieszyć kod do takiego stanu żeby kiedyś otrzymać v4.

```c++
bool test(int a1) {
  int v3 = a1;
  int v4 = 0;
  while (v3) {
    v1 = clock();
    v4 += v3 % 10;
    v3 /= 10;
  }
  return v4 == 41;
}

int getint() {
  return 49000000;
}

int main() {
  int v2 = 2;
  int v4 = 2;
  while(true) {
    int i;
    for ( i = 2; v4 - 1 >= i && v4 % i; ++i );
    if (i == v4) {
      ++v2;
      exit(0);
      if (getint() <= v2 && test(v4)) {
          printf("DCTF{%d}\n", v4);
          break;
      }
    }
    v4++;
  }
}
```

Następnie patrzymy na działanie kodu. Po usunięciu sleepów kod robi dalej to co oryginał, ale szybciej. Myślimy więc jak go dalej przyśpieszyć.

Na pewno rzuca się w oczy bezsensowna pętla for w mainie - do czego ona służy? Mając trochę doświadczenia, rozpoznajemy ją jako sprawdzanie czy liczba v4 jest pierwsza.
Inwestujemy więc w pomocniczą funkcję sprawdzaącą to samo, ale znacznie szybciej (da się oczywiście lepiej, ale było i tak wystarczająco dobrze):

```c++
bool isprime(int number){
    if(number == 2) return true;
    if(number % 2 == 0) return false;
    for(int i=3; (i*i)<=number; i+=2){
        if(number % i == 0 ) return false;
    }
    return true;
}
```

Kolejnym krokiem było zauważenie, warunek może być spełniony dopiero kiedy v2 > 49000000 - a, jak widać od razu po spojrzeniu na kod - v2 to ilość napotkanych na razie liczb pierwszych.
Zamiast liczyć od zera do 49000000wej liczby pierwszej, możemy od razu podstawić pod v2 wartość 49000000, a pod v4 wartość 961748862 (v2-ta liczba pierwsza - 2, bo taka dokładnie relacja wiązała v2 i v4).

Ostateczna wersja funkcji main (całe źródło [znajduje się tu](hack.cpp))

```c++
int main() {
    int v2 = 49000000; // ndx liczby pierwszej
    int v4 = 961748862; // (v2-2)ta liczba pierwsza + 1
    while(true) {
        int i;
        if (isprime(v4)) {
            v2++;
            if(getint() <= v2 && test(v4)) {
                printf("DCTF{%d}\n", v4);
                break;
            }
        } v4++;
    }
}
```

W tym momencie możemy uruchomić nasz program bezpośrednio i poczekać kilka sekund aż wypluje flagę:

    DCTF{961749023}


### ENG version

We get a [binary](./re200) (elf) to work with and we start with analysis of its behaviour.

An interesting fact is that this binary does not read any files or input from use, nor does it take any command line parameters - it just executes.

The core of the program is:

```c++
bool test(int a1) {
  int v3 = a1;
  int v4 = 0;
  while (v3) {
    v1 = clock();
    sleep(5);
    v4 += v3 % 10;
    if (clock() - v1 <= 19) {
      v3 *= 137;
    }
    v3 /= 10;
  }
  return v4 == 41;
}

int getint() {
  v0 = clock();
  sleep(5);
  if (clock() - v0 > 19)
    result = 49000000;
  else
    result = 33000000;
  return result;
}

int main() {
  int v2 = 2;
  int v4 = 2;
  while(true) {
    int i;
    for ( i = 2; v4 - 1 >= i && v4 % i; ++i );
    if (i == v4) {
      v0 = clock();
      ++v2;
      sleep(3);
      if ( clock() - v0 <= 19 )
      exit(0);
      if(getint() <= v2 && test(v4)) {
          printf("Well done\n", v4);
          break;
      }
    }
    v4++;
  }
}
```

There is a lot of useless code and sleeps. But most importantly: what does this code do? It tests numbers (in v4) starting from 2 to infinity until it finds a number it `likes` (passes two checks). Then prints `well done`. We assumed that the `v4` is a flag (a good assumption as it turned out).


First step was to remove all sleeps (however since some parts of the code depend on the execution time, we assume that the correct execution path is the one that code uses when it runs longer) to speed up the code so that we can actually get `v4` in reasonable time.

```c++
bool test(int a1) {
  int v3 = a1;
  int v4 = 0;
  while (v3) {
    v1 = clock();
    v4 += v3 % 10;
    v3 /= 10;
  }
  return v4 == 41;
}

int getint() {
  return 49000000;
}

int main() {
  int v2 = 2;
  int v4 = 2;
  while(true) {
    int i;
    for ( i = 2; v4 - 1 >= i && v4 % i; ++i );
    if (i == v4) {
      ++v2;
      exit(0);
      if (getint() <= v2 && test(v4)) {
          printf("DCTF{%d}\n", v4);
          break;
      }
    }
    v4++;
  }
}
```

Then we look at the code execution. After all sleeps are removed the code is still doing what it was, but now faster. We try to improve it even further.

We notice a long loop in main - what does it do? With a little experience we recognize it as primarity check for v4. We make a function with the same goal, but much faster (of course we could do it even better, but this was sufficient):

```c++
bool isprime(int number){
    if(number == 2) return true;
    if(number % 2 == 0) return false;
    for(int i=3; (i*i)<=number; i+=2){
        if(number % i == 0 ) return false;
    }
    return true;
}
```

Next step was to notice that the condition can be fulfilled only when v2 > 49000000 and as we see in the code the v2 counts prime numbers seen so far.
Instead of counting from 0 to 49000000th prime number we can simply put 49000000 as value for v2 and 961748862 for v4 (this is the v2th prime number -2, since this was to relation between v2 and v4).

Final version of the main function (whole source [is here](hack.cpp))


```c++
int main() {
    int v2 = 49000000; // prime number index
    int v4 = 961748862; // (v2-2)th prime number + 1
    while(true) {
        int i;
        if (isprime(v4)) {
            v2++;
            if(getint() <= v2 && test(v4)) {
                printf("DCTF{%d}\n", v4);
                break;
            }
        } v4++;
    }
}
```

Now we can run the code and wait few seconds to get the flag:

    DCTF{961749023}