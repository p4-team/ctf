# Fibonacci (ppc 400)

###ENG
[PL](#pl-version)

The task is pretty simple.
The server asks us how many recursions we need to compute N-th fibonacci number (using recursive algorithm).
For some reason we could spend 25s on each question, which was a bit silly considering we could just pre-compute the results instantly in a fraction of a second.

We can compute this using a dynamic algorithm.
First two fibonacci numbers require 0 recursions, and k-th number require as many recursions as calculating k-2-th number + 1 (1 because we are calling fib(k-2)), plus calculating k-1-th number plus 1 (again 1 because we are calling fib(k-1)).
And we can compute this iteratively from the bottom.
So in general:

```python
calls = [0, 0] + [0] * (n + 1)
for i in range(2, n + 1):
	calls[i] = calls[i - 1] + calls[i - 2] + 2
```

We started by pre-computing results for the first 1000 numbers, but this as already an overkill because the largest tests were less than 500.
Running this on 100 tests gives the flag: `3DS{g00d4lgorithmsC4nSaveYourTime}`

###PL version

Zadanie było dość proste.
Serwer pytał ile wywołań rekurencyjnych potrzeba zeby policzyć N-tą liczbę fibonacciego (używając algorytmu rekurencyjnego).
Z jakiegoś powodu mogliśmy użyć aż 25s na jedno pytanie, co było dość dziwne biorąc pod uwagę że można było wyliczyć sobie wcześniej tablicę rozwiązań w ułamku sekundy.

Możemy policzyć rozwiązanie algorytmem dynamicznym.
Pierwsze dwie liczby wymagają 0 rekurencji a k-ta liczba wymaga tyle rekurencji ile policzenie liczby k-2 plus 1 (1 bo wywołujemy fib(k-2)), plus ile policzenie liczby k-1 plus 1 (znowu 1 bo wywyłujemy fib(k-1)).
Czyli generalnie:

```python
calls = [0, 0] + [0] * (n + 1)
for i in range(2, n + 1):
	calls[i] = calls[i - 1] + calls[i - 2] + 2
```

Zaczęliśmy przez wyliczenie rozwiazań dla pierwszego 1000 liczb bo okazało się przeszacowaniem, ponieważ największy test miał nie więcej niż 500.
Uruchomienie tego dla 100 testów dało nam flagę: `3DS{g00d4lgorithmsC4nSaveYourTime}`
