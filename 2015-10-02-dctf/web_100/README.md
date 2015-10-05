##Web 100 (web, 100p)

###PL
[ENG](#eng-version)


W zadaniu dostajemy prostą stronę wyświetlającą ilość pieniędzy na koncie oraz okienko do aktywacji kodów. Zostaje nam udostępniony jednorazowy kod doładowujący 10$.

Po użyciu kodu dostajemy komunikat, że ciągle mamy za mało kasy, zatem musimy jakoś znaleźć sposób na wielokrotne użycie tego samego kodu lub rozgryźć jak program weryfikuje te kody, zaczniemy od łatwiejszego :P

Z kodami rabatowymi kojarzy się szczególnie jeden powszechny exploit: [race condtition](https://www.owasp.org/index.php/Race_Conditions).

Usuwamy ciasteczka żeby pozbyć się sesji i wysyłamy parę zapytań z tym samym kodem jednocześnie, po odświeżeniu strony pokazują nam się najszybciej zarobione pieniądze w życiu :D

### ENG version
