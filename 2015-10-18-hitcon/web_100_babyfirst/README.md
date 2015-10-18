## Babyfirst (web, 100p, ?? solves)

> baby, do it first.

> http://52.68.245.164

### PL
[ENG](#eng-version)

Po połączeniu się pod podany url wyświetla się nam taka strona:

```php
<?php
    highlight_file(__FILE__);

    $dir = 'sandbox/' . $_SERVER['REMOTE_ADDR'];
    if ( !file_exists($dir) )
        mkdir($dir);
    chdir($dir);

    $args = $_GET['args'];
    for ( $i=0; $i<count($args); $i++ ){
        if ( !preg_match('/^\w+$/', $args[$i]) )
            exit();
    }
    exec("/bin/orange " . implode(" ", $args));
?>
```

Program tworzy folder "sandbox/ADRES_IP" oraz chdiruje do niego. Możemy wyświetlić zawartość tego folderu nawigując w przeglądarce
do http://52.68.245.164/sandbox/nasze_ip.Straciliśmy w tym momencie dużo czasu na zgadywanie co robi /bin/orange (cóż, okazuje się
że nic - był to alias na /bin/yes).

Ale później zaczeliśmy myśleć, w jaki sposób można ominąć pret_match() - bo to jedyny sposób jaki widzieliśmy. Próbowaliśmy różnych rzeczy,
ale ostatecznie zauważyliśmy bardzo ciekawą rzecz - jeśli ostatnim bajtem wyrazu jest \n, przechodzi on ten check. Co to oznacza? Że możemy 
zmusić exec do wykonania czegoś takiego:

http://52.68.245.164/?args[]=a%0A&args[]=touch&args[]=cat

```
/bin/orange a
touch cat
```

I stworzy nam to plik `cat` w naszym sandboxowym folderze. Jest to bardzo duży krok w przód - możemy wykonać dowolną alfanumeryczną komendę.
Następnie myśleliśmy długo, jaką komendę wykonać - wszystko ciekawe wymagało użycia albo albo slasha, albo myślnika, albo kropki.

Odkryliśmy na szczęście w pewnym momencie, że wget ciągle wspiera pobieranie stron po IP, podanym jako longu! To znaczy że zadziała coś takiego:

http://92775836/

W tym momencie byliśmy kolejny duży krok bliżej rozwiązania zadania - wget może np. pobrać kod php z naszego serwera, a my wykonamy go za pomocą php.
Niestety, duży problem. Wget zapisuje pliki do pliku o nazwie "index.html", a my nie jesteśmy w stanie takiej nazwy zapisać (kropka!). Redirecty
po stronie serwera nie zmienią też nazwy pliku, bo do tego trzeba przekazać wgetowi odpowiednią opcję (myślnik!).

(( a to zostaje dla reva ))

### ENG version

