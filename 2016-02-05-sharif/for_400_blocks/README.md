## Blocks (Forensics, 400p)

    I recovered as much data as I could. Can you recover the flag?

    Download data3

###ENG
[PL](#pl-version)

Let's look at hexdump of the file. It contains some SQL-like text:
```
00000220  00 00 00 81 14 04 07 17  15 15 01 82 0b 74 61 62  |.............tab|
00000230  6c 65 64 61 74 61 64 61  74 61 05 43 52 45 41 54  |ledatadata.CREAT|
00000240  45 20 54 41 42 4c 45 20  22 64 61 74 61 22 20 28  |E TABLE "data" (|
00000250  0a 09 60 49 44 60 09 49  4e 54 45 47 45 52 20 4e  |..`ID`.INTEGER N|
00000260  4f 54 20 4e 55 4c 4c 20  50 52 49 4d 41 52 59 20  |OT NULL PRIMARY |
```
It looks like database dump, but sqlite3 doesn't want to work with it. After investigation, it seems that file magic is
missing. Patching the file allows us to work with the database. Let's look at contents:
```
SQLite version 3.8.11.1 2015-07-29 20:00:57
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
sqlite> .open dat
sqlite> .tables
category  data    
sqlite> .schema category
CREATE TABLE `category` (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`Cat`	TEXT NOT NULL
);
sqlite> SELECT * FROM category;
1|CHRM
2|IDAT
3|ICCP
4|IHDR
5|TEXT
6|TIME
7|PLTE
8|TRNS
sqlite> .schema data
CREATE TABLE "data" (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`Data`	BLOB NOT NULL,
	`Cat`	INTEGER NOT NULL
);
sqlite> SELECT ID, Cat FROM data;
1|2
2|2
3|2
4|2
5|2
6|7
7|4
8|2
9|2
10|2
11|2
12|8
13|2
14|2
```
It seems like a PNG file was saved in the database. Unfortunately the chunks are in parts - the most important, IDAT
chunk is in 11 parts. Concatenating them in the most obvious order doesn't work, so we had to bruteforce it - after
all it's only `11!` or `39,916,800` combinations. Using `getblobs.sh`, `doit.py` and `to_image.py` in this order, we
were able to get image, containing flag.

###PL version

Obejrzyjmy hexdump pliku. Zawiera tekst podobny do SQLa:
```
00000220  00 00 00 81 14 04 07 17  15 15 01 82 0b 74 61 62  |.............tab|
00000230  6c 65 64 61 74 61 64 61  74 61 05 43 52 45 41 54  |ledatadata.CREAT|
00000240  45 20 54 41 42 4c 45 20  22 64 61 74 61 22 20 28  |E TABLE "data" (|
00000250  0a 09 60 49 44 60 09 49  4e 54 45 47 45 52 20 4e  |..`ID`.INTEGER N|
00000260  4f 54 20 4e 55 4c 4c 20  50 52 49 4d 41 52 59 20  |OT NULL PRIMARY |
```
Wygląda to na zserializowaną bazę danych, ale sqlite3 nie chce z nią pracować. Okazuje się, że brakuje magii w pliku.
Po spatchowaniu danych, możemy pracować. Spójrzmy na zawartość:
```
SQLite version 3.8.11.1 2015-07-29 20:00:57
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
sqlite> .open dat
sqlite> .tables
category  data    
sqlite> .schema category
CREATE TABLE `category` (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`Cat`	TEXT NOT NULL
);
sqlite> SELECT * FROM category;
1|CHRM
2|IDAT
3|ICCP
4|IHDR
5|TEXT
6|TIME
7|PLTE
8|TRNS
sqlite> .schema data
CREATE TABLE "data" (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`Data`	BLOB NOT NULL,
	`Cat`	INTEGER NOT NULL
);
sqlite> SELECT ID, Cat FROM data;
1|2
2|2
3|2
4|2
5|2
6|7
7|4
8|2
9|2
10|2
11|2
12|8
13|2
14|2
```
Wygląda na to, że ukryto w bazie plik PNG. Niestety chunki są w kawałkach - w szczególności, chunk IDAT jest w 11 
częściach. Połączenie ich w oczywisty sposób nie działa, więc kolejność musieliśmy wybrutować - to ostatecznie tylko
`11!`, czyli `39,916,800` kombinacji. Odpalając `getblobs.sh`, `doit.py` oraz `to_image.py` w tej kolejności, po
parunastu minutach brutowania dostaliśmy obrazek z flagą.
