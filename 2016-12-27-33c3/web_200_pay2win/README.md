# Pay2Win (web 200)

###ENG
[PL](#pl-version)

In the task we have a webpage where we can purchase some cheap object and a flag.
Flag is much more expensive.
Once we click on the item to purchase we can see a page with details and we have to put credit card number to confirm the purchase.

We notice instantly that the webpage with item details has the same URL, with different long hash-looking value.
After fiddling with this we figure it's a 8-bytes block encryption ECB ciphertext.
This means we can split and combine blocks in different order to get some funny results.
This way we can "assemble" items with strange names and strange prices.

After that we tried actually buying an item.
We can't buy the flag with some fake credit card number, but we can buy the other item.
And the purchase results webpage has exactly the same layout at item details - again there is one URL and the same looking ECB ciphertext.

So we fiddle again and see what we can assemble from the correct confirmation and the incorrect confirmation.

And we combine the valid cheap confirmation:

```
5765679f0870f430
9b1a3c83588024d7
c146a4104cf9d2c8
d3d78d0842397676
28df361f896eb3c3
706cda0474915040
```

With invalid flag confirmation:

```
232c66210158dfb2
3a2eda5cc945a0a9
650c1ed0fa0a08f6
a7ef23b6d345dd42
f1380b66410fa383
2f7ef761e2bbe791
```

To get the valid flag confirmation:

```
5765679f0870f430
9b1a3c83588024d7
650c1ed0fa0a08f6
a7ef23b6d345dd42
f1380b66410fa383
2f7ef761e2bbe791
```

And the flag: `33C3_3c81d6357a9099a7c091d6c7d71343075e7f8a46d55c593f0ade8f51ac8ae1a8`


###PL version

W zadaniu dostajemy stronę internetową na której można kupić jakiś tani obiekt oraz flagę.
Flaga jest dużo droższa.
Kiedy klikniemy na wybrany obiekt dostajemy stronę ze szczegółami obiektu oraz miejsce na podanie numeru karty kredytowej.

Zauważyliśmy szybko, że strona ze szczegółami ma ten sam URL oraz długi parametr wyglądający jak hash.
Po zabawie z tym parametrem doszliśmy do wniosku że to dane szyfrowane 8-bajtowym szyfrem blokowym w trybie ECB.
To oznacza że możemy mieszać bloki i składać z nich nowe szyfrogramy, uzyskując ciekawe rezultaty jak dziwne nazwy oraz ceny.

Następnie spróbowaliśmy kupić coś.
Nie mogliśmy kupić flagi bo strona twierdziła że nasz fałszywy numer karty kredytowej przekroczył limit, ale mogliśmy kupic drugi obiekt.
Po kupieniu przenosimy się na stronę ze szczegółami kupna, która wygląda bardzo podobnie - znowu jest tam jeden URL i szyfrogram.

Ponownie postanowiliśmy pobawić się w mieszanie bloków, tym razem z szyfrogramu z nieudaną próbą kupna flagi oraz z udanym kupnem innego obiektu.

Finalnie łączymy udane kupno:

```
5765679f0870f430
9b1a3c83588024d7
c146a4104cf9d2c8
d3d78d0842397676
28df361f896eb3c3
706cda0474915040
```

Z nieudanym kupnem flagi:

```
232c66210158dfb2
3a2eda5cc945a0a9
650c1ed0fa0a08f6
a7ef23b6d345dd42
f1380b66410fa383
2f7ef761e2bbe791
```

Dostając udane kupno flagi:

```
5765679f0870f430
9b1a3c83588024d7
650c1ed0fa0a08f6
a7ef23b6d345dd42
f1380b66410fa383
2f7ef761e2bbe791
```

I samą flagę: `33C3_3c81d6357a9099a7c091d6c7d71343075e7f8a46d55c593f0ade8f51ac8ae1a8`
