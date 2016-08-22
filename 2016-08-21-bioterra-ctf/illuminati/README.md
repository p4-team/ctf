## Illuminati (Web, 200p)

###ENG
[PL](#pl-version)

In the task we get access to a Illuminati recruitment webpage.
However the recruitment is closed and we can only send messages to the admin and he might accept us.
We could see only our own messages.

Our first assumption was that it's some standard XSS attack on the admin, but placing some example XSS payload in the form uncovered an SQL error printed.
This meant we have an SQL Injection vulnerability.
The form had 2 fields:

- subject limited to 40 characters (verified server side)
- message with no length limit

Both of them were exploitable with a `"`.
The injection point was an `INSERT INTO` query, which limited a bit our capabilities.
More so that initially we though we have to exploit the `subject` field doing some crazy SQL golfing in 40 characters, since we could not inject a `select` into the second field due to query construction.
The query was something like:

`insert into requests (id, "$subject", "$message")`

Which means that the message field content was either inside quotation marks, or if we close the quotation mark, already outside insert query.
We could chain another insert values but we didn't know the ID and thus we would not see the contents of this second insert query.

For a moment we though we will have to make a blind sqli here, but fortunately we came up with a great idea - why not chain injections from both fields at the same time, putting an injection in `subject` which will `shift` the column to the `message` field, lifting the 40 characters limit.

We figured we can put for example the subject as:

```
theSubject",concat(
```

and message as:

```
,(select whatever we want)))#
```

And therefore we escape the quotation marks by concat of empty string and our query result!

This way we could now execute any query we wanted, so we dumped the whole database via group_concat and substring.
The passwords, including the admin password, were hashed and not likely to be broken.
Rest of the database did not contain anything particularly useful.

We thought that maybe we could update the admin password to our own password hash (hoping the passwords are not salted with username as salt), but we did not have rights to do it.

It took us a while to notice that the session cookie for this task was very particular - it helped that we developed a simple python script to send queries, and thus we had session cookie as parameter.
The cookie was a number plus our user ID, which is quite odd.
So we figured that maybe it's possible to forge admin cookie.
In the database in users table there was a strange field with `last login timestamp`.
Timestamps are often used as random seeds so we checked what random can we get using our timestamp as seed and we got our missing cookie part!

Therefore, we finally extracted admin login timestamp from database via SQL Injection, we seeded random with the value, took the generated random int, glued it with admin user ID and got the final cookie `1229569179-209`, which was enough to get us logged in as admin and get the flag.

###PL version

W zadaniu dostajemy dostęp do strony rekrutacyjnej Illuminatów.
Jednakże rekrutacja jest zamknięta i możemy jedynie wysłać wiadomość do admina, który może nas zaakceptuje.
Możemy widzieć tylko nasze własne wiadomości.

Nasze pierwsze skojarzenie to oczywiście standardowy atak XSS na admina, jednakże przykładowy payload XSS w formularzu sprawił że naszym oczom ukazał się błąd SQLa.
To oznaczało, że podatność stanowi jednak SQL Injection.
Formularz miał 2 pola:

- temat z limitem 40 znaków (sprawdzane po stronie serwera)
- wiadomość bez limitu długości

Oba pola były exploitowalne przez `"`.
Punktem wstrzyknięcia było zapytanie `INSERT INTO` co trochę ograniczało nasze możliwości.
Dodatkowo początkowo myśleliśmy, że możemy użyć efektywnie tylko pola `subject` i trzeba będzie robić jakiś ciężki SQL golfing na 40 znaków, ponieważ nie mogliśmy wstrzyknąć `select` do drugiego pola ze względu  na budowę zapytania.
Zapytanie miało postać:

`insert into requests (id, "$subject", "$message")`

Co oznaczało, że zawartość pola message była albo wewnatrz cudzysłowów, albo jeśli je domknęliśmy, poza danymi do insertowania.
Moglibyśmy co prawda dołączyć kolejny zestaw danych dla insert, ale nie znaliśmy wartości ID i nie moglibyśmy zobaczyć wyniku tego drugiego zapytania.

Początkowo myśleliśmy, że skończy się na ataku blind sqli, ale na szczęście wpadliśmy na lepszy pomysł - czemu nie połączyć wstrzyknięcia z dwóch pól jednocześnie, umieszczajac w polu `subject` kod który `przesunie` kolumne do pola `message`, usuwając 40 znakowy limit.

Wymyśliliśmy, że do pola subject można dać:


```
theSubject",concat(
```

a wiadomość:

```
,(select whatever we want)))#
```

I tym samym uciekamy z cudzysłowia przez złączenie pustego stringa z wynikiem naszego zapytania!

W ten sposób mogliśmy teraz wykonać dowolne zapytania więc dumpowaliśmy całą bazę przez group_concat i substring.
Hasła w bazie, w tym hasło admina, były niestety hashowane i raczej nie wyglądały na łamalne.
Reszta bazy nie wyglądała na zbyt przydatną.

Myśleliśmy, że może da się podmienić hash hasła admina na nasz własny (licząc, że hasła nie są solone loginami), ale nie mieliśmy do tego praw.

Chwile zajęło nam zauważenie, że ciastko sesji dla tego zadania wyglądało dość nietypowo - pomógł fakt, że mieliśmy już napisany prosty skrypt pythona do wysyłania zapytań do bazy i tym samym session id było w nim parametrem.
Cookie zawierało pewien numer oraz user ID, co jest dość dziwne.
Uznaliśmy więc, że może da się sfabrykować cookie admina.
W bazie danych w tabeli użytkowników znajdowało się dziwne pole `last login timestamp`.
Znaczniki czasowe często są stosowane jako ziarna dla randoma, więc sprawdziliśmy co da nam random dla naszego timestampa jako ziarna i otrzymaliśmy liczbę z naszego cookie!

W związku z tym wyciągnęliśmy z bazy timestamp dla admina przez SQL Injection, ustawiliśmy ziarno randoma na tą wartość, pobraliśmy losową liczbę, połączyliśmy z ID admina i uzyskaliśmy cookie `1229569179-209`, które pozwoliło zalogować się do aplikacji jako admin i uzyskać flagę.
