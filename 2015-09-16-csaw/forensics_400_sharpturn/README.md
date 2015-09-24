## sharpturn (forensics, 400p, 110 solves)

> I think my SATA controller is dying.
> 
> sharpturn.tar.xz-46753a684d909244e7d916cfb5271a95

### PL Version
`for ENG version scroll down`

Dostajemy zip z czymś co może być tylko zawartością folderu `.git`. Wypakowywujemy więc sobie z niego dane (zrobiliśmy to za pomocą pythona, import zlib i zlib.decompress, ale po zastanowieniu w sumie wystarczyłby pewnie git checkout ;) ).

Po chwili zauważamy że coś się nie zgadza - hash pliku sharp.cpp jest inny niż powinien. Patrzymy więc na rewizje po kolei - [rewizja pierwsza](sharp_v1_efda_efda) ma dobry hash. [Rewizja druga](sharp_v2_354e_8675)... już nie. Napisaliśmy więc [sprytny skrypt w pythonie](flipuj.py), flipujący losowe bity (domyślamy się że o to chodzi, skoro w treści zadania jest coś o umierającym kontrolerze SATA) i próbujący odkryć te które sie nie zgadzają.

W ten sposób dochodzimy do [poprawnej wersji rewizji drugiej](sharp_v2_354e_354e). Niestety hash [rewizji trzeciej](sharp_v3_d961_7564) również się nie zgadza, ale poprawiamy i jego naszym bitflipperem i mamy [poprawną rewizję trzecią](sharp_v3_d961_7564). I to samo robimy przy czwartej - [plik ze złym hashem](sharp_v4_f8d0_8096) zamieniamy na [plik z dobrym hashem](sharp_v4_f8d0_f8d0).

W tym momencie mamy wszystko czego potrzebujemy - faktoryzujemy sobie jeszcze liczbę jak wymaga program, i idziemy:

    Part1: Enter flag:
    flag
    Part2: Input 31337:
    31337
    Part3: Watch this: https://www.youtube.com/watch?v=PBwAxmrE194
    ok
    Part4: C.R.E.A.M. Get da _____:
    money
    Part5: Input the two prime factors of the number 272031727027.
    31357 8675311
    flag{3b532e0a187006879d262141e16fa5f05f2e6752} 

(Warto zauważyć poczucie humoru autorów zadania, gdzie "enter flag" wymaga podania dosłownie "flag").

Flaga którą otrzymujemy jest przyjmowana przez system, więc jesteśmy kolejne 400 punktów do przodu.

### ENG Version

We get a zip file with something that can only be the contents of `.git` directory. We extract the data (we did this with python, import zlib and zlib.decompress, but most likely we could have simply used git checkout ;) ).

After a while we realise that something is wrong - hash of sharp.cpp file is incorrect. We check the sequence of revisions one by one - [first revision](sharp_v1_efda_efda) has a correct hash. [Second revision](sharp_v2_354e_8675)... does not. We wrote a [clever python script](flipuj.py) which flips random bits (we guess that this is the case, since the task decription mentions a broken SATA controller) and tries to figure out which are incorrect.

This was we finally get to [correct version of second revision](sharp_v2_354e_354e). Unfortunately, hash of the [third revision](sharp_v3_d961_7564) is also incorrect, but we fix it with our bitflipper and we get a [correct third revision](sharp_v3_d961_7564). We do the same with fourth revision - [file with incorrect hash](sharp_v4_f8d0_8096) we turn into [file with correct hash](sharp_v4_f8d0_f8d0).

Now we have almost everything we need - we also need to factor a given number, and we proceed:

    Part1: Enter flag:
    flag
    Part2: Input 31337:
    31337
    Part3: Watch this: https://www.youtube.com/watch?v=PBwAxmrE194
    ok
    Part4: C.R.E.A.M. Get da _____:
    money
    Part5: Input the two prime factors of the number 272031727027.
    31357 8675311
    flag{3b532e0a187006879d262141e16fa5f05f2e6752} 

(Author's sense of humour is worth noting here - we were supposed to put "flag" string as an answer for a prompt "enter flag").
The flag we get is accepted so we are 400 points up.
