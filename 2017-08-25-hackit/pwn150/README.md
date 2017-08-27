# Today’s moon phase (pwn 150)

## ENG
[PL](#pl-version)

In the task we get ARM x86 [binary](pwn150) to work with.
We can run the binary via retdec and get [source](pwn150.c).

In the code we have already a nice function to read the flag.
We also have to stack canary protection.
This means we expect some stack buffer overflow to overwrite return pointer and jump to function which prints the flag.

This points to all places where we can provide some inputs to the application.
We have `getline` which reallocates memory automatically, so not here.
We have `scanf` with `%c` so again, surely not here.
We have another `scanf` with `%5hu%c` and the buffer is large enough (although retdec decompilation doesn't show this nicely).
Finally we have something interesting:

```c
snprintf((char *)&str2, 32, "%%%zus", (int64_t)(v6 % 0x10000));
scanf((char *)&str2);
```

Again retdec doesn't do justice here, but what happens is that we create a format string based on integer we read before and then we read based on this format.
We read the input into buffer initially set as:

```c
memset((char *)&v1, 0, 512);
```

So it has 512 bytes, and this is all inside a condition:

```c
if ((int16_t)v6 < 513)
```

It would seem we can't pass anything more than 512, so we can't create a format string which would allow the buffer overflow.
Let's look one more time on the format for the size: `%5hu`, so 5 digits and we read this as `unsigned short`.
5 digits seems a lot considering the max number we expect is `512`...

Now let's look at the condition one more time: `(int16_t)v6 < 513`. But surely `int16_t` is `signed short`!
So we found signed-unsigned issue here.
We could pass a value much larger than 512, as long as after casting to signed value it's lower than 513, which is simple enough because anything large will become negative.

So the exploitation chain is as follows:

1. Send random name.
2. Send `Y` (we want to send feedback)
3. Send large number to create string format allowing overflow
4. Send payload overflowing the buffer and overwrite return pointer (532 bytes + address) to function printing the flag (0x104d8)

```
python -c "print('A\n'+'Y\n'+'65536\n'+('A'*532)+chr(0xd8)+chr(0x04)+chr(0x01)+'\n')" | nc6 165.227.98.55 2222
```

And we get `h4ck1t{Astronomy_is_fun}`

## PL version

W zadaniu dostajemy [binary](pwn150) ARM x86.
Możemy zdekompilować go za pomocą retdec i dostaniemy [source](pwn150.c).

W kodzie widać od razu ładną funkcje do wypisywania flagi.
Nie ma też stack canary.
To oznacza, że spodziewamy się stack buffer overflow za pomocą którego nadpiszemy adres powrotu z funkcji i skoczymy od funkcji wypisującej flagę.

To sugeruje analizę miejsc, gdzie wprowadzamy do aplikacji dane.

Na początku mamy `getline`, ale on realokuje pamięć w miarę potrzeb, więc nie tutaj.
Następnie mamy `scanf` ale z `%c` więc też nic z tego.
Później jest kolejny `scanf` z `%5hu%c` ale bufor jest wystarczająco duży (chociaż w retdecowej dekompilacji słabo to widać).
Wreszcie mamy coś ciekawego:

```c
snprintf((char *)&str2, 32, "%%%zus", (int64_t)(v6 % 0x10000));
scanf((char *)&str2);
```

Znów retdec poległ na generacji sensownego kodu, ale zamysł jest taki, ze generujemy tu string format zależny od wartości zmiennej wczytanej wcześniej i za pomocą tego formatu pobieramy dane.
Dane idą do bufora który był przygotowany przez:

```c
memset((char *)&v1, 0, 512);
```

Więc ma 512 bajtów, a tworzenie formatu i pobieranie danych jest w warunku:

```c
if ((int16_t)v6 < 513)
```

Wydawałoby się, że nie możemy podać niczego ponad 512, więc nie wygenerujemy string format, który pozwolilby na overflow.
Popatrzmy jednak jeszcze raz na format według którego pobierany jest rozmiar: `%5hu`, więc 5 cyfr i czytamy `unsigned short`.
5 cyfr to dużo skoro oczekujemy nie wiecej niż `512`...

Popatrzmy teraz na warunek jeszcze raz: `(int16_t)v6 < 513`. A przecież `int16_t` to `signed short`!
Mamy więc błąd signed-unsigned.
Można więc przemycić wartość większą niż 512, o ile po zrzutowaniu do typu signed jej wartość będzie mniejsza niż 513, co jest trywialne, bo każda wystarczająco duża liczba będzie ujemna.

Więc schemat ataku to:

1. Wysyłamy losowe imie.
2. Wysyłamy `Y` (chcemy wysłać feedback)
3. Wysyłamy dużą liczbę która pozwoli nam utworzyć string format umożliwiający overflow
4. Wysyłamy dane przepełniające bufor i nadpisujący adres powrotu z funkcji (532 bajty + adres) na adres funkcji wypisującej flagę (0x104d8).

```
python -c "print('A\n'+'Y\n'+'65536\n'+('A'*532)+chr(0xd8)+chr(0x04)+chr(0x01)+'\n')" | nc6 165.227.98.55 2222
```

I dostajemy: `h4ck1t{Astronomy_is_fun}`
