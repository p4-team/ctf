## Good Morning (web, 3 points, 110 solves)
	http://52.86.232.163:32800/  https://s3.amazonaws.com/bostonkeyparty/2016/bffb53340f566aef7c4169d6b74bbe01be56ad18.tgz

In this task we were given a source of web survey. It used MySQL in backend to store our answers. The script
was not using prepared statements, so we quickly came to conclusion that there has to be a SQL injection possible.
Unfortunately, our input was escaped before passing to MySQL library. However, they use their home-made escaping function
instead of properly tested official ones. 

Because the site was in Japanese, they used Shift-JIS character encoding. One of the oddities conencted to this encoding
is that it changes position of backslash - 0x5C, which is ASCII backslash, in SJIS means yen. The websocket and Python script
itself (including escaping function) use Unicode, so we can send `[yen]" stuff`, which will be converted by escaping function
to `[yen]\" stuff`, and then converted to SJIS `0x5C\" stuff`. Since 0x5C is equivalent to backslash, that means our input will
be interpreted as one escaped backslash, followed by unescaped quote, enabling us to put arbitrary SQL code there.

Proof:
```
>>> print mysql_escape(json.loads('{"type":"get_answer","question":"q","answer":"\u00a5\\\""}')["answer"]).encode("sjis")
\\"
```
Exploiting via Chrome developer console:
```
socket.onmessage=function(e){console.log(e.data);};
socket.send('{"type":"get_answer","question":"q","answer":"\u00a5\\\" OR 1=1 -- "}')

VM416:2 {"type": "got_answer", "row": [1, "flag", "BKPCTF{TryYourBestOnTheOthersToo}"]}
```
