# Woodstock (forensics)

###ENG
[PL](#pl-version)

In the task we get a [pcap](ws1_2.pcapng).
If we just run strings or search on it we can get the first flag `BITSCTF{such_s3cure_much_w0w}`.

The second flag is more complex to get here.
In the pcap we can see that there are 2 users interacting over some DC++/ADC hub and exchanging a `fl3g.txt` file.
After analysing the input file and reading on the ADC protocol we finally figured out that the file transfer part is actually missing from the pcap.
The only thing we can recover (eg. with binwalk, or by decoding zlib streams transferred) are file lists:

```xml
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<FileListing Version="1" CID="IW27TT3CMX5NKVCSVJ2CFJYSVUUC6CB43FF3XLA" Base="/" Generator="EiskaltDC++ 2.2.9">
<Directory Name="cadence">
</Directory>
<Directory Name="DSP">
</Directory>
<Directory Name="DC">
	<File Name="DEFCON 19 - The Art of Trolling (w speaker)-AHqGV5WjS4w.mp4" Size="98273830" TTH="KEVJ3EBNSE6XXLTPVCB5WUDMS5KR7P32MJQCGWY"/>
	<File Name="Fallen Kingdom - The Complete Minecraft Music Video Series-ayl3UXKpH1g.mp4" Size="511422768" TTH="M5PWQCU5AUV5L4A367BLGWWAYD5U3NUAVDTDQMI"/>
	<File Name="fl3g.txt" Size="14" TTH="CA4CMF34SHRUQIBG6MNRDAI5BVT7HQQRTGC7TBA"/>
	<File Name="Man punches a kangaroo in the face to rescue his dog (Original HD)-FIRT7lf8byw.mkv" Size="69864590" TTH="SOQ7ECDJ6YWM5F5Z3XLXGOFM6J23FOKNKWW5PXY"/>
	<File Name="poster.jpeg" Size="89139" TTH="IPLZJ2E4VJC4Q5X5NQ5D43COFAU3CGSZ5NQWJVA"/>
	<File Name="small2.jpg" Size="669170" TTH="K53V57ZPPJUOT5CAUP6DM3BAZI4YMUU536OYD3Q"/>
	<File Name="This Week in Stupid (04_12_2016)-m8LJl98_H60.mkv" Size="252235314" TTH="56UJJZ32LDK7V7QR5PZKPT7N2VOKPCY6WBZX3JA"/>
	<File Name="TRUMP UP THE JAMS! - The Fallout of the 2016 Election-jPLQh70GNrA.mkv" Size="274708751" TTH="YXPU6LCXAH5AY6I63KTJ4I3Q36YMZEXYEPGS6MQ"/>
	<File Name="when leftists attack - SJWs confront man over MAGA shirt-l4L-fk1dWhs.mp4" Size="122011301" TTH="B3W7EZGS2VMUG6B773WCQKPQ24G77R2EDDASJII"/>
</Directory>
</FileListing>
```

and 

```xml
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<FileListing Version="1" CID="AH3KWVYA5DAWJA7HAVHXC6BCLPNG34PVQVMPXPY" Base="/" Generator="EiskaltDC++ 2.2.9">
<Directory Name="dcpp">
	<File Name="text" Size="14" TTH="CA4CMF34SHRUQIBG6MNRDAI5BVT7HQQRTGC7TBA"/>
</Directory>
</FileListing>
```

We notice that the file size if 14 bytes, and we know that the flag contains `BITSCTF{}`, so in fact we're missing only 5 bytes.
Fortunately admin disclosed that there is a trailing `\n` in the file, so in fact we're missing only 4 bytes!
And we know the TTH hash of the flag file, so we can now brute-force the contents.

We had some issues with finding a proper code for this task, because different tools/libs were giving different hash results but we finally found a tool http://directory.fsf.org/wiki/Tthsum which seemed to do the trick.

We used ramdisk to create temp files with potential flags and tested if the resulting hashes match the hash we have.
After a while we finally got the flag `BITSCTF{sw3g}`

###PL version

W zadaniu dostajemy [pcapa](ws1_2.pcapng).
Jeśli tylko uruchomimy na nim strings albo wyszukiwarke to znajdujemy pierwszą flagę `BITSCTF{such_s3cure_much_w0w}`.

Druga flaga była trochę bardziej skomplikowana.
W pcapie mamy interakcje dwóch użytkowników za pomocą huba DC++/ADC i wymianę pliku `fl3g.txt`.
Po dogłębnej analizie pcapa i protokołu ADC doszliśmy do tego, że transferu pliku w pcapie nie ma.
Jedyne co możemy odzyskać to listy plików (np. przez binwalka lub dekodując transferowane strumienie zlib):

```xml
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<FileListing Version="1" CID="IW27TT3CMX5NKVCSVJ2CFJYSVUUC6CB43FF3XLA" Base="/" Generator="EiskaltDC++ 2.2.9">
<Directory Name="cadence">
</Directory>
<Directory Name="DSP">
</Directory>
<Directory Name="DC">
	<File Name="DEFCON 19 - The Art of Trolling (w speaker)-AHqGV5WjS4w.mp4" Size="98273830" TTH="KEVJ3EBNSE6XXLTPVCB5WUDMS5KR7P32MJQCGWY"/>
	<File Name="Fallen Kingdom - The Complete Minecraft Music Video Series-ayl3UXKpH1g.mp4" Size="511422768" TTH="M5PWQCU5AUV5L4A367BLGWWAYD5U3NUAVDTDQMI"/>
	<File Name="fl3g.txt" Size="14" TTH="CA4CMF34SHRUQIBG6MNRDAI5BVT7HQQRTGC7TBA"/>
	<File Name="Man punches a kangaroo in the face to rescue his dog (Original HD)-FIRT7lf8byw.mkv" Size="69864590" TTH="SOQ7ECDJ6YWM5F5Z3XLXGOFM6J23FOKNKWW5PXY"/>
	<File Name="poster.jpeg" Size="89139" TTH="IPLZJ2E4VJC4Q5X5NQ5D43COFAU3CGSZ5NQWJVA"/>
	<File Name="small2.jpg" Size="669170" TTH="K53V57ZPPJUOT5CAUP6DM3BAZI4YMUU536OYD3Q"/>
	<File Name="This Week in Stupid (04_12_2016)-m8LJl98_H60.mkv" Size="252235314" TTH="56UJJZ32LDK7V7QR5PZKPT7N2VOKPCY6WBZX3JA"/>
	<File Name="TRUMP UP THE JAMS! - The Fallout of the 2016 Election-jPLQh70GNrA.mkv" Size="274708751" TTH="YXPU6LCXAH5AY6I63KTJ4I3Q36YMZEXYEPGS6MQ"/>
	<File Name="when leftists attack - SJWs confront man over MAGA shirt-l4L-fk1dWhs.mp4" Size="122011301" TTH="B3W7EZGS2VMUG6B773WCQKPQ24G77R2EDDASJII"/>
</Directory>
</FileListing>
```

oraz

```xml
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<FileListing Version="1" CID="AH3KWVYA5DAWJA7HAVHXC6BCLPNG34PVQVMPXPY" Base="/" Generator="EiskaltDC++ 2.2.9">
<Directory Name="dcpp">
	<File Name="text" Size="14" TTH="CA4CMF34SHRUQIBG6MNRDAI5BVT7HQQRTGC7TBA"/>
</Directory>
</FileListing>
```

Możemy zauważyć że rozmiar pliku z flagą to 14 bajtów a wiemy że flaga zawiera `BITSCTF{}` więc brakuje nam jedynie 5 bajtów.
Szczęśliwie admin wspomniał że plik kończy się znakiem `\n` więc brakuje już tylko 4 bajtów!
A znamy hash pliku, więc możemy brutować jego zawartość.

Mieliśmy trochę problemów ze znalezieniem kodu do tego zadania ponieważ różne narzędzia/biblioteki dawały różne wyniki hasha. Koniec końcówk znaleźliśmy narzędzie http://directory.fsf.org/wiki/Tthsum które dawało dobre wyniki.

Użyliśmy ramdisku żeby tworzyć tymczasowe pliku z potencjalnymi flagami i testowaliśmy czy wynikowe hashe pasują do pliku z flagą i finalnie dostaliśmy `BITSCTF{sw3g}`
