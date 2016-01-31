##HQLol (Web, 500p)

	Plenty of hacker movies. 
	But table FLAG isn't mapped by HQL and you aren't an DB administrator. 
	Anyway, good luck!

###PL
[ENG](#eng-version)

W zadaniu dostajemy stronę napisaną w gradle która pozwala przeglądać listę filmów o hackerach oraz wyszukiwać filmy.
Ta ostatnia opcja jest wyjatkowo ciekawa ponieważ od razu widać, że wyszukiwarka jest podatna na SQL Injection, a dodatkowo wypisuje logi błędu oraz stacktrace.

Zapytania do bazy wykonywane są poprzez Hibernate, a baza to H2. 
Użycie Hibernate oraz HQL wyklucza możliwość wykonania `union select`, niemniej cały czas możemy wykonywać podzapytania.
Ponieważ widzimy logi błędów, możemy w warunku `where` wykonywać niepoprawne rzutowania (np. stringa na inta) i w ten sposób odczytywać wartości.

Dodatkowo jak wynika z treści zadania tabela z flagą nie jest zmapowana przez Hibernate, więc jakakolwiek próba wykonania zapytania dla tabeli `flag` skończy się błędem `flag table is not mapped by Hibernate`.

Treść zadania informuje nas także, że nie jesteśmy administratorem, więc nie możemy skorzystać z funkcji `file_read()` udostępnianej przez bazę H2.

Po długiej analizie obu potencjalnych wektorów ataku - bazy H2 oraz Hibernate trafiliśmy wreszcie na interesujące zachowanie lexera/parsera HQL - nie rozpoznaje on poprawnie `non-breaking-space` w efekcie użycie takiego symbolu jest traktowane jak zwykły symbol.

Oznacza to, że `XXnon-breaking-spaceXX` zostanie potraktowane przez parser jako jedno słowo, podczas gdy baza danych potraktuje to jako dwa słowa przedzielone spacją.
Dzięki temu wysłanie ciągu `selectXflagXfromXflag` gdzie przez `X` oznaczamy non-breaking-space nie zostanie przez parser HQL zinterpretowane jako podzapytanie i nie dostaniemy błędu `table flag is not mapped`, a jednocześnie baza H2 poprawnie zinterpretuje ten ciąg jako podzapytanie.

Do pobrania konkretnej wartości wykorzystaliśmy niepoprawne rzutowanie wartości z tabeli `flag` i flagę odczytaliśmy z logu błędu.

Skrypt rozwiązujący zadanie:

```python
import requests
from bs4 import BeautifulSoup

val = u'\u00A0'

payload = u"' and (cast(concat('->', (selectXflagXfromXflagXlimitX1)) as int))=0 or ''='"
quoted = requests.utils.quote(payload)
quoted = quoted.replace('X', val)
response = requests.get('http://52.91.163.151:8080/movie/search?query=' + quoted)
soup = BeautifulSoup(response.text)
x = soup.find('dl', class_='error-details')
if x:
    print x
else:
    print response.text
```

###ENG version

In the task we get a webpage writen in gradne, which allows us to browse hacker movies and search them.
This last option is interesting since it's clear that there is a SQL Injection vulnerability there, and also because it prints out the whole error messages with stacktraces.

Database queries are handled by Hibernate and the database is H2.
Hibernate and HQL restricts us a little bit, because we can't use `union select`, however we can still execute subqueries.
Since we can see error logs we can perform incorrect casts in `where` condition (eg. string to int) and read the value from error message.

Additionally the task description states that the tabel with flag is not mapped by Hibernate, so any attempt to query this table will end up with `flag table is not mapped by Hibernate`.

The task description also informs us that we're not admin so we can't use `file_read()` function from H2 database.

After a long analysis of potential attack vectors - H2 database and Hibernate, we finally found an interesting behaviour of HQL parser - it does not handle non-breaking-spaces correctly, and therefore this symbol is treated as a normal character and not as whitespace.

This means that `XXnon-breaking-spaceXX` will be treated by parser as a single word, while the database will treat this as 2 words separated by a space.
Thanks to that, sending `selectXflagXfromXflag`, where `X` is the non-breaking-space, will not be recognized by HQL parser as subquery and thus we won't see `table flag is not mapped` error, but the database itself will recognize this as a subquery.

In order to get value from table we used the incorrect cast of the value from `flag` table and the result could be seen in errorlog.

Script to solve this task:

```python
import requests
from bs4 import BeautifulSoup

val = u'\u00A0'

payload = u"' and (cast(concat('->', (selectXflagXfromXflagXlimitX1)) as int))=0 or ''='"
quoted = requests.utils.quote(payload)
quoted = quoted.replace('X', val)
response = requests.get('http://52.91.163.151:8080/movie/search?query=' + quoted)
soup = BeautifulSoup(response.text)
x = soup.find('dl', class_='error-details')
if x:
    print x
else:
    print response.text
```
