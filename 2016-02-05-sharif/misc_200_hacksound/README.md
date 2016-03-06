## Hack By The Sound (Misc, 200p)

    A well known blogger has came to a hotel that we had good relationships with its staffs. We tried to capture the sound of his room by placing a microphone inside the desk.

    We have recorded the sound about the time that he has typed a text in his blogg. You could find the text he typed in "Blog Text.txt".
    
    We reduce noises somehow and found that many characters may have the same keysound. Also we know that he use meaningful username and password.
    
    Could you extract the username and password of his blog?
    
    flag is concatenation of his username and password as usernamepassword.
    
    Download sound.tar.gz

###ENG
[PL](#pl-version)

The attached .wav file had no sound loud enough for our ears, but amplifying it using Audacity we were able to notice
that it was sound of a person typing. Words were pretty noticeable - space always meant that typing stops for a split
second. By ear, all the key sounds were identical though.

However, we checked out Audacity's wave representation of keys and overlaid some of them in GIMP. Here is the result:
![](http://i.imgur.com/royrw1X.png)

The first image is two "S" sounds overlaid - there were almost no changes. The second one - "O" and "I" - had minor
differences, and the last one - "N" and "A" - showed noticeable changes. Apparently, the further the keys are on the
keyboard, the more differences they have. 

The task now was obvious, but still hard. In the end, we did the following:
- read raw data from the wav
- found the sound peaks, corresponding to individual key presses
- cut about 0.05s worth of sound around each peak
- repair blog text - there were some extra characters in a couple of places, which made keysound-to-character
  correspondence wrong
- for each unknown keypress, iterate over known keypresses and try to find best fit

Unfortunately, some characters had the same sound, so we were unable to find the password in plaintext - instead, we
got a range of characters for each position:

```
[] [] [ced] [frv] [ced] [ikl] [hny] [sw] [bgt] [ced] [il] [hny] [,.] [ced] [op] [mu] [] [
] [ ] [
] [ ] [] [a] [ced] [jmu] [ikl] [hny] [] [-sw] [op] [jmu] [ced] [bgt] [hny] [ikl] [hny] [bgt] [] [
] [ ] [
] [ ] [] 
```
The first word was probably website (look at the end - ".com"), so we were not interested in that. The remaining
two words were somewhat challenging to guess, but eventually we found them: `admin` and `something`. Concatenated
togather, they were the flag.

###PL version

Załączony plik .wav był zbyt cichy, żeby cokolwiek usłyszec, ale wzmacniając go przy użyciu Audacity, zauważyliśmy, że
było to nagranie osoby piszącej na klawiaturze. Słowa były rozróżnialne - spacja była znacznie dłuższym dźwiękiem od
pozostałych klawiszy. Te niestety były dla ludzkiego ucha nierozróżnialne.

Sprawdziliśmy jednak reprezentację tych dźwięków w Audacity i nałożyliśmy niektóre z nich na siebie w GIMPie. Rezultat:
![](http://i.imgur.com/royrw1X.png)

Pierwszy obrazek, to dwa dźwięki "S" nałożone na siebie - wyglądają jak jedna fala. Drugi - to "O" i "I" - miał niewielkie,
pikselowe wręcz różnice. Ostatni zaś - "N" i "A" - ujawnił znaczące różnice w dźwiękach. Najwyraźniej im dalej klawisze
się od siebie znajdują na klawiaturze, tym większa jest różnica w ich dźwiękach.

W tym momencie doskonale wiedzieliśmy, o co chodzi w zadaniu - należy dopasować nieznane dźwięki z początku do znanych
z końca nagrania. Łatwo powiedzieć, trudniej zrobić. Ostatecznie, zrobiliśmy to następująco:
- wczytalliśmy surowe dane z pliku i je sparsowaliśmy
- znaleźliśmy górki odpowiadające uderzeniom klawisza
- wycięliśmy około 0.05-sekundowe kawałki wokół każdej górki
- naprawiliśmy podany tekst z bloga - niektóre litery pojawiły się w tekście, ale nie w dźwięku, co psuło dopasowywanie
- dla każdego nieznanego dźwięku, znajdowaliśmy znany o najlepszym dopasowaniu

W praktyce jednak, musliśmy poprzestać na kilku możliwościach dla każdego uderzenia - niektóre klawisze miały bowiem
identyczny dźwięk, co inne, nie pozwalając tym samym na jednoznaczny odczyt. Wynik działania programu:
```
[] [] [ced] [frv] [ced] [ikl] [hny] [sw] [bgt] [ced] [il] [hny] [,.] [ced] [op] [mu] [] [
] [ ] [
] [ ] [] [a] [ced] [jmu] [ikl] [hny] [] [-sw] [op] [jmu] [ced] [bgt] [hny] [ikl] [hny] [bgt] [] [
] [ ] [
] [ ] [] 
```
Pierwsze słowo to prawdopodobnie nazwa strony internetowej (świadczy o tym końcówka ".com"), więc nie jesteśmy tym
fragmentem zainteresowani. Pozostałe dwa słowa to login i hasło - po dłuższej chwili, zauważyliśmy, że pasują do
nich słowa: `admin` i `something`. Połączone razem, były one flagą.
