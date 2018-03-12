# Welcome to droid (Re, 635p, 24 solved)

[PL](#pl-version)

In the task we get [android application](droid.apk) to work with.
Once we reverse the sources, it seems we need to pass some checks to reach the flag.
However one of the checks is:

```java
public String m4832k() {
	char[] cArr = new char[]{'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'};
	StringBuffer stringBuffer = new StringBuffer();
	Random random = new Random();
	for (int i = 0; i < 20; i++) {
		stringBuffer.append(cArr[random.nextInt(cArr.length)]);
	}
	return stringBuffer.toString();
}
```

And sice it's using random values, it's very unlikely we can pass it.
We could try to patch the code, but it's a lot of fuss.
If we could pass all the checks the code that shows the flag is:

```java
this.f3092l = (EditText) findViewById(R.id.editText);
this.f3092l.setText(stringFromJNI());
```

So it calls a single function from the native library shipped with the app.
The function is pretty much unreversable, way to complex, but we don't need that.
We can simply load this library and call the function, without all silly checks!

In order to do that we create a new android project (we actually used NDK example) with Android Studio, create a new Activity, but keeping all the names and packages the same, and write code:

```java
package com.example.puing.a2018codegate;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

import java.util.logging.Logger;

public class Main4Activity extends AppCompatActivity {
    static {
        System.loadLibrary("hello-libs");
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        TextView tv = new TextView(this);
        String flagString = stringFromJNI();
        tv.setText(flagString);
        setContentView(tv);
        Logger.getLogger("flagLogger").info(flagString);
    }

    public native String stringFromJNI();
}
```

We modify the build.gradle for libs to include our .so files:

```
sourceSets {
	main {
		// let gradle pack the shared library into apk
		jniLibs.srcDirs = ['../distribution/gperf/lib', '../distribution/droid/lib']
	}
}
```

And we're good to go.
We can just run the app and get:

![](flag.png)

So the flag is: `FLAG{W3_w3r3_Back_70_$3v3n7een!!!}`

### PL version

W zadaniu dostajemy [aplikację androidową](droid.apk).
Po zdekompilowaniu i analizie źródeł widać, że musimy przejść kilka testów żeby dostać flagę.
Niestety jeden z nich to:

```java
public String m4832k() {
	char[] cArr = new char[]{'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'};
	StringBuffer stringBuffer = new StringBuffer();
	Random random = new Random();
	for (int i = 0; i < 20; i++) {
		stringBuffer.append(cArr[random.nextInt(cArr.length)]);
	}
	return stringBuffer.toString();
}
```

A skoro używa losowych wartości to jest mała szansa że uda się go przejść.
Moglibyśmy spróbować patchować ten kod, ale to dużo roboty.
Gdybyśmy przeszli testy to za wyświetlenie flagi odpowiada:

```java
this.f3092l = (EditText) findViewById(R.id.editText);
this.f3092l.setText(stringFromJNI());
```

Więc wołana jest jedna funkcja z natywnej biblioteki dostarczonej z aplikacją.
Sama funkcja jest praktycznie nie do zreversowania, zbyt skomplikowana, ale nie musimy tego robić.
Możemy po prostu załadować sobie tą bibliotekę i wywołać funkcje, bez żadnych testów!

Żeby to zrobić stworzyliśmy nowy projekt androidowy (użyliśmy jako szablonu przykładowego kodu z NDK) w Android Studio, stworzyliśmy własne Activity, pozostawiając takie same nazwy klas i pakietów i napisaliśmy kod:

```java
package com.example.puing.a2018codegate;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

import java.util.logging.Logger;

public class Main4Activity extends AppCompatActivity {
    static {
        System.loadLibrary("hello-libs");
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        TextView tv = new TextView(this);
        String flagString = stringFromJNI();
        tv.setText(flagString);
        setContentView(tv);
        Logger.getLogger("flagLogger").info(flagString);
    }

    public native String stringFromJNI();
}
```

Musieliśmy też zmodyfikować build.gradle dla bibliotek, żeby uwzględnić nasze pliki .so:

```
sourceSets {
	main {
		// let gradle pack the shared library into apk
		jniLibs.srcDirs = ['../distribution/gperf/lib', '../distribution/droid/lib']
	}
}
```

I pozostało już tylko uruchomić aplikację i dostać:

![](flag.png)

Więc flaga to `FLAG{W3_w3r3_Back_70_$3v3n7een!!!}`
