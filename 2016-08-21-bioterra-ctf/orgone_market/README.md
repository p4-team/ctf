## Orgone Market (Web, 300p)

###ENG
[PL](#pl-version)

In the task we get a link to a webpage where we can buy some conspiracy-related objects for special orgone coins.
However we have 0 coins and those things cost!
There is a form on the page to claim free 300 coins, but this is not enough to buy anything on the page.

After poking around to check for some other possible vulnerabilities we figure that the intended solution is to use a timing attack / race condition and send multiple coin claim requests and thus getting multiple of the 300 free coins.
The first problem was the fact that there was a captcha to solve, however it was predictable and was changing every 1s.
The second problem that every failed attempt required registering new account.
So after we failed twice (apparently we had to send the requests in different sessions!) we checked again if maybe there is some easier way to get the flag.

And it turned out there was an unintended vulnerability - when we were sending request to buy an item we provided ID of the object to buy.
Apparently the script was then querying the price from database to check if we can afford it. 
However, if the ID we sent was missing in the DB there was no check to verify it, and the price was taken from returned NULL, which coerced to 0.
And we could afford to buy the non-existent item, getting the flag in return.

`flag{1m_s0rr4y_th4t_th3r3_1s_no_s3cr3t_4_U}`

###PL version

W zadaniu dostajemy link do strony internetowej gdzie możemy kupić przedmioty związane ze spiskową teorią dzieją za specjalna walutę orgone coins.
Niestety mamy 0 monet a wszystko kosztuje!
Na stronie jest formularz pozwalający nam uzyskać darmowe 300 monet, ale to nie wystarczy na kupno żadnego z przedmiotów.

Po upewnieniu się szybko czy nie ma na stronie żadnych innych oczywistych podatności uznaliśmy, że oczekiwane rozwiązanie to atak czasowy / race condition polegający na wysłaniu kilku requestów do pobrania darmowych monet i w ten sposób uzyskanie wielokrotności 300.
Pierwszy problem stanowił fakt, że była tam captcha do rozwiązania, ale była ona przewidywalna i zmieniała się co 1s.
Drugi problem polegał na tym, że nieudana próba wymagała zakładania nowego konta.
Po dwóch porażkach (najwyraźniej requesty trzeba było wysłać z dwóch równoległych sesji!) postanowiliśmy jeszcze raz poszukać łatwiejszej drogi do flagi.

I okazało się, że istnieje niezamierzona podatność - kiedy wysyłamy żądanie kupna przedmiotu dostarczamy jego ID.
Najwyraźniej skrypt następnie pobiera cenę przedmiotu o podanym ID aby sprawdzić czy mamy dość monet żeby go kupić.
Niemniej jednak jeśli ID nie istnieje w bazie nie ma żadnej weryfikacji i cena jest brana ze zwróconego przez bazę NULLa, który rzutuje się do 0.
W efekcie możemy bez problemu pozwolić sobie na kupno nieistniejącego przedmiotu i tym samym na uzyskanie flagi.

`flag{1m_s0rr4y_th4t_th3r3_1s_no_s3cr3t_4_U}`
