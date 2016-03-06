## Eso Tape (RE, 80p)

	Description: I once took a nap on my keyboard. I dreamed of a brand new language, but
	I could not decipher it nor get its meaning. Can you help me? Hint: Replace the
	spaces with either '{' or '}' in the solution. Hint: Interpreters don't help. 
	Operations write to the current index.

###ENG
[PL](#pl-version)

This was a fun task. We were given a source code of an unknown programming language.
We assumed it would print out the flag. First observation we made, was that number 
of `@*`, `@**` and `@***` instructions was about right for the flag, and ther distribution among
code was about uniform - so we assumed those were print statements. This is start of code:
```
## 
%% 
%++ 
%++ 
%++ 
%# 
*&* 
@** 
%# 
**&* 
***-* 
***-* 
%++ 
%++ 
@*** 
```
This code should print out `IW`. After trying many things, we noticed that I is 9th letter of
alphabet, which is `3*3` - and 3 is the number of `@++` instructions, so `*&*` was likely
multiplication. We also guessed that `*`, `**` and `***` refer to distinct "registers" of
machine. Since the first print statement prints from the second register, something had to be
put there - after some trial and error, we concluded that `%#` is something like "move current
write pointer to the next register". We wrote interpreter up to this part, at which point we got
stuck. After some time, admin hinted on IRC, that this is a real language. Looking it up on 
esolang website, we found out it is `TapeBagel`. After finishing up the interpreter, we got flag.

###PL version

To byłe ciekawe zadanie - dostaliśmy plik z kodem w nizenanym języku programowania. Naturalnie 
założyliśmy, że wypisuje on flagę. Patrząc na liczbę instrukcji z `@`, domyśliliśmy się, że
są to instrukcje wypisania. Początek kodu:
```
## 
%% 
%++ 
%++ 
%++ 
%# 
*&* 
@** 
%# 
**&* 
***-* 
***-* 
%++ 
%++ 
@*** 
```
Ten kod powinien zatem wypisywać `IW`. Po dłuższej chwili zauważyliśmy, że I jest dziewiątą literą 
alfabetu, a `9=3*3`, przy czym 3 to ilość instrukcji `%++`, które zapewne zwiększają jakąś liczbę.
Zatem `*&*` zapewne mnoży liczbę `*` przez samą siebie. Później wpadliśmy na to, że `*`, `**`,
 `***` to zapewne kolejne rejestry maszyny. Ponieważ `@**` wypisuje dopiero drugi rejestr, coś
musiało być do niego wcześniej włożone. W ten sposób wymyślilismy, że `%#` to "zwiększanie
wskaźnika". Napisaliśmy interpreter uwzględniający znane już nam instrukcje, nie mogliśmy
wypisać nic więcej niż `IW ILOV`. Po jakimś czasie admin napisał na IRCu, że to prawdziwy język.
Poszukalismy więc na stronie esolang tegoż, i znaleźliśmy - jest to `TapeBagel`. Dokończywszy
interpreter, dostaliśmy flagę.
