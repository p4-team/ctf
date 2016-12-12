# J1 (forensics)

###ENG
[PL](#pl-version)

This was a multilevel forensics task.

We were given a windows virtual machine to work with. 
The machine had user "M" with unknown password.
Intially we reset the password, but this turned out to be a bad idea since the user had bitlocker encrypoted files and the password was necessary after all.
So we used Ophcrack to recover the password hash `f6939966b0ffbc61c2c520cea20c2db0` and some online breaker told us this is `qwerty1234`.

Now we could decrypt the files:

* A picture with some meaningless email
* Email hinting that admin likes to use the same password in many places
* html page with some javascript

The javascript has some placeholders for parameters we had to guess/bruteforce but after a while we got:

```javascript
for (var d = 11; d < 12; d++) {
	var key = "";
	var clear = "";
	var encrypted = "96.28.95.118.9.2.58.29.56.52.44.25.58.51.83.8.108.20.53.37.88.2.71.80";
	secret = navigator.platform + "en-UStrue2000" ;

	for (i=0; i < secret.length; i++) { key+= String.fromCharCode(secret.charCodeAt(i) ^ d);}
	encrypted = encrypted.split ("."); for (i=0; encrypted.length > key.length; i++) { key += key; }

	for (i=0; i < encrypted.length; i++) { clear += String.fromCharCode(key.charCodeAt(i) ^ parseInt(encrypted[i]));}
	document.write (clear + "<br>");
}
```

and were left with the only interesting result:

```
<~:N0l_;flS`D]j3W/iG=:~>
```

It took us a while to realise that this is ASCII85 encoding and it decodes to `OpenStego v0.6.1`.

We used this tool on the picture we recovered, using the same admin password (as hinted in the recovered email) and we got a doc file from this.

This doc file contained a macro with flag decryption.
Sadly none of us had MS Word to open this :( Luckily quick thinking of one of our players saved us.
He uploaded this Word file to Malwr, which then opened the file inside a sandbox and provided us with a useful memory dump.
Among other things there was a base64 string, which decoded finally gave us the flag.


###PL version

Zadanie było wielopoziomowym problemem z informatyki śledczej.

Dostaliśmy windowsową maszynę wirtualną do pracy.
Na maszynie był użytkownik "M" z nieznanym hasłem.
Początkowo zresetowaliśmy hasło, ale to okazało się złym pomysłem, bo na dysku były pliku szyfrowane bitlockerem i hasło było potrzebne żeby je odzyskać.
Użyliśmy Ophcracka żeby odzyskać hash hasła `f6939966b0ffbc61c2c520cea20c2db0` a jakiś onlinowy hash breaker powiedział że to `qwerty1234`.

Teraz mogliśmy odszyfrować pliki:

* Obrazek z nieistotnym mailem
* Mail wspominający że admin lubi używać tego samego hasła wielokrotnie
* Stronę html ze skryptem JS

Skrypt miał pewne placeholdery które trzeba było zgadnąć / brutować ale po pewnym czasie uzyskaliśmy:

```javascript
for (var d = 11; d < 12; d++) {
	var key = "";
	var clear = "";
	var encrypted = "96.28.95.118.9.2.58.29.56.52.44.25.58.51.83.8.108.20.53.37.88.2.71.80";
	secret = navigator.platform + "en-UStrue2000" ;

	for (i=0; i < secret.length; i++) { key+= String.fromCharCode(secret.charCodeAt(i) ^ d);}
	encrypted = encrypted.split ("."); for (i=0; encrypted.length > key.length; i++) { key += key; }

	for (i=0; i < encrypted.length; i++) { clear += String.fromCharCode(key.charCodeAt(i) ^ parseInt(encrypted[i]));}
	document.write (clear + "<br>");
}
```

i otrzymaliśmy jedyny sensowny wynik:

```
<~:N0l_;flS`D]j3W/iG=:~>
```

Chwile zajęło nam odkrycie że to string kodowany jako ASCII85 i dekoduje się do `OpenStego v0.6.1`.

Użyliśmy tego narzędzia na odzyskanym obrazku, używając tego samego hasła admina (jak zasugerowano w mailu który odzyskaliśmy) i dostaliśmy z tego plik doc.

Ten plik worda zawierał makro które dekodowało flagę.
Niestety nikt z nas nie miał pod ręką MS Worda i nie mogliśmy tego otworzyć.
Szczęśliwie uratował nas świetny pomysł jednego z graczy.
Wrzucił on rzeczony plik na Malwr, gdzie plik został otwarty w sandboxie, z którego dostaliśmy użyteczny memdump.
Pośród różnych rzeczy był tam string base64, który po zdekodowaniu dał nam flagę.
