#Offensive 100 (web, 100p)

`For eng scroll down`

W tym zadaniu dostajemy stronę z 3 sekcjami:

  * Przycisk Sign up
  * Przycisk Sign in
  * Tabela z logiem logowań
  
W tym zadaniu trzeba było zauważyć 2 rzeczy:

 * Czasami, logując się, zamiast zalogować się na swoje konto zostajemy zalogowani na konto osoby która zalogowała się w tym samym czasie.

 * Dokładnie co minutę, loguje się ktoś z id równym 0 (przypuszczamy, że jest to konto na które mamy się dostać)

Łącząc te dwa zjawiska postanawiamy zalogować się na swoje konto dokładnie w zerowej sekundzie.
 Nie działa, robimy reload strony iiii...
 
 ![Alt text](pic1.png)

In this task we get a web site with 3 sections:
 * Sign up button
 * Sign in button
 * Accounts logged in log

In order to complete this challange we had to notice 2 things:

 * Sometimes, when we log in, instead of logging in to our account we get redirected a account that logged in the same time.
 * Exactly every minute, a id=0 login appears in the log. (That probably is the account we have to get into)
 
Using theese 2 observations we decide to log in to our account at exactly 0 seconds.
When the site loads we're still on our accounts page, we try to reload the site and...
  ![Alt text](pic1.png)
