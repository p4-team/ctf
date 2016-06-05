## Worst Pwn Ever (Pwn)

###ENG
[PL](#pl-version)

We get netcat connection parameters to work with.
After connecting to the server we get a custom command-line prompt, but typing some random things cause the connection to close.
Some fuzzing lead us to typing `1+()` which crashes with a nice python exception that we can't add int to a tuple.
This means that our input has to be evaluated by python interpreter.
We use this to run:

```python
__import__("pty").spawn("/bin/sh")
```

To get a real shell on the target machine.
After that we tried the standard aproach with `find flag` but it gave us nothing.
Fortunately we came back to task description which stated that the admin is `environmentalist` and so we typed `set` to see evn variables and there was a variable named `_F_L_AG` containing the flag itself.

###PL version

Dostajemy parametry do połączenia się przez netcata.
Po połączeniu serwer wyświetla znak zachęty jak w shellu, ale próby wpisywania losowych rzeczy powodują zerwanie połączenia.
Trochę fuzzowanai pozwala zauważyć że wpisanie `1+()` wysypuje shella z ładnym pythonowym wyjątkiem ze nie można dodać inta do krotki.
To oznacza, że nasz input jest ewaluowany przez interpreter pythona.
W związku z tym uruchamiamy:

```python
__import__("pty").spawn("/bin/sh")
```

Aby dostać prawdziwego shella na docelowej maszynie.
Po tym próbowaliśmy trochę standardowych operacji jak `find flag` ale niczego nie znaleźliśmy.
Na szczęście wróciliśmy do opisu zadania, w którym było napisane że admin to `environmentalist` w zwiazku z tym wpisaliśmy komendę `set` żeby zobaczyć wszystkie zmienne środowiskowe i faktycznie jedną z nich była `_F_L_AG` zawierająca flagę.
