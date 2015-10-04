## Reverse 100 (re, 100p)

### PL
(ENG)[#eng-version]

Dostajemy [program](./r100) (elf konkretnie), który wykonuje bardzo proste sprawdzenie hasła i odpowiada czy hasło jest poprawne czy nie.

Domyślamy się że poprawne hasło jest flagą.

Cały program to coś w rodzaju:

    int main() {
        printf("Enter the password: ");
        if (fgets(&password, 255, stdin)) {
            if (check_password(password)) {
              puts("Incorrect password!");
            } else {
              puts("Nice!");
            }
        }
    }

Patrzymy więc w funkcję check_password (oczywiście nie nazywała się tak w binarce, nie dostaliśmy symboli):

    bool check_password(char *password) {
        char* arr[3] = { "Dufhbmf", "pG`imos", "ewUglpt" };
        for (i = 0; i <= 11; ++i) {
            if (v3[8 * (i % 3)][2 * (i / 3)] - password[i] != 1) {
                return true;
            }
        }
        return false;
    }

Z równania `v3[8 * (i % 3)][2 * (i / 3)] - password[i] != 1` od razu wynika co trzeba zrobić (coś - hasło ma być równe 1, czyli hasło = coś + 1).

Wyliczyliśmy hasło na podstawie podanych stałych i zdobyliśmy flagę.

### ENG

We get a [binary](./r100) (elf to be exact), which performs a simple password check and returns if the password was correct or not.

We expect the password to be the flag.

Whole code is something like: 

    int main() {
        printf("Enter the password: ");
        if (fgets(&password, 255, stdin)) {
            if (check_password(password)) {
              puts("Incorrect password!");
            } else {
              puts("Nice!");
            }
        }
    }

We go into the check_password function (of course it was not called like that in the binary, there was no symbol table):

    bool check_password(char *password) {
        char* arr[3] = { "Dufhbmf", "pG`imos", "ewUglpt" };
        for (i = 0; i <= 11; ++i) {
            if (v3[8 * (i % 3)][2 * (i / 3)] - password[i] != 1) {
                return true;
            }
        }
        return false;
    }

From the equation `v3[8 * (i % 3)][2 * (i / 3)] - password[i] != 1` we can see right away what we need to do (something - password has to be equal to 1 so therefore password+something = 1)

We simply calculated the password based on the constant values and got the flag.
