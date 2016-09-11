## Rotten Uploader (Web, 150p)

###ENG
[PL](#pl-version)

In the task we get access to file uploader service.
Uploading is disabled and we can only download files already there.
There is a simple Path-Traversal in the GET parameter so we can actually download all the files, including index.php and download.php by using `../index.php`.
Index reveals that there is `file_list.php` file, and download.php blacklists is:

```php
<?php
header("Content-Type: application/octet-stream");
if(stripos($_GET['f'], 'file_list') !== FALSE) die();
readfile('uploads/' . $_GET['f']); // safe_dir is enabled. 
?>
```

So it seems there might be something interesting there!
We need to somehow provide the file name in a way that it does not contain `file_list` but can be read by readfile.
We checked the server headers and surprisingly there was no indication that it's a unix machine.
And on windows there is the old backward compatilibity for file names longer than 8 characters, so we try to use filename `file_l~1` and it works fine.

```php
<?php
$files = [
  [FALSE, 1, 'test.cpp', 1135, 'test.cpp'],
  [FALSE, 2, 'test.c', 74, 'test.c'],
  [TRUE, 3, 'flag_c82e41f5bb7c8d4b947c9586444578ade88fe0d7', 35, 'flag_c82e41f5bb7c8d4b947c9586444578ade88fe0d7'],
  [FALSE, 4, 'test.rb', 1446, 'test.rb'],
];
```

From here we get the name of the file with the flag and from there the flag itself.

###PL version

W zadaniu dostajemy link do uploadera plików.
Uploadowanie nie działa ale możemy ściągnąć pliki które już tam są.
Jest tam prosty błąd Path-Traversal wiec możemy pobrać wszytkie pliki, wliczając w to index.php i download.php poprzez `../index.php`.
Index informuje nas że jest tam plik `file_list.php` z listą wszytkich plików, ale download.php nie pozwala go ściągnąć:

```php
<?php
header("Content-Type: application/octet-stream");
if(stripos($_GET['f'], 'file_list') !== FALSE) die();
readfile('uploads/' . $_GET['f']); // safe_dir is enabled. 
?>
```

Wygląda na to że może tam być coś ciekawego!
Musimy jakoś dostarczyć ścieżkę do pliku tak żeby nie zawierała `file_list` ale jednocześnie żeby readfile mógł plik odczytać.
Sprawdzilismy nagłówki wysyłane przez stronę i ku naszemu zdumieniu nic nie wskazywało na maszynę unixową.
A dla windowsa istnieje wsteczna kompatybilność dla nazw plików dłuższych niż 8 znaków, więc spróbowaliśmy użyć nazwy `file_l~1` i zadziałała dając:

```php
<?php
$files = [
  [FALSE, 1, 'test.cpp', 1135, 'test.cpp'],
  [FALSE, 2, 'test.c', 74, 'test.c'],
  [TRUE, 3, 'flag_c82e41f5bb7c8d4b947c9586444578ade88fe0d7', 35, 'flag_c82e41f5bb7c8d4b947c9586444578ade88fe0d7'],
  [FALSE, 4, 'test.rb', 1446, 'test.rb'],
];
```

Stąd poznaliśmy nazwę pliku z flagę a w nim już samą flagę.
