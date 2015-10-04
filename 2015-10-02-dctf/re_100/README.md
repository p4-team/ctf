## Reverse 100 (re, 100p)

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

