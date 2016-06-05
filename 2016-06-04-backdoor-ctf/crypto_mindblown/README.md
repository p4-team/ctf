## Mindblown (Crypto)

###ENG
[PL](#pl-version)

We are given authentication logic running on the server:

```
var express = require('express');
var app = express();
var port = process.env.PORT || 9898;
var crypto = require('crypto');
var bodyParser = require('body-parser')
var salt = 'somestring';
var iteration = /// some number here;
var keylength = // some number here;

app.post('/login', function (req, res) {
	var username = req.body.username;
	var password = req.body.password;
	if (username !== 'chintu') {
		res.send('Username is wrong');
		return;
	}
	if (crypto.pbkdf2Sync(password, salt, iteration, keylength).toString() === hashOfPassword) {
		if (password === 'complexPasswordWhichContainsManyCharactersWithRandomSuffixeghjrjg') {
			// some logic here and return something
		} else {
			// return flag here
		}
	} else {
		res.send('Password is wrong');
	}
});
```

It seems straightforward: we need to login as user `chintu` and our password hash has to match the hash value for `complexPasswordWhichContainsManyCharactersWithRandomSuffixeghjrjg` while at the same time it has to be a different string.

Initially we thought it will require time-consuming hash collision generation, almost impossible since we don't know the number of iterations and keylen.

However, we found this: https://mathiasbynens.be/notes/pbkdf2-hmac which describes vulnerability of `pbkdf2Sync` function in case password is longer than the size of hash function used. 
In our case the default `sha1` hash is used and we notice that the user password is longer than 64 bytes.
This means that `pbkdf2Sync` will actually use `sha1(password)` instead of actual passsword value, and therefore we can use `sha1(password)` as `password` itself -> `sha1('complexPasswordWhichContainsManyCharactersWithRandomSuffixeghjrjg') = e6~n22k81<[p"k5hhV6*`

We therefore login using
`username: chintu`
`password: e6~n22k81<[p"k5hhV6*`

And we get the flag.

###PL version

Dostajemy kod autentykacji działającej na serwerze:

```
var express = require('express');
var app = express();
var port = process.env.PORT || 9898;
var crypto = require('crypto');
var bodyParser = require('body-parser')
var salt = 'somestring';
var iteration = /// some number here;
var keylength = // some number here;

app.post('/login', function (req, res) {
	var username = req.body.username;
	var password = req.body.password;
	if (username !== 'chintu') {
		res.send('Username is wrong');
		return;
	}
	if (crypto.pbkdf2Sync(password, salt, iteration, keylength).toString() === hashOfPassword) {
		if (password === 'complexPasswordWhichContainsManyCharactersWithRandomSuffixeghjrjg') {
			// some logic here and return something
		} else {
			// return flag here
		}
	} else {
		res.send('Password is wrong');
	}
});
```

Zadanie wydaje się dość proste koncepcyjnie: mamy zalogować się jako użytkownik `chintu` a hash podanego hasła musi zgodzić się z hashem dla hasła `complexPasswordWhichContainsManyCharactersWithRandomSuffixeghjrjg`, jednocześnie będąc innym stringiem.

Początkowo myśleliśmy, że będzie wymagało to czasochłonnego liczenia kolizji hashy, praktycznie niemożliwego przy braku znajomości liczby iteracji oraz długości klucza.

Niemniej jednak znaleźliśmy artykuł: https://mathiasbynens.be/notes/pbkdf2-hmac opisujący podatność funkcji `pbkdf2Sync` w sytuacji gdy podane hasło jest dłuższe niż rozmiar hasha używanej funkcji.

W naszym przypadku używana jest domyślna funkcja `sha1` i widzimy że hasło ma wiecej niż 64 bajty.
To oznacza, że `pbkdf2Sync` w praktyce użyje wartości `sha1(password)` zamiast wartości hasła a co za tym idzie możemy z powodzeniem użyć wartości `sha1(password)` jako `password` -> `sha1('complexPasswordWhichContainsManyCharactersWithRandomSuffixeghjrjg') = e6~n22k81<[p"k5hhV6*`


Dzięki temu logujemy się za pomocą:
`username: chintu`
`password: e6~n22k81<[p"k5hhV6*`

I dostajemy flagę.
