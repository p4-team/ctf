## SRM (Reverse, 50p)

> The flag is : The valid serial number
> [Download](RM.exe)

###ENG
[PL](#pl-version)

We downloaded windows binary and run it. It asks us to enter serial and checks its validity.

We disasembled it, and checked content of its DialogFunc. We can clearly see interesting fragment:

```c
if (strlen(v13) != 16
  || v13[0] != 67
  || v25 != 88
  || v13[1] != 90
  || v13[1] + v24 != 155
  || v13[2] != 57
  || v13[2] + v23 != 155
  || v13[3] != 100
  || v22 != 55
  || v14 != 109
  || v21 != 71
  || v15 != 113
  || v15 + v20 != 170
  || v16 != 52
  || v19 != 103
  || v17 != 99
  || v18 != 56 ) {
    // FAIL
  } else {
    // OK
  }
```

Different xXX stand for different characters of input - using debugger it's easy to check which variable is which character.
Reversing this check took a while, because every comparsion had to be implemented, but when we succeeded, we get valid serial that turned out to be flag:

    CZ9dmq4c8g9G7bAX

###PL version

Pobieramy windowsową binarkę i uruchamiamy. Prosi ona o podanie serialu i sprawdza jego poprawność.

Disasemblujemy ją więc, i patrzymy na zawartośc DialogFunc. Od razu widać ciekawy fragment:

```c
if (strlen(v13) != 16
  || v13[0] != 67
  || v25 != 88
  || v13[1] != 90
  || v13[1] + v24 != 155
  || v13[2] != 57
  || v13[2] + v23 != 155
  || v13[3] != 100
  || v22 != 55
  || v14 != 109
  || v21 != 71
  || v15 != 113
  || v15 + v20 != 170
  || v16 != 52
  || v19 != 103
  || v17 != 99
  || v18 != 56 ) {
    // FAIL
  } else {
    // OK
  }
```

Różne vXX odpowiadają za różne znaki inputu - łatwo dojść do tego które odpowiadają za które przy użyciu debuggera.
Reversowanie tego zajęło chwilę bo trzeba było porównać wszystkie znaki, ale kiedy się udało, otrzymaliśmy poprawny serial, będący równoczesnie flagą:

    CZ9dmq4c8g9G7bAX
