##Trivia 2 (Trivia/Recon, 200p)

	I love this song. What is my project ID?

###PL
[ENG](#eng-version)

Dostajemy plik mp3 (nie udostępnimy go bo był piracki...) oraz informacje, że flagą jest `project ID`.
W pliku mp3 trafiamy na dość nietypowy dobór zdjęcia ustawionego jako okładka albumu.
Po wyszukaniu tego zdjęcia przez tineye.com i google reverse image search trafiamy na githuba: https://github.com/UziTech którego właściciel ma to samo zdjecie w avatarze.

Następnie spędziliśmy bardzo (!) dużo czasu testując różne możliwości dla flagi - nazwy projektów z githuba, ID projektów pobrane przez API i wiele innych możliwości.

W końcu przeszukując zawartość plików w repozytorium w poszukiwaniu `project` oraz `id` trafiliśmy między innymi na plik:

https://github.com/UziTech/NSF2SQL/blob/master/NSF2SQL/NSF2SQL.csproj

a flagą okazało się pole `<ProjectGuid>` czyli `3AD3A009-FC65-4067-BFF1-6CE1378BA75A`

###ENG version

We get mp3 file (not included since it was pirated...) and information that the flag is `project ID`.
Inside the mp3 file we find a strange picture set as album cover.
We look for the picture with tineye.com and google reverse image search and we find github: https://github.com/UziTech whose owner has the same picture in avatar.

Next we spend a lot (!) of time trying to figure out what could be the flag - project names, project IDs taken from API, and many many more strange ideas.

Finally while looking for `project` and `id` inside the files in repository we found the file:

https://github.com/UziTech/NSF2SQL/blob/master/NSF2SQL/NSF2SQL.csproj

and the flag turned out to be the value of `<ProjectGuid>` so `3AD3A009-FC65-4067-BFF1-6CE1378BA75A`
