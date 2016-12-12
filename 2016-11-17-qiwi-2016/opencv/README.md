# OpenCV (ppc 200)

###ENG
[PL](#pl-version)

In the task we get an OpenCV cascade classifier and a lot of images in a [package](task.zip).
Each of the images has a small hashcode embedded.
The goal is to see which of the pictures gets selected by OpenCV.
We simply loaded the classifier and run:

```python
import os
import cv2


def main():
    cascade = cv2.CascadeClassifier('/tmp/task/any.xml')
    basedir = "/tmp/task/images"
    for filename in os.listdir(basedir):
        img = cv2.imread(basedir + "/" + filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        flags = cascade.detectMultiScale(gray, 1.3, 5)
        if len(flags) > 0:
            print(filename)
            for (x, y, w, h) in flags:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imshow('img', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


main()
```

And we got image 240.bmp with `FWqM5vfOKvY0T8t3ho6L`

###PL version

W zadaniu dostajemy klasyfikator OpenCV i sporo obrazków w [paczce](task.zip).
Każdy obrazek zawiera hashcode.
Celem jest znalezienie obrazka wybranego przez OpenCV.
Po prostu uruchomiliśmy klasyfikator:

```python
import os
import cv2


def main():
    cascade = cv2.CascadeClassifier('/tmp/task/any.xml')
    basedir = "/tmp/task/images"
    for filename in os.listdir(basedir):
        img = cv2.imread(basedir + "/" + filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        flags = cascade.detectMultiScale(gray, 1.3, 5)
        if len(flags) > 0:
            print(filename)
            for (x, y, w, h) in flags:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imshow('img', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


main()
```

Co wskazało 240.bmp z `FWqM5vfOKvY0T8t3ho6L`
