## We lost the Fashion Flag! (Forensics, 100p)

    In Sharif CTF we have lots of task ready to use, so we stored their data about author or creation date and other related information in some files. But one of our staff used a method to store data efficiently and left the group some days ago. So if you want the flag for this task, you have to find it yourself!

    Download fashion.tar.gz

###ENG
[PL](#pl-version)

In this task we had a bunch of unknown files and one `fashion.model`. Looking at hexdump of it, we see string "FemtoZIP".
It turns out it's name of a compression program. Downloading it and decompressing the files, we have a couple thousand
of files with contents like:
```
{'category': 'reverse', 'author': 'staff_4', 'challenge': 'Fashion', 'flag': 'SharifCTF{b262389c6b7a6b5f112547d5394079db}', 'ctf': 'Shairf CTF', 'points': 300, 'year': 2014}
```
Every file had different flag. However, we could grep  all the files for correct year, category etc. using command:

`for f in `ls`; do cat $f | grep "'points': 100" | grep "'category': 'forensic'" | grep "'year': 2016"; done`

This gives us only five results, first one of which is correct.

###PL version

W tym zadaniu dostaliśmy sporo nieznanych plików i jeden `fashion.model`. Hexdump z niego zawiera tekst "FemtoZIP".
Okazuje się, że to program do kompresji danych. Pobierając go i odpalając, otrzymujemy kilka tysięcy plików z 
zawartością w stylu:
```
{'category': 'reverse', 'author': 'staff_4', 'challenge': 'Fashion', 'flag': 'SharifCTF{b262389c6b7a6b5f112547d5394079db}', 'ctf': 'Shairf CTF', 'points': 300, 'year': 2014}
```
Każdy plik zawierał jednakże inną flagę. Ale od czego jest grep! Użyliśmy go do odfiltrowania zawartości ze śmieci:

`for f in `ls`; do cat $f | grep "'points': 100" | grep "'category': 'forensic'" | grep "'year': 2016"; done`

W tym momencie zostało już tylko pięć flag, jedna z których jest poprawna.
