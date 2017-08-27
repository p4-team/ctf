# B3tterS0ci4lN3twork (web 50)

	Hint: try to find some cves

## ENG
[PL](#pl-version)

In the task we get access to some webpage.
We can register and log in.
In this webpage we can send messages to other users and there is a clear XSS in the messages.
This pointed us (and many other players) in wrong direction.
We can also change password and upload avatar, but it takes only `.png/.jpg` files.

Once the hint was released we had to change the approach -> CVE has to be about some real software, webserver, php version etc.
All seemed right, but we decided to check how the avatar is uploaded to the server, and we found out that it is using `wget 1.15`.

It's not the latest version, so it's a good candidate for some know vulnerabilty.
Some looking around and we found: https://legalhackers.com/advisories/Wget-Exploit-ACL-bypass-RaceCond-CVE-2016-7098.html

The issue is that until the connection is closed during file upload, the file extension check is not triggered.
This means we can upload a PHP shell and use it as long as we don't close the wget connection!

We used the PoC from the article, replacing single command execution for

```python
while True:
	command = raw_input(">")
	print urllib2.urlopen(WEBSHELL_URL+"?cmd="+command).read()
```

And we got ourselves a nice shell, which we used to list files and find hidden php file with flag:
`h4ck1t{wg3t_cv3_1n_CTF}`

## PL version

W zadaniu dostajemy link do strony internetowej.
Możemy się tam zarejestrować i zalogować.
Strona pozwala wysyłać wiadomości między użytkownikami i jest tam ewidentna podatność XSS.
To skierowało nas (i wiele innych osób) na złe tory.
Na stronie możemy też zminić hasło oraz uploadować avatar, ale tylko `.png/.jpg`.

Po udostępnieniu podpowiedzi musieliśmy zmienić podejscie -> CVE musi dotyczyć jakiegoś prawdziwego oprogramowania, serwera, wersji php itd.
Wszystko wyglądało dobrze, ale postanowiśmy sprawdzić w jaki sposób avatar jest pobierany na serwer i okazało się że za pomocą `wget 1.15`.

To nie jest najnowsza wersja, więc jest dobrym kandydatem na jakąś znaną podatność.
Chwila szukania i trafiliśmy na: https://legalhackers.com/advisories/Wget-Exploit-ACL-bypass-RaceCond-CVE-2016-7098.html

Błąd polega na tym, że dopóki połączenie z uploadem pliku nie zostanie zerwane, filtr rozszerzeń plików nie jest uruchamiany.
To oznacza że możemy uploadować PHP shell i dopóki nie zerwiemy połączenia wgeta możemy tego shella używać.

Zastosowalismy PoC z artykułu, zmieniając jedynie dla wygody jedno wykonanie komendy na:

```python
while True:
	command = raw_input(">")
	print urllib2.urlopen(WEBSHELL_URL+"?cmd="+command).read()
```

I dostaliśmy dość ładego shella, za pomocą którego listowaliśmy i wypisywaliśmy pliki, w tym ukryty plik php z flagą: `h4ck1t{wg3t_cv3_1n_CTF}`
