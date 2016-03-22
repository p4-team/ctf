## smartcat0 (web)

###ENG
[PL](#pl-version)

We get a webpage where we can input an IP address and the page will ping it and show us the results.
The task was very similar to the one from teaser (https://github.com/p4-team/ctf/tree/master/2016-01-16-insomnihack/web_100_smartcat#eng-version), but this time `;` was not blacklisted.
Therefore we only had to put as input

```
127.0.0.1;command
```

And this way we could get remote code execution.
We used `find` to look for the flag and then we simply used `cat` to read it.

###PL version

Dostajemy stronę internetową na której możemy podać adres IP do pingowania a następnie dostaniemy wyniki pinga.
Zadanie jest bardzo podobne do tego z teasera (https://github.com/p4-team/ctf/tree/master/2016-01-16-insomnihack/web_100_smartcat), ale tym razem znak `;` był dozwolny.
W związku z tym wystarczyło podać jako wejście:

```
127.0.0.1;command
```

I w ten sposób uzyskaliśmy remote code execution.
Teraz wystarczyło użyć `find` aby zlokalizować flagę oraz `cat` aby ją wypisać.
