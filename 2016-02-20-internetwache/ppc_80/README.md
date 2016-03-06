## Brute with Force (PPC, 80p)

	Description: People say, you're good at brute forcing... Have fun! 
	Hint: You don't need to crack the 31. character (newline). 
	Try to think of different (common) time representations. 
	Hint2: Time is CET 
	
###ENG
[PL](#pl-version)

Server sends input as:

	Hint: Format is TIME:CHAR
	Char 0: Time is 22:02:54, 052th day of 2016 +- 30 seconds and the hash is: ae3c4c0487d14dd3314facdc2d4408a845da947f
	
And our task is to find the right timestamp and the right character which will hash to given value. 
Each character we find is part of the flag.
We had some problems with getting the right epoch value (timezones etc) so we hardcoded the current epoch and were looking from that point.
The hash has 160 bits so we assume it's SHA-1.
The solution is quite simple: we loop over possible timestamps and printable characters and we test if hashing them together will give the hash value we look for. Once we find the proper hash we send the response to the server and collect another hash for another character of the flag.

```python
import hashlib
import re
import socket
import string


def brute_result(hashval):
    timestamp = 1455987261
    i = 0
    while True:
        for c in string.printable:
            brute = str(timestamp + i) + ":" + c
            h = hashlib.sha1(brute).digest().encode("hex")
            if hashval == h:
                return str(timestamp + i)+":"+c
        i += 1
    print ":("


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("188.166.133.53", 11117))
    regex = "Char \d+: Time is (\d+):(\d+):(\d+), .* hash is: (.+)"
    chars = []
    initial_data = str(s.recv(4096))
    print(initial_data)
    try:
        while True:
            task = str(s.recv(4096))
            print(task)
            m = re.match(regex, task)
            hour = m.group(1)
            minute = m.group(2)
            sec = m.group(3)
            hashval = m.group(4)
            print(hour, minute, sec, hashval)
            result = brute_result(hashval)
            print(result)
            s.sendall(result + "\n")
            chars.append(result.split(":")[1])
            s.recv(4096)
    except:
        print "".join(chars)


main()
```

After some time we get: `IW{M4N_Y0U_C4N_B3_BF_M4T3RiAL!}`

###PL version

Serwer przysyła dane w postaci:

	Hint: Format is TIME:CHAR
	Char 0: Time is 22:02:54, 052th day of 2016 +- 30 seconds and the hash is: ae3c4c0487d14dd3314facdc2d4408a845da947f
	
A naszym zadaniem jest znaleźć właściwy timestamp oraz właściwy znak które razem hashują się do podanej wartości.
Każdy znaleziony znak to fragment flagi.
Mieliśmy pewne problemy z ustaleniem poprawnej wartości epoch (strefy czasowe etc) więc finalnie hardkodowaliśmy aktualną wartość epoch i szukaliśmy od tego punktu.
Hash ma 160 bitów więc założyliśmy że to SHA-1.
Rozwiązanie jest dość proste: pętlimy po wszystkich możliwych timestampach oraz znkach i sprawdzamy czy hashując je razem dostaniemy podany w zadaniu hash. Kiedy znajdziemy odpowiednie wartości wysyłamy odpowiedź do serwera i pobieramy kolejny hash dla kolejnego znaku flagi.

```python
import hashlib
import re
import socket
import string


def brute_result(hashval):
    timestamp = 1455987261
    i = 0
    while True:
        for c in string.printable:
            brute = str(timestamp + i) + ":" + c
            h = hashlib.sha1(brute).digest().encode("hex")
            if hashval == h:
                return str(timestamp + i)+":"+c
        i += 1
    print ":("


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("188.166.133.53", 11117))
    regex = "Char \d+: Time is (\d+):(\d+):(\d+), .* hash is: (.+)"
    chars = []
    initial_data = str(s.recv(4096))
    print(initial_data)
    try:
        while True:
            task = str(s.recv(4096))
            print(task)
            m = re.match(regex, task)
            hour = m.group(1)
            minute = m.group(2)
            sec = m.group(3)
            hashval = m.group(4)
            print(hour, minute, sec, hashval)
            result = brute_result(hashval)
            print(result)
            s.sendall(result + "\n")
            chars.append(result.split(":")[1])
            s.recv(4096)
    except:
        print "".join(chars)


main()
```

Po kilkunastu zadaniach dostajemy: `IW{M4N_Y0U_C4N_B3_BF_M4T3RiAL!}`