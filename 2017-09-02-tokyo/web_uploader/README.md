# Freshen uploader (web)


## ENG
[PL](#pl-version)

It was a basic 2-stage web task.
We get link to a webpage which is supposed to be some uploader service, but upload is disabled.
We can see 3 uploaded files and we can dowload them.

Download link is for example: `fup.chal.ctf.westerns.tokyo/download.php?f=6a92b449761226434f5fce6c8e87295a`

We instantly get interested in the GET parameter `f` and what exactly it might mean.
It looks like some kind of hash, but it's always a good idea to play a little bit with those, just to verify what they might be.

It turns out that in fact the parameter is not some hash stored in DB, but simply a file name!
We can pass `../index.php` and download the index file for example.

The only interesting part in index.php is:

```php
include('file_list.php');
```

Which indicates some interesting file we might want to download, however we can't!

We proceed to get the [download.php](download.php) file to verify how this feature works in the first place.

There is the first flag: `TWCTF{then_can_y0u_read_file_list?}`

The script is quite simple:

```php
$filename = $_GET['f'];
if(stripos($filename, 'file_list') != false) die();
header("Contest-Type: application/octet-stream");
header("Content-Disposition: attachment; filename='$filename'");
readfile("uploads/$filename");
```

We need to bypass the check `if(stripos($filename, 'file_list') != false) die();` but we also need to download the file which clearly has `file_list` in the name!

We quickly notice `!=` comparison here, which is very unsafe in PHP, and most likely the vulnerability here.
This comparison can cast the result value to perform comparison.
If we check what exactly `stripos` returns, it is the start index at which given string contains the target string.
Specifically if the variable starts with target string, `stripos` will return `0`, and comparison `!=` and `==` might cast this to `false` boolean!

It means that sending simply `f=file_list.php` can bypass the check, but the file is in directory one level higher so we need some `../`.
But this is not really difficult since directory traversal doesn't require the whole tree to actually be there! 
Just the final path has to be correct, so we can send `f=file_list/../../file_list.php`
This will bypass check since string starts with `file_list` and at the same time the effective path is `../file_list.php` which is what we need.

In the file we have a name of the second flag file `flag_ef02dee64eb575d84ba626a78ad4e0243aeefd19145bc6502efe7018c4085213` and we can grab it to get the other flag: `TWCTF{php_is_very_secure}`


## PL version
