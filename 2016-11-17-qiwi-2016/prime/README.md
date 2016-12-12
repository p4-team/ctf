# Prime (ppc 100)

###ENG
[PL](#pl-version)

In the task we get a lot of [files](encrypted.zip) with a large number as filename and a single byte as content.
The goal of this task is to extract contents from all files which have a prime number as name.
We do this with a simple script and gmpy2.is_prime():

```python
import codecs
import os
from gmpy2 import is_prime


def main():
    basedir = "/tmp/encrypted"
    result = ""
    for filename in os.listdir(basedir):
        if is_prime(int(filename)):
            with codecs.open(basedir + "/" + filename, "r") as input_file:
                data = input_file.read()[:-1]
                result += data
    print('result', result)


main()
```

Which gives the flag: `c93c0f30299130cde942fce8ec5dd0b3012dcfa478a4ab2314ee525098fb779e2812d6731d372bae6d71e220a6`

###PL version

W zadaniu dostajemy dużo [plików](encrypted.zip) z dużą liczbą jako nazwa pliku i jednym bajtem zawartości.
Celem jest pobranie zawartości ze wszystkich plików, których nazwa jest liczbą pierwszą.
Robimy to za pomocą skryptu i gmpy2.is_prime():

```python
import codecs
import os
from gmpy2 import is_prime


def main():
    basedir = "/tmp/encrypted"
    result = ""
    for filename in os.listdir(basedir):
        if is_prime(int(filename)):
            with codecs.open(basedir + "/" + filename, "r") as input_file:
                data = input_file.read()[:-1]
                result += data
    print('result', result)


main()
```

Co daje nam flage: `c93c0f30299130cde942fce8ec5dd0b3012dcfa478a4ab2314ee525098fb779e2812d6731d372bae6d71e220a6`
