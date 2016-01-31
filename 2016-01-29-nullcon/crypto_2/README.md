##Caesar (Crypto, 400p)

	Some one was here, some one had breached the security and had infiltrated here. 
	All the evidences are touched, Logs are altered, records are modified with key as a text from book.
	The Operation was as smooth as CAESAR had Conquested Gaul. 
	After analysing the evidence we have some extracts of texts in a file. 
	We need the title of the book back, but unfortunately we only have a portion of it...

###PL
[ENG](#eng-version)

Dostajemy [plik](The_extract.txt) a z treści zadania wynika, że może być on szyfrowany za pomocą szyfru Cezara.
Uruchamiamy więc prosty skrypt:

```python
import codecs

with codecs.open("The_extract.txt") as input_file:
    data = input_file.read()
    for i in range(26):
        text = ""
        for x in data:
            c = ord(x)
            if ord('a') <= c < ord('z'):
                text += chr((c - ord('a') + i) % 26 + ord('a'))
            elif ord('A') <= c < ord('Z'):
                text += chr((c - ord('A') + i) % 26 + ord('A'))
            else:
                text += chr(c)
        print(text)
```

Który wypisuje wszystkie możliwe dekodowania, wśród których mamy:

	Dr. Sarah Tu races against time to block the most dangerous Internet malware ever created, a botnet called QUALNTO. While Sarah is closed off in her comzuter lab, her sister, Hanna, is brutally attacked and left in a coma. As Sarah reels with guilt over not being there for her sister, a web of deceztion closes in, threatening her and everyone she loves.

	Hanna’s condition is misleading. In her coma state, she is able to build a zsychic bridge with FBI Szecial Agent Jason McNeil. Her cryztic messages zlague Jason to keez Sarah safe.

	Tough and street-smart Jason McNeil doesn’t believe in visions or telezathic messages, and he fights the voice inside his head. His first imzression of Dr. Sarah Tu is another stiletto wearing ice-dragon on the war zath―until he witnesses her façade crumble after seeing her sister’s bloody, tortured body. Jason’s zrotective instinct kicks in. He falls for Sarah―hard. 

	When an extremenly dangerous arms dealer and cybercriminal discovers that Sarah blocked his botnet, he kidnzs Sarah. Zlaced in an imzossible zosition, will she destroy the botnet to zrotect national security or release it to save the man she loves

Pochodzące z książki `In the Shadow of Greed` co jest flagą.
	
###ENG version

We get a [file](The_extract.txt) and the task description suggests that the encryption is Caesar.
Therefore we run a simple script:

```python
import codecs

with codecs.open("The_extract.txt") as input_file:
    data = input_file.read()
    for i in range(26):
        text = ""
        for x in data:
            c = ord(x)
            if ord('a') <= c < ord('z'):
                text += chr((c - ord('a') + i) % 26 + ord('a'))
            elif ord('A') <= c < ord('Z'):
                text += chr((c - ord('A') + i) % 26 + ord('A'))
            else:
                text += chr(c)
        print(text)
```

Which prints all possible decryptions where we can find:

	Dr. Sarah Tu races against time to block the most dangerous Internet malware ever created, a botnet called QUALNTO. While Sarah is closed off in her comzuter lab, her sister, Hanna, is brutally attacked and left in a coma. As Sarah reels with guilt over not being there for her sister, a web of deceztion closes in, threatening her and everyone she loves.

	Hanna’s condition is misleading. In her coma state, she is able to build a zsychic bridge with FBI Szecial Agent Jason McNeil. Her cryztic messages zlague Jason to keez Sarah safe.

	Tough and street-smart Jason McNeil doesn’t believe in visions or telezathic messages, and he fights the voice inside his head. His first imzression of Dr. Sarah Tu is another stiletto wearing ice-dragon on the war zath―until he witnesses her façade crumble after seeing her sister’s bloody, tortured body. Jason’s zrotective instinct kicks in. He falls for Sarah―hard. 

	When an extremenly dangerous arms dealer and cybercriminal discovers that Sarah blocked his botnet, he kidnzs Sarah. Zlaced in an imzossible zosition, will she destroy the botnet to zrotect national security or release it to save the man she loves

Coming from `In the Shadow of Greed` book, which is the flag.
