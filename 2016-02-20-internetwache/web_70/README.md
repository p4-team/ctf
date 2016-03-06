## The Secret Store (Web, 70p)

	Description: We all love secrets. Without them, our lives would be dull. 
	A student wrote a secure secret store, however he was babbling about problems with the database. 
	Maybe I shouldn't use the 'admin' account. 
	Hint1: Account deletion is intentional. 
	Hint2: I can't handle long usernames. 
	
###ENG
[PL](#pl-version)

In the task we get access to www page which allows us to register a user and set a "secret" value for him.
We expected that we were supposed to login as admin and the secret for the admin would be the flag.
We spent a lot of time on this, trying a lot of stuff including XSS (the page was vulnerable), blind SQLi and many more.
We have noticed that it was possible to change password for our users if we tried to register them again, but this didn't work for admin user.
The solution turned out to be rather simple - the limit for number of characters in login was 32, however the check for existing accounts took whole input to test.
This means that registering a user with 33 character in login would in fact register this user with only first 32 character as login, but the check for unique login would be performed on whole 33 characters input.

Therefore we registered user with login:

```python
payload = 'admin'+(' '*27)+'aa'
```

Which meant that in reality we simply changed the password for `admin` user since spaces were omitted.

The flag was: `IW{TRUNCATION_IS_MY_FRIEND}`

###PL version

W zadaniu dostajemy dostęp do strony www która pozwala zarejestrowac użytkownika i ustawić dla niego "sekretną" wartość.
Założyliśmy, że musimy zalogować się jako admiin a sekretna wartość będzie flagą.
Spędziliśmy nad tym zadaniem bardzo dużo czasu próbując różnych podejść, między innymi XSS (strona była podatna), ślepe SQLi i wiele innych.
Zauważyliśmy że jest możliwość zmiany hasła dla naszych użytkowników poprzez ponowną ich rejestracje, ale to nie działało dla admina.
Rozwiązanie okazało się dość proste - limit na długość loginu wynosił 32 znaki, ale test unikalności loginu był przeprowadzany dla całego wejścia.
To oznacza że rejestracja użytkownika z loginem na 33 znaki w rzeczywistości zarejestrowałby użytkownika z pierwszymi 32 znakami jako login, ale sprawdzenie czy taki użytkownik nie istnieje brałoby pod uwagę 33 znaki.

W związku z tym zarejestrowaliśmy użytkownika:

```python
payload = 'admin'+(' '*27)+'aa'
```

Co oznacza że w praktyce zmieniliśmy hasło dla `admin`, bo spacje zostały pominięte.

W ten sposób uzyskaliśmy flagę: `IW{TRUNCATION_IS_MY_FRIEND}`
