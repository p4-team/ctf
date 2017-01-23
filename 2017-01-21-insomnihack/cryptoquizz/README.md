# cryptoquizz (crypto/misc 50)

###ENG
[PL](#pl-version)

The task was marked as crypto but it was a misc if anything.
In the task the server ask us about a year of birth of some famous cryptographer and after a while sends a flag.
We made a script which was taking data from google and wikipedia for this.
Since the timeout was very short we cached all results we had and stored in a dict for later reuse:

```python
import re
import requests
from crypto_commons.netcat.netcat_commons import nc, receive_until_match


def get_birth_year(name):
    url = "https://www.google.pl/search?q=" + (name.replace(" ", "+"))
    content = requests.get(url).content
    reg = "Data i miejsce urodzenia:.+?(\d{4})"
    potential = re.findall(reg, content)
    if len(potential) > 0:
        return potential[0]
    reg = "Data urodzenia:.+?(\d{4})"
    potential = re.findall(reg, content)
    if len(potential) > 0:
        return potential[0]
    else:
        url = "https://en.wikipedia.org/wiki/" + (name.replace(" ", "_"))
        content = requests.get(url).content
        reg = "\(.*born.*(\d{4})\)"
        return re.findall(reg, content)[0]


def main():
    dictionary = {'David Chaum': '1955', 'Paul Kocher': '1973', 'Jean-Jacques Quisquater': '1945',
                  'Gilles Brassard': '1955', 'David Naccache': '1967', 'Claus-Peter Schnorr': '1943',
                  'Oded Goldreich': '1957', 'Scott Vanstone': '1947', 'Douglas Stinson': '1956',
                  'Vincent Rijmen': '1970', 'Yehuda Lindell': '1971', 'Daniel Bleichenbacher': '1964',
                  'Rafail Ostrovsky': '1963', 'Wang Xiaoyun': '1966', 'Donald Davies': '1924', 'Claude Shannon': '1916',
                  'Daniel J. Bernstein': '1971', 'Neal Koblitz': '1948', 'Tatsuaki Okamoto': '1952',
                  'Horst Feistel': '1915', 'Paul van Oorschot': '1962', 'Whitfield Diffie': '1944',
                  'Kaisa Nyberg': '1948', 'Lars Knudsen': '1962', 'Alan Turing': '1912', 'Markus Jakobsson': '1968',
                  'Silvio Micali': '1954', 'Nigel P. Smart': '1967', 'Ivan Damgard': '1956', 'Jacques Patarin': '1965',
                  'Serge Vaudenay': '1968', 'Jacques Stern': '1949', 'Ron Rivest': '1947', 'Yvo Desmedt': '1956',
                  'Arjen K. Lenstra': '1956'}
    s = nc("quizz.teaser.insomnihack.ch", 1031)
    reg = "What is the birth year of (.*) \?\n\n"
    try:
        while True:
            data = receive_until_match(s, reg, 1000)
            print(data)
            name = re.findall(reg, data)[0]
            print(name)
            if name in dictionary:
                year = dictionary[name]
            else:
                year = get_birth_year(name)
                dictionary[name] = year
            print(year)
            s.sendall(year + "\n")
            print(dictionary)
    except:
        print(data)
        print(dictionary)


main()
```

And this got us instantly: `INS{GENUINE_CRYPTOGRAPHER_BUT_NOT_YET_A_PROVEN_SKILLED_ONE}`

###PL version

Zadanie było oznaczone jako crypto, ale ewidentnie był to misc.
W zadaniu serwer pyta nas o rok urodzenia sławnych kryptografów a po kilku udanych próbach zwraca flagę.
Napisaliśmy skrypt który za pomocą google i wikipedii wyszukiwał odpowiedź.
Timeout był bardzo krótki więc wyniki zbieraliśmy w mapie żeby móc je ponownie wykorzystać.

```python
import re
import requests
from crypto_commons.netcat.netcat_commons import nc, receive_until_match


def get_birth_year(name):
    url = "https://www.google.pl/search?q=" + (name.replace(" ", "+"))
    content = requests.get(url).content
    reg = "Data i miejsce urodzenia:.+?(\d{4})"
    potential = re.findall(reg, content)
    if len(potential) > 0:
        return potential[0]
    reg = "Data urodzenia:.+?(\d{4})"
    potential = re.findall(reg, content)
    if len(potential) > 0:
        return potential[0]
    else:
        url = "https://en.wikipedia.org/wiki/" + (name.replace(" ", "_"))
        content = requests.get(url).content
        reg = "\(.*born.*(\d{4})\)"
        return re.findall(reg, content)[0]


def main():
    dictionary = {'David Chaum': '1955', 'Paul Kocher': '1973', 'Jean-Jacques Quisquater': '1945',
                  'Gilles Brassard': '1955', 'David Naccache': '1967', 'Claus-Peter Schnorr': '1943',
                  'Oded Goldreich': '1957', 'Scott Vanstone': '1947', 'Douglas Stinson': '1956',
                  'Vincent Rijmen': '1970', 'Yehuda Lindell': '1971', 'Daniel Bleichenbacher': '1964',
                  'Rafail Ostrovsky': '1963', 'Wang Xiaoyun': '1966', 'Donald Davies': '1924', 'Claude Shannon': '1916',
                  'Daniel J. Bernstein': '1971', 'Neal Koblitz': '1948', 'Tatsuaki Okamoto': '1952',
                  'Horst Feistel': '1915', 'Paul van Oorschot': '1962', 'Whitfield Diffie': '1944',
                  'Kaisa Nyberg': '1948', 'Lars Knudsen': '1962', 'Alan Turing': '1912', 'Markus Jakobsson': '1968',
                  'Silvio Micali': '1954', 'Nigel P. Smart': '1967', 'Ivan Damgard': '1956', 'Jacques Patarin': '1965',
                  'Serge Vaudenay': '1968', 'Jacques Stern': '1949', 'Ron Rivest': '1947', 'Yvo Desmedt': '1956',
                  'Arjen K. Lenstra': '1956'}
    s = nc("quizz.teaser.insomnihack.ch", 1031)
    reg = "What is the birth year of (.*) \?\n\n"
    try:
        while True:
            data = receive_until_match(s, reg, 1000)
            print(data)
            name = re.findall(reg, data)[0]
            print(name)
            if name in dictionary:
                year = dictionary[name]
            else:
                year = get_birth_year(name)
                dictionary[name] = year
            print(year)
            s.sendall(year + "\n")
            print(dictionary)
    except:
        print(data)
        print(dictionary)


main()
```

To prawie od razu dało nam: `INS{GENUINE_CRYPTOGRAPHER_BUT_NOT_YET_A_PROVEN_SKILLED_ONE}`
