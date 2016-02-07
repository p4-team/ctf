## Asian Cheetah (Misc, 50p)

    We have hidden a message in png file using jar file. Flag is hidden message. Flag is in this format:

    SharifCTF{flag}

    Download cheetah.tar.gz

###ENG
[PL](#pl-version)

In this task we had an image and a Java program used to hide flag in it. Decompiling the program allows us to notice
that least significant bits are used to hide the message. We can easliy get the flag using the following script:
```
from PIL import Image

im=Image.open("AsianCheetah1.png")
l=list(im.getdata())
b=[]
for x in l:
    b.append(x[2]&1)

s=[]
for i in range(100):
    c=0
    for j in range(8):
        c*=2
        c+=b[i*8+j]
    s.append(chr(c))
print repr("".join(s))
```

###PL version

W zadaniu dostaliśmy obrazek i program w Javie, którego użyto do ukrycia w nim flagi. Dekompilacja programu pozwala
nam dostrzec fakt użycia najmłodszych bitów do zakodowania wiadomości. Flagę możemy otrzymać używając tego skryptu:
```
from PIL import Image

im=Image.open("AsianCheetah1.png")
l=list(im.getdata())
b=[]
for x in l:
    b.append(x[2]&1)

s=[]
for i in range(100):
    c=0
    for j in range(8):
        c*=2
        c+=b[i*8+j]
    s.append(chr(c))
print repr("".join(s))
```
