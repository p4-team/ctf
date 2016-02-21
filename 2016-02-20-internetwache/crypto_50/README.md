## Crypto-Pirat (Crypto, 50p)

	Did the East German Secret Police see a Pirat on the sky? Help me find out! 
	Hint: We had 9 planets from 1930–2006... 
	Hint2: Each planet has a number. (There's a table on a well-known website). 
	After that you might be interested in ciphers used by the secret police. 

[attachment](ciphertext.txt)
	
###ENG
[PL](#pl-version)

This task was a bit of a guessing game, but still quite fun. 
The harder part was to start with the task.
It turned out that we had to change unicode planet symbols in the input file to planet numbers. 

```python
with open("ciphertext.txt", "rb") as file:
    data = file.read()

chars = {
    0x2295: "3",
    0x2640: "2",
    0x2646: "8",
    0x2647: "9",
}

result = "".join([chars.get(ord(c), c) for c in data.decode("utf8")])
```

Which gave us:

	82928 99283 92928 98983 89899 28983 89898 98983 89929 28392 83928 38989 92898 39292 83898 98992 83898 
	98983 89898 98392 89928 98392 89899 28389 89929 29283 89899 28392 92898 38992 83928 99292 83898 98989 
	83928 99289 83928 98992 83898 99292 92839 28989 83929 29283 92928 98983 89898 98389 92928 38989 89899 
	28392 92898 98389 89899 29283 89898 98389 92898 98389 89898 98983 89929 28392 92898 38983 89899 29292 
	83928 99289 83929 28989 89839 28983 92928 98983 89898 98392 89899 28389 83929 29283 89928 98389 92929 
	28389 92928 98389 89928 39289 89899 28392 89898 99283 92898 98992 83928 98989 92839 28989 89928 39289 
	89899 2

This seemed similar to one-time-pad encryption used by some secret services in the past.
Using the suggestion from description that it is about germany, we found the TAPIR encryption scheme, and the decryption table:

http://scz.bplaced.net/m.html#t

From this table we figured that we are interested in 2-digit partition of our data. There were only 4 different 2-digit blocks:

	82, 83, 89, 92

First one start the symbolic mode, second is a control character for space and the last two are dot and dash.
This suggests morse code.
We generate morse code from the previous code result:

```python
result = result.replace(" ", "")
result = "".join(result[i:i + 2] for i in range(0, len(result), 2))
result = result.replace("82", "")
result = result.replace("83", " ")
result = result.replace("89", ".")
result = result.replace("92", "-")
```

Which gives:

	-.- --.. ..-. .... .-- - - ..-. -- ...- ... ... -.-. -..- ..--- ..- --. .- -.-- .... -.-. -..- ..--- -.. --- --.. ... .-- ....- --.. ...-- ... .-.. ..... .-- --. . ..--- -.-. --... -. --.. ... -..- . --- .-. .--- .--. ..- -...- -...- -...- -...- -...- -...-

And this decodes as morse code to:

	KZFHWTTFMVSSCX2UGAYHCX2DOZSW4Z3SL5WGE2C7NZSXEORJPU======
	
Which we recognize as base-32 encoded string, which decoded via `base64.b32decode("KZFHWTTFMVSSCX2UGAYHCX2DOZSW4Z3SL5WGE2C7NZSXEORJPU======")` gives:

	VJ{Neee!_T00q_Cvengr_lbh_ner:)}

Which looks like some kind of shift/substitution cipher. 
It turnes out to be rot13 which decoded via `code.encode("rot_13")` gives: `IW{Arrr!_G00d_Pirate_you_are:)}`

###PL version

Zadanie wymagało trochę zgadywania, ale mimo to było dość ciekawe.
Największy problem stanowiło znalezienie punktu zaczepienia na początek.
Okazało się, że należało zamienić unicodowe symbole planet w pliku wejściowym na numery tych planet w układzie słonecznym:

```python
with open("ciphertext.txt", "rb") as file:
    data = file.read()

chars = {
    0x2295: "3",
    0x2640: "2",
    0x2646: "8",
    0x2647: "9",
}

result = "".join([chars.get(ord(c), c) for c in data.decode("utf8")])
```

To dało nam:

	82928 99283 92928 98983 89899 28983 89898 98983 89929 28392 83928 38989 92898 39292 83898 98992 83898 
	98983 89898 98392 89928 98392 89899 28389 89929 29283 89899 28392 92898 38992 83928 99292 83898 98989 
	83928 99289 83928 98992 83898 99292 92839 28989 83929 29283 92928 98983 89898 98389 92928 38989 89899 
	28392 92898 98389 89899 29283 89898 98389 92898 98389 89898 98983 89929 28392 92898 38983 89899 29292 
	83928 99289 83929 28989 89839 28983 92928 98983 89898 98392 89899 28389 83929 29283 89928 98389 92929 
	28389 92928 98389 89928 39289 89899 28392 89898 99283 92898 98992 83928 98989 92839 28989 89928 39289 
	89899 2

Przypomina to tablice do szyfrowania metodą one-time-pad stosowane przez służby specjalne w przeszłości.
Korzystając z sugestii że chodziło o niemcy, trafiamy na szyfrowanie TAPIR i tablicę dekodującą:

http://scz.bplaced.net/m.html#t

Z tej tablicy zauważamy że interesują nas podział naszych danych na 2-cyfrowe fragmenty.
To daje nam zaledwie 4 różne bloki:

	82, 83, 89, 92

Pierwszy otwiera transmisje symboliczną, drugi to znak spacji, a pozostałe dwa to kropka i kreska.
To sugeruje kod morsa, który generujemy przez:

```python
result = result.replace(" ", "")
result = "".join(result[i:i + 2] for i in range(0, len(result), 2))
result = result.replace("82", "")
result = result.replace("83", " ")
result = result.replace("89", ".")
result = result.replace("92", "-")
```

Co daje:

	-.- --.. ..-. .... .-- - - ..-. -- ...- ... ... -.-. -..- ..--- ..- --. .- -.-- .... -.-. -..- ..--- -.. --- --.. ... .-- ....- --.. ...-- ... .-.. ..... .-- --. . ..--- -.-. --... -. --.. ... -..- . --- .-. .--- .--. ..- -...- -...- -...- -...- -...- -...-

A to dekoduje się do:

	KZFHWTTFMVSSCX2UGAYHCX2DOZSW4Z3SL5WGE2C7NZSXEORJPU======
	
Co rozpoznajemy jako stringa kodowanego w base-32, który po zdekodowaniu przez `base64.b32decode("KZFHWTTFMVSSCX2UGAYHCX2DOZSW4Z3SL5WGE2C7NZSXEORJPU======")` daje:

	VJ{Neee!_T00q_Cvengr_lbh_ner:)}

Co wygląda na szyfr przestawieniowy/podstawieniowy.
Okazuje się, że jest to rot-13, który po zdekodowaniu przez `code.encode("rot_13")` daje: `IW{Arrr!_G00d_Pirate_you_are:)}`
