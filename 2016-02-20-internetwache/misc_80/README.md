## 404 Flag not found (Misc, 80p)

	I tried to download the flag, but somehow received only 404 errors :( Hint: The last 
	step is to look for flag pattern.
	
###ENG
[PL](#pl-version)

This task wsa more of stegano than misc. Pcap file contained a lot of requests to sites such as
12332abc.example.com. After collecting all of them, getting rid of all parts except of first,
and hex-decoding them, we got:
```
In the end, it's all about flags.
Whether you win or lose doesn't matter.
{Ofc, winning is cooler
Did you find other flags?
Noboby finds other flags!
Superman is my hero.
_HERO!!!_
Help me my friend, I'm lost in my own mind.
Always, always, for ever alone.
Crying until I'm dying.
Kings never die.
So do I.
}!
```
Reading first character from each line, we got flag.

###PL version

Zadanie bardziej stegano niż misc. W pcapie było sporo żądań do stron w stylu 1232abe.example.com.
Po zczytaniu ich wszystkich, zebraniu tylko pierwszych członów i odkodowaniu ich szesnastkowo,
otrzymujemy:
```
In the end, it's all about flags.
Whether you win or lose doesn't matter.
{Ofc, winning is cooler
Did you find other flags?
Noboby finds other flags!
Superman is my hero.
_HERO!!!_
Help me my friend, I'm lost in my own mind.
Always, always, for ever alone.
Crying until I'm dying.
Kings never die.
So do I.
}!
```
Czytając pierwsze znaki z każdej linii, dostajemy flagę.
