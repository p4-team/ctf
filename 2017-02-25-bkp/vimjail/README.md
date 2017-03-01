# VimJail (pwn)

###ENG
[PL](#pl-version)

In the task we get credentials to log-in on the server via SSH.
We are `ctfuser` user and we can see that there is `flagReader` binary in our home, but with it's only executable for `secretuser`.
The binary also has GUID bit set, so it can read flag in the `/.flag`.

By checking sudoers we notice that, as expected from the task name, we can sudo on secretuser when running `rvim`:

```
sudo -u secretuser rvim
```

The problem is that rvim restricts shell commands execution, so we can't simply run the `flagReader`.
It took us a lot of time to figure this out but finally we noticed that we can use a custom `.vimrc` file when starting rvim, and commands in such file will be executed with the current user provileges!

So by using file:

```
python3 import os
python3 os.system("/home/ctfuser/flagReader /.flag")
```

And running: 

```
sudo -u secretuser rvim -u ourvimrcfile
```

gives the flag `flag{rVim_is_no_silverbullet!!!111elf}`

###PL version

W zadaniu dostajemy dane do logowania na serwer po SSH.
Logujemy się jako `ctfuser` i możemy zobaczyć ze ` home jest binarka `flagReader`, ale można jej użyć tylko jako `secretuser`.
Binarka dodatkowo ma ustawiony GUID i może odczytać flagę z `/.flag`.

Po sprawdzeniu listy sudoers widzimy, że, zgodnie z oczekiwaniami po nazwie zadania, możemy zrobić sudo na secretusera uruchamiając `rvim`:

```
sudo -u secretuser rvim
```

Problem polega na tym, że rvim nie pozwala na uruchamianie komend shell więc nie możemy po prostu uruchomić `flagReader`.
Zajęło nam dość sporo czasu wpadnięcie na rozwiązanie, ale finalnie zauważyliśmy, że można przy starcie podać własny plik `.vimrc` a komendy z tego pliku zostaną wykonane z uprawnieniami aktualnego użytkownika!

Więc używając pliku:

```
python3 import os
python3 os.system("/home/ctfuser/flagReader /.flag")
```

I uruchamiając:

```
sudo -u secretuser rvim -u ourvimrcfile
```

Dostajemy flagę `flag{rVim_is_no_silverbullet!!!111elf}`
