## Android (Reverse, 100p)

> Find the Flag!!
> [Download](Sharif_CTF.apk)

###ENG
[PL](#pl-version)

We download android application given to us by challenge creators.
First think we do is packing it into java decompiler (http://www.javadecompilers.com/apk).

Most of code is boring and uninteresting, but one of functions is clearly more interesting:

```java
public void onClick(View view) {
    String str = new String(" ");
    str = this.f5a.f1b.getText().toString();
    Log.v("EditText", this.f5a.f1b.getText().toString());
    String str2 = new String("");
    int processObjectArrayFromNative = this.f5a.processObjectArrayFromNative(str);
    int IsCorrect = this.f5a.IsCorrect(str);
    str = new StringBuilder(String.valueOf(this.f5a.f3d + processObjectArrayFromNative)).append(" ").toString();
    try {
        MessageDigest instance = MessageDigest.getInstance("MD5");
        instance.update(str.getBytes());
        byte[] digest = instance.digest();
        StringBuffer stringBuffer = new StringBuffer();
        for (byte b : digest) {
            stringBuffer.append(Integer.toString((b & 255) + 256, 16).substring(1));
        }
        if (IsCorrect == 1 && this.f5a.f4e != "unknown") {
            this.f5a.f2c.setText("Sharif_CTF(" + stringBuffer.toString() + ")");
        }
        if (IsCorrect == 1 && this.f5a.f4e == "unknown") {
            this.f5a.f2c.setText("Just keep Trying :-)");
        }
        if (IsCorrect == 0) {
            this.f5a.f2c.setText("Just keep Trying :-)");
        }
    } catch (NoSuchAlgorithmException e) {
        e.printStackTrace();
    }
}
```

As you can see, this function gets text from button and uses "IsCorrect" method to check input validity. If input is valid, flag is given to the user.

Fortunately, IsCorrect is native function, so we have to disassemble ARM library to get our hands on the flag.

[libadnjni.so](libadnjni.so)

Function IsCorrect is very long, but most of it is not important. In fact, everything it does is calling strcmp on constant input.
To be precise, input from user is compared to hardcoded string 'ef57f3fe3cf603c03890ee588878c0ec'.

It's enough to enter this string into application as password and we get the flag.

###PL version

Pobieramy androidową aplikację którą dają nam twórcy zadania. Pierwsze co robimy, to pakujemy ją do dekompilera javy (http://www.javadecompilers.com/apk).

Wiekszość kodu to jak zwykle śmieci, ale znajdujemy jedną ciekawą funkcję:

```java
public void onClick(View view) {
    String str = new String(" ");
    str = this.f5a.f1b.getText().toString();
    Log.v("EditText", this.f5a.f1b.getText().toString());
    String str2 = new String("");
    int processObjectArrayFromNative = this.f5a.processObjectArrayFromNative(str);
    int IsCorrect = this.f5a.IsCorrect(str);
    str = new StringBuilder(String.valueOf(this.f5a.f3d + processObjectArrayFromNative)).append(" ").toString();
    try {
        MessageDigest instance = MessageDigest.getInstance("MD5");
        instance.update(str.getBytes());
        byte[] digest = instance.digest();
        StringBuffer stringBuffer = new StringBuffer();
        for (byte b : digest) {
            stringBuffer.append(Integer.toString((b & 255) + 256, 16).substring(1));
        }
        if (IsCorrect == 1 && this.f5a.f4e != "unknown") {
            this.f5a.f2c.setText("Sharif_CTF(" + stringBuffer.toString() + ")");
        }
        if (IsCorrect == 1 && this.f5a.f4e == "unknown") {
            this.f5a.f2c.setText("Just keep Trying :-)");
        }
        if (IsCorrect == 0) {
            this.f5a.f2c.setText("Just keep Trying :-)");
        }
    } catch (NoSuchAlgorithmException e) {
        e.printStackTrace();
    }
}
```

Jak widać, jest jest na czymś wywoływana funkcja IsCorrect, i jeśli wywołanie zakończy sie sukcesem, flaga jest przekazywana użytkownikowi.

Niestety (albo na szczęście), IsCorrect jest funkcją natywną, więc żeby ją przeanalizować musimy disasemblować ARMową bibliotekę

[libadnjni.so](libadnjni.so)

Funkcja IsCorrect zawiera bardzo dużo kodu, ale większośc jest niepotrzebna. Tak naprawdę wywołuje tylko strcmp ze stałym napisem.
Konkretnie input użytkownika jest porównywany z 'ef57f3fe3cf603c03890ee588878c0ec'.

Wystarczy wprowadzić tą wartość w aplikacji androidowej, i dostajemy flagę. 100 punktów do przodu.
