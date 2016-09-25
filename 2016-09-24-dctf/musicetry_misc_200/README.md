# Musicetry (Misc 200)

```
They should have forbidden this from the moment they hear abou the idea! Damn circles, rectangles is all we needed! 
```

###ENG
[PL](#pl-version)

In the task we get a webpage with a CD picture.
We thought this might be stegano, but the picture was `.jpg` and it was hotlinked from a legitimate webpage so we figured it can't be it.
We noticed also a strange `data` cookie set by the webpage.
There were 4 different cookies we could get:

```
## %%
```

```
## %% %++ %++ %++ %++ @* %++ @* #% %# %++ %++ %++ %++ %++ @** %% %++ %++ @* %# ## #% %++ %++ %++ %++ @** %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ @** ## %% %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ @*
```

```
## %% %++ %++ %++ %++ %++ %++ %++ %++ @* %++ @* %++ %++ %++ %++ %++ @* %++ %++ %++ %++ %++ %++ @* %% ##
```

```
## %% %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ @* %# %++ @** %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ @** %# %++ %++ %++ %++ %++ @***
```

One of our friends spent once a few hours on a CTF reversing a certain brainfuck-like language from scratch, using only the code which should print a flag (we know the flag prefix).
Later it turned out that this was an actual esoteric language with a specification... 
Anyway, our friend instantly recognized `data` payload as code for TapeBagel language.
And we already had interpreter for it:

https://github.com/p4-team/ctf/tree/master/2016-02-20-internetwache/re_80

So we used the interpreter to decode the inputs, getting `HINT`, `TAPE`, `DEFCESO`.
This was a big WTF for us, because we were sure this is just a hint for the task solution, so we were trying to google anything related, to no avail.
In the end one of our friends just checked if md5 of `DEFCESO` is not a flag, and it was...


###PL version

W zadaniu dostajemy linkkdo strony z obrazkiem płyty CD.
Myśleliśmy początkowo że może to być stegano, ale obrazek był `.jpg` i był linkowany z prawdziwej strony, więc uznaliśmy że to raczej nie to.
Zauważyliśmy także dziwne cookie `data` ustawiane przez stronę.
Były 4 różne wartości które mogliśmy dostać:

```
## %%
```

```
## %% %++ %++ %++ %++ @* %++ @* #% %# %++ %++ %++ %++ %++ @** %% %++ %++ @* %# ## #% %++ %++ %++ %++ @** %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ @** ## %% %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ @*
```

```
## %% %++ %++ %++ %++ %++ %++ %++ %++ @* %++ @* %++ %++ %++ %++ %++ @* %++ %++ %++ %++ %++ %++ @* %% ##
```

```
## %% %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ @* %# %++ @** %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ %++ @** %# %++ %++ %++ %++ %++ @***
```

Jeden z naszych kolegów spędził kiedyś kilka godzin na CTFie reversując język podobny do brainfucka, korzystając jedynie z kodu który miał wypisać flagę (znalism prefix flagi).
Później okazało się, że to jest opisany język ezoteryczny z istniejącą specyfikacją...
Niemniej nasz kolega od razu rozpoznał zawartość cookie `data` jako kod języka TapeBagel.
Mamy juz do niego interpreter:

https://github.com/p4-team/ctf/tree/master/2016-02-20-internetwache/re_80

Użyliśmy interpretera do odkodowania danych, dostając `HINT`, `TAPE`, `DEFCESO`.
Dalsza część to mocny WTF, ponieważ byliśmy pewni, że to tylko hint dla dalszej części zadania i próbowalismy googlować cokolwiek związanego, bez efektów.
Na koniec jeden z naszych kolegów sprawdzić czy aby czasem md5 z `DEFCESO` nie jest po prostu flagą i był...
