# Super duper advanced attack (web 100)


###ENG
[PL](#pl-version)

In this task we get access to a web page with some table displayed.
There is also input box and `search` button.
With this we can search through the contents of the table.

Very quickly we notice `SQLInjection` in where condition.
The query is something like: 

```sql
select x,y from z where y like '%input%'
```

So we can easily send as input: `fer%' union select 1,2 #` to get `1,2` as result row.
From here we check what database this is - MySQL.
There is `information_schema` table in mysql so we proceed with listing all tables:

`fer%' union SELECT table_name, table_schema FROM information_schema.tables #`

and columns:

`fer%' union SELECT COLUMN_NAME, table_name FROM INFORMATION_SCHEMA.COLUMNS #`

There was only a single normal table - `users` and it contained some md5 hashed passwords, but no flag.

We spent long time checking everything in the DB (triggers, indexes, constraints, procedures...), we tried also to load external files, but to no avail.
In the end we decided it's time to `hack` our way through this task and check how other teams are trying to work this out.
This was possible since we had access to `INFORMATION_SCHEMA.PROCESSLIST` table.
This table can list all operations that DB is performing at the moment.
So sending:

`fer%' union SELECT state,info FROM INFORMATION_SCHEMA.PROCESSLIST #`

Would print queries and operations that were currently performed.
We've seen some boring queries from sqlmap or some other scanner but then, not so long after we got a hit - there was information that database was sending `@flag` session variable to someone.
So we knew what has to be done - we just need to do `select @flag` to get: `EKO{do_not_forget_session_variables}`.

This was a badly designed task - the hardest part was "guessing" where can the flag be, not exploiting the application.

###PL version

W zadaniu dostajemy adres strony internetowej wyświetlającej tabelkę z danymi.
Jest tam też input box i `search` button.
Za ich pomocą możemy wyszukać dane z tabelki.

Dość szybko zauważamy, że formularz jest podatny na `SQLInjection` w warunku where.
Zapytanie wyglądało mniej więcej tak:

```sql
select x,y from z where y like '%input%'
```

Możemy więc wysłać jako input: `fer%' union select 1,2 #` aby dostać `1,2` jako jeden z wierszy wyniku.
Następnie sprawdziliśmy z jaką bazą mamy do czynienia - MySQL.
W tej bazie mamy tabelę `information_schema` więc korzystamy z niej żeby wylistować wszystkie tabele:

`fer%' union SELECT table_name, table_schema FROM information_schema.tables #`

I kolumny:

`fer%' union SELECT COLUMN_NAME, table_name FROM INFORMATION_SCHEMA.COLUMNS #`

Była tam tylko jedna zwykła tabela - `users` i zawierała kilka hasełm hashowanych md5, ale nie flagę.

Spędziliśmy sporo czasu sprawdzając wszystko w bazie (triggery, indeksy, ograniczenia, procedury...), próbowaliśmy także ładować pliki z dysku, ale wszystko to na nic.
Finalnie zdecydowaliśmy, że czas `shackować` to zadanie i sprawdzić jak inne drużyny podchodzą do tego zadania.
Było to możliwe, ponieważ mieliśmy dostęp do tabeli `INFORMATION_SCHEMA.PROCESSLIST`.
Ta tabela może listować wszystkie operacje które w danej chwili wykonuje baza.
Więc wysłanie:

`fer%' union SELECT state,info FROM INFORMATION_SCHEMA.PROCESSLIST #`

Wypisuje zapytania i operacje które są wykonywane.
Widzieliśmy trochę nudnych zapytań ewidentnie z sqlmapa albo innego skanera, aż w końcu po krótkim czasie pojawia się informacja, że baza wysłała komuś zmienną sesyjną `@flag`.
Teraz było już oczywiste, że należy wykonać `select @flag` aby dostać: `EKO{do_not_forget_session_variables}`

To jest przykład źle zaprojektowanego zadania gdzie najtrudniejszym elementem jest "zgadnięcie" gdzie autor schował flagę, a nie samo exploitowanie podatności.
