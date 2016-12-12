# Datetime (ppc 100)

###ENG
[PL](#pl-version)

In the task we a lot of [messages](messages.zip).
Each message has a timestamp in the format `Friday_1_April_2015` and contains some random hash value.
The flag is one of those hashes and we have to find the right one.
The point is to find the message with correct timestamp - where day of the week matches the designated date.
We do this with a simple python script and datetime library:

```
import codecs
import os
import datetime


def main():
    basedir = "/tmp/messages"
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    months = ["", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
              "november", "december"]
    for filename in os.listdir(basedir):
        x = filename.split("_")
        dayname = x[0]
        dayno = x[1]
        month = months.index(x[2].lower())
        year = x[3][:-4]
        date = datetime.datetime(int(year), int(month), int(dayno))
        if date.weekday() == days.index(dayname.lower()):
            print(filename)
            with codecs.open(basedir + "/" + filename, "r") as input_file:
                data = input_file.read()
                print(data)


main()
```

Which gives us:

```
Tuesday_15_June_1982.txt
4eec2cd9e4bb0062d0e41c8af1bd8a0f
```


###PL version

W zadaniu dostajemy dużo [wiadomości](messages.zip).
Każda wiadomość ma znacznik czasu w postaci `Friday_1_April_2015` i zawiera losowy hashcode.
Flaga jest jednym z tych hashy i musimy znaleźć odpowiedni.
Idea zadania jest dość prosta - tylko jeden znacznik czasowy jest poprawny, tzn dzień tygodnia zgadza się z datą.
Poprawny plik odnajdujemy za pomocą skryptu i biblioteki datetime:

```
import codecs
import os
import datetime


def main():
    basedir = "/tmp/messages"
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    months = ["", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
              "november", "december"]
    for filename in os.listdir(basedir):
        x = filename.split("_")
        dayname = x[0]
        dayno = x[1]
        month = months.index(x[2].lower())
        year = x[3][:-4]
        date = datetime.datetime(int(year), int(month), int(dayno))
        if date.weekday() == days.index(dayname.lower()):
            print(filename)
            with codecs.open(basedir + "/" + filename, "r") as input_file:
                data = input_file.read()
                print(data)


main()
```

Co daje nam:

```
Tuesday_15_June_1982.txt
4eec2cd9e4bb0062d0e41c8af1bd8a0f
```
