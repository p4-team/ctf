# F4ceb00k 60s (Web 100)

```
WWWarmup challenge for your soul. http://10.13.37.11 
```

###ENG
[PL](#pl-version)

In the task we get a webpage where we can put a User-Agent string and it seemingly tells us how many users used the same UA (which seems to be random data).
Tampering with our own, real UA string we figure that the application saves logs from our entries in `/ua_logs` directory under the name taken from our UA.
We can access those files, so if we could create a file with `.php` in name, we would get a remote code execution on the server.
UA is sanitized though, so we can't do that, because the filter passes only `a-zA-Z0-9\-` range (we could confirm this by triggering an error during file creation, eg by passing a too long file name).

After a while the task got `fixed` and it turned out that our approach was totally wrong, and the application was now showing some SQL errors for certain inputs.
Injection point was `INSERT INTO` query.

This of course meant that the attack vector is in fact SQLInjection.
We did some tests and it turned out that our queries are also sanitized, but the filter is just doing simple string replace for words like `select`, so we could bypass this by putting `sselectelect` this way the `select` in the middle would be replaced with empty string, leaving `select` :)

The final payload to get the flag:

`), ((selselectect*frofromm(seselectlect load_load_filefile('/flag')) as a limit 0, 1), '2') #`

This way we tried to pass the loaded flag content as `id` field of the table we were inserting into, and thus causing the SQL error:

```
PDO::query(): SQLSTATE[HY000]: General error: 1366 Incorrect integer value: 'DCTF{02a61a4c169a1b3987fe8e128cb67c92}\x0A' for column 'id' at row 2
```

###PL version


W zadaniu dostajemy stronę internetową na której możemy podać string User-Agent a strona mówi nam ile osób użyło tego sameog UA (dane są raczej losowe).
Modyfikacje naszego prawdziwego UA pozwalają stwierdzić że strona loguje wpisywane przez nas dane do `/ua_logs` do plików pod taką nazwą jak nasze prawdziwe UA.
Możemy przeglądać te pliki, więc gdyby dało się utworzyć taki z nazwą `.php` moglibyśmy uzyskać remote code execution na serwerze.
Niestety nasze UA jest filtrowane i przepuszcza tylko `a-zA-Z0-9\-` (zweryfikowane poprzez wywołanie błędu przy wysłaniu stringa za długiego na nazwę pliku).

Po jakimś czasie zadanie zostało `naprawione` i okazało się że nasze podejście było zupełnie chybione - teraz aplikacja pokazywała błędy SQL dla niektórych inputów.
Punkt wstrzyknięcia był w zapytaniu `INSERT INTO`.

To oczywiście oznaczało że mamy do czynienia z atakiem SQLInjection.
Przeprowadziliśmy trochę testów i okazało się że dane są filtrowane poprzez proste string replace dla słów takich jak `select`, więc mogliśmy obejść to wysyłając np. `sselectelect`, gdzie filtr usuwał wewnętrzne `select` zostawiają nam `select` :)

Payload do wyciągnięcia flagi:

`), ((selselectect*frofromm(seselectlect load_load_filefile('/flag')) as a limit 0, 1), '2') #`

W ten sposób próbowalismy posłać zawartość flagi jako wartość dla pola `id` w tabeli do której wstawialiśmy dane, a to spowodowało błąd:

```
PDO::query(): SQLSTATE[HY000]: General error: 1366 Incorrect integer value: 'DCTF{02a61a4c169a1b3987fe8e128cb67c92}\x0A' for column 'id' at row 2
```
