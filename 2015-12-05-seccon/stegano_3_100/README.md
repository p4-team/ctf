##Steganography 3 (Stegano, 100p)

```
We can get desktop capture!
Read the secret message.
```

###PL
[ENG](#eng-version)

Dostajemy obraz:

![](desktop_capture.png)

Na podstawie którego chcemy uzyskać flagę. Pierwszym krokiem jest odtworzenie binarki otwartej w hexedytorze. Zrobiliśmy to za pomocą OCRa a następnie ręcznego poprawiania błędów. Wynikiem jest program [elf](elf.bin).
Uruchomienie go daje w wyniku wiadomość `Flood fill` zakodowaną jako base64. Po pewnym czasie wpadliśmy wreszcie na rozwiązanie, które polegało na użyciu "wypłeniania kolorem" na początkowym obrazie:

![](floodfill.png)

co daje nam flage:

`SECCON{the_hidden_message_ever}`

### ENG version

We get a picture:

![](desktop_capture.png)

And we want to get a flag based on this. First step is to recreate the binary open in hexeditor. We used OCR and then fixed defects by hand. This way we got [elf binary](elf.bin).
Running it give a message `Flood fill` encoded as base64. After a while we finally figured the solution, which was to use "flood fill" on the initial picture:

![](floodfill.png)

which gives us a flag:

`SECCON{the_hidden_message_ever}`