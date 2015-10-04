## Reverse 300 (re, 300p)

### PL
(ENG)[eng-version]

Dostajemy [program](./r300.exe) (tym razem PE windowsowe), który pobiera od usera parę username:hasło. Mamy zdobyć hasło dla użytkownika "Administrator".

Okazuje się dodatkowo że są zabezpieczenia przed bezpośrednim zapytaniem o hasło dla usera "Administrator".

Program po kolei:
 - pyta o username
 - pyta o hasło
 - sprawdza czy w username występuje litera "A" - jeśli tak, to hasło nie będzie poprawnie generowane.
 - następnie sprawdza czy hasło ma odpowiednią długość (zależną od nicka - chyba zależność to długość_nicka - 1, ale nie sprawdzaliśmy). Jeśli nie, znowu, nie będzie błędu ale sprawdzenie wykona się niepoprawnie.
 - Następnie następuje sprawdzenie hasła:

```
for (int i = 0; i < strlen(password) - 1; i++) {
    if (!cbc_password_check(dużo obliczeń matematycznych na i, password[i])) {
        return false;
    }
}
```

 - poszliśmy na łatwiznę (a raczej, wybraliśmy optymalne rozwiązanie) - nie reversowaliśmy algorytmu, tylko śledziliśmy co robi funkcja cbc_password_check w każdej iteracji. Robiła ona dużo obliczeń na username, i na podstawie tego sprawdzała jaka powinna być kolejna litera hasła i wykonywała porównanie. Wystarczyło "prześledzić" raz przebieg tej funkcji, w debuggerze pominąć returny, i mieliśmy gotowe hasło.

Z tego odczytaliśmy wymagane hasło dla administratora: `#y1y3#y1y3##` i zdobyliśmy flagę.

### ENG

We get a [binary](./r300.exe) (this time a windows PE), which takes user:password pair as input. We need a password for "Administrator" user.

There are some additional protection against directly asking for password for "Administrator" user.

The binary:
 - asks for username
 - asks for password
 - checks if there is letter "A" in the useraname - if so, the password will not be generated correctly.
 - then it checks is the password has a proper length (depending on the usernaem - something like username_length -1, but we didn't check). If no, again it will not show any errors byt password check will fail.
 - then there is the actual password check:

```
for (int i = 0; i < strlen(password) - 1; i++) {
    if (!cbc_password_check(a lot of mathematical compuations over i, password[i])) {
        return false;
    }
}
```

- we took the easy path (or the optmimal solution) - we didn't try to reverse the algorithm, but we tracked what the cbc_password_check function was doing in each iteration. It was doing a lot fo computations on username and then it was using this to check what should be the next password letter and was doing the comparison. We only had to "track" this function once in a debugger, skip returns and we had the password.

With this approach we got the password for Administrator: `#y1y3#y1y3##` and we got the flag.