# Diffie-Hellman 2 (crypto 300)

###ENG
[PL](#pl-version)

In the task we get parameters for Diffie-Hellman key exchange.
However, we get only the public secrets from the participants, like if we were sniffing them, and we want to get the shared secret from this.

We get:

```
p = 6703903964971298549787012499102923063739682910296196688861780721860882015036773488400937149083451713845015929093243025426876941405973284973216824503042047
ga = 842498333348457493583344221469363458551160763204392890034487820288 # g^a
gb = 89202980794122492566142873090593446023921664 # g^b
g = 9444732965739290427392
```

From this we want to calculate `g^ab mod p`, and therefore we need to know either `a` or `b`.
Normally this would not be possible, but the numbers we have are rather small, so we can effecively compute a discrete logarithm and recover `a` from `g^a` or `b` from `g^b`:

```python
def discrete_log(g, ga):
    for i in range(2, 1000):
        if g ** i == ga:
            return i


def main():
    p = 6703903964971298549787012499102923063739682910296196688861780721860882015036773488400937149083451713845015929093243025426876941405973284973216824503042047
    ga = 842498333348457493583344221469363458551160763204392890034487820288
    gb = 89202980794122492566142873090593446023921664
    g = 9444732965739290427392
    a = discrete_log(g, ga)
    b = discrete_log(g, gb)
    print(a)
    print(b)
    print(pow(gb, a, p))
    print(str(pow(gb, a, p))[:20])


main()

```

Which tells us that `a = 3`, `b = 2` and the flag is `70980344169492860405`

###PL version

W zadaniu dostajemy parametry dla wymiany klucza protokołem Diffiego Hellmana.
Niemniej dostajemy jedynie publiczne sekrety uczestników, tak jakbyśmy ich sniffowali, a chcemy z tego uzyskać wspólny sekret.
 
Dostajemy:

```
p = 6703903964971298549787012499102923063739682910296196688861780721860882015036773488400937149083451713845015929093243025426876941405973284973216824503042047
ga = 842498333348457493583344221469363458551160763204392890034487820288 # g^a
gb = 89202980794122492566142873090593446023921664 # g^b
g = 9444732965739290427392
```

I z tego chcemy policzyć `g^ab mod p`, co oznacza że musimy poznać `a` lub `b`.
Normalnie to nie byłoby możliwe, ale liczby na których operujemy są względnie małe więc możemy efektywnie policzyć logarytm dyskretny i odzyskać `a` z `g^a` lub `b` z `g^b`:

```python
def discrete_log(g, ga):
    for i in range(2, 1000):
        if g ** i == ga:
            return i


def main():
    p = 6703903964971298549787012499102923063739682910296196688861780721860882015036773488400937149083451713845015929093243025426876941405973284973216824503042047
    ga = 842498333348457493583344221469363458551160763204392890034487820288
    gb = 89202980794122492566142873090593446023921664
    g = 9444732965739290427392
    a = discrete_log(g, ga)
    b = discrete_log(g, gb)
    print(a)
    print(b)
    print(pow(gb, a, p))
    print(str(pow(gb, a, p))[:20])


main()

```

Co mówi nam ze `a = 3`, `b = 2` a flaga to `70980344169492860405`
