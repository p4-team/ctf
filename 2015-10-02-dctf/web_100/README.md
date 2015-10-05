##Web 100 (web, 100p)

###PL
[ENG](#eng-version)

W zadaniu dostajemy prostą stronę wyświetlającą ilość pieniędzy na koncie oraz okienko do aktywacji kodów. Zostaje nam udostępniony jednorazowy kod doładowujący 10$.

Po użyciu kodu dostajemy komunikat, że ciągle mamy za mało pieniędzy, zatem musimy znaleźć jakiś sposób na wielokrotne użycie tego samego kodu lub rozgryźć jak program weryfikuje kody. Zaczęliśmy od łatwiejszego.

Z kodami rabatowymi kojarzy się szczególnie jeden powszechny exploit: [race condtition](https://www.owasp.org/index.php/Race_Conditions).

Usuwamy ciasteczka żeby pozbyć się sesji i wysyłamy parę zapytań z tym samym kodem jednocześnie, po odświeżeniu strony pokazują nam się najszybciej zarobione pieniądze w życiu, oraz flagę.

### ENG version

We get a link to a webpage displaying the amount of money on our account and a form for submitting codes. We have a single-use code for 10$.

After we use this code we get an information that we still don't have enough money for the flag, so we assume we need to find a way to use the code multiple times or figure out how the system verifies the codes. We started with the simpler one.

There is a very common error with discount codes: [race condtition](https://www.owasp.org/index.php/Race_Conditions).

We remove cookies to get rid of current session (with already used code) and we send multiple requests at the same time. After the page loads we can see the fastest earned money in out lifes, and the flag.