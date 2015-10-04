## Reverse 300 (re, 300p)

Dostajemy [program](./r300.exe) (tym razem PE windowsowe), który pobiera od usera parę username:hasło. Mamy zdobyć hasło dla użytkownika "Administrator".

Okazuje się dodatkowo że są zabezpieczenia przed bezpośrednim zapytaniem o hasło dla usera "Administrator".

Program po kolei:
 - pyta o username
 - pyta o hasło
 - sprawdza czy w username występuje litera "A" - jeśli tak, to hasło nie będzie poprawnie generowane.
 - następnie sprawdza czy hasło ma odpowiednią długość (zależną od nicka - chyba zależność to długość_nicka - 1, ale nie sprawdzaliśmy). Jeśli nie, znowu, nie będzie błędu ale sprawdzenie wykona się niepoprawnie.
 - Następnie następuje sprawdzenie hasła:

    for (int i = 0; i < strlen(password) - 1; i++) {
        if (!cbc_password_check(dużo obliczeń matematycznych na i, password[i])) {
            return false;
        }
    }

 - poszliśmy na łatwiznę (a raczej, wybraliśmy optymalne rozwiązanie) - nie reversowaliśmy algorytmu, tylko śledziliśmy co robi funkcja cbc_password_check w każdej iteracji. Robiła ona dużo obliczeń na username, i na podstawie tego sprawdzała jaka powinna być kolejna litera hasła i wykonywała porównanie. Wystarczyło "prześledzić" raz przebieg tej funkcji, w debuggerze pominąć returny, i mieliśmy gotowe hasło.

Z tego odczytaliśmy wymagane hasło dla administratora: #y1y3#y1y3##. I zdobyliśmy flagę.
