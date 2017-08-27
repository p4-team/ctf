# Weekands of hacker (web 150)

	Hint: : Format answer is h4ck1t{<something>}. You must type right flag on keyboard, where? Feel you real hacker. 

## ENG
[PL](#pl-version)

This was a very poor and stupid task.
We don't get anything here, we just have to look for something strange.
It was technically trivial, but tedious to find the actual task.

After the hint was relased we moved our focus to the main page of the CTF Dashboard.
There were some fancy linux consoles in html with animations, which seems to match the hint.

We browsed through the files there and we found one which was interesting -> https://ctf.com.ua/js/jquery.js

The interesting part was that it's not jquery at all.
It's the JS code which is running the consoles animations.

Once we go through it there is an interesting part:

```js
    typer:function(key){
        $m=[70,70,71,79,86,74,71,83,80,74,77,86,81,95];//times alt is pressed for Access Granted
        $c=Typer.counter-211;if (!Typer.failed&// speed of the Typer
        $c>=0){if (!(key==$m[$c]-$c)){Typer.failed=true;// remove all existing popu
        Typer.makeDenied();}if($c+1==$m.length){Typer.makeAccess()}}// remove all existing popuccess();
    },
```

It seems if we match the condition, one of the consoles will show "access granted" popup.
The condition here is trivial:

```
$m=[70,70,71,79,86,74,71,83,80,74,77,86,81,95]
//
if key==$m[$c]-$c)`
```

where `$c` is just loop couter, we just run: 

```python
"".join([chr(c-i) for i,c in enumerate([70,70,71,79,86,74,71,83,80,74,77,86,81,95])])
```

and get the flag: `h4ck1t{feelrealhacker}`

## PL version

To było dość słabe i głupie zadanie.
Nie dostajemy tutaj nic i musimy poszukać sobie czegoś dziwnego.
Zadanie było technicznie trywialne ale problemem było samo znalezienie zadania.

Po udostępnieniu podpowiedzi skierowaliśmy się do głownej strony CTFa, gdzie były linuxowe konsole w htmlu z jakimiś animacjami, co pasowało to podpowiedzi.

Przeglądając pliki na stronie trafiliśmy na jeden ciekawy -> https://ctf.com.ua/js/jquery.js

Ciekawe jest to, że to wcale nie jquery.
To kod generujący animacje na konsolach.

Trafiamy tam na ciekawy fragment:

```js
    typer:function(key){
        $m=[70,70,71,79,86,74,71,83,80,74,77,86,81,95];//times alt is pressed for Access Granted
        $c=Typer.counter-211;if (!Typer.failed&// speed of the Typer
        $c>=0){if (!(key==$m[$c]-$c)){Typer.failed=true;// remove all existing popu
        Typer.makeDenied();}if($c+1==$m.length){Typer.makeAccess()}}// remove all existing popuccess();
    },
```

Wygląda na to, że jeśli spełnimy warunek, jedna z konsol pokaże popup "access granted".
Warunek jest trywialny:

```
$m=[70,70,71,79,86,74,71,83,80,74,77,86,81,95]
//
if key==$m[$c]-$c)`
```

gdzie `$c` to licznik pętli, więc uruchamiamy:

```python
"".join([chr(c-i) for i,c in enumerate([70,70,71,79,86,74,71,83,80,74,77,86,81,95])])
```

i dostajemy flagę: `h4ck1t{feelrealhacker}`
