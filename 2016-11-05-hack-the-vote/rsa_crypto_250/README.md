# The best RSA (crypto 250)

###ENG
[PL](#pl-version)

This was a very badly designed task.
We prepared an expected solver, but we didn't get the flag simply because we assumed this can't be a right solution.
Apparently author thought it's a great idea to prepare a task which requires hours (!) of heavy multithreaded computations.

We get [data](data.txt) with a very very long ciphertext and very very long modulus.
However it's quite simple to notice that the modulus is divisible by 5, and quick check shows that it can be actually factored into primes <= 251.
The only problem is that there are about 1500 of each prime, so de modulus is something like:

`n = 3^14XX * 5^14XX * ... * 251^14XX`

We can quickly factor this with small sieve.

The naive approach would be to calculate `d` and `fi(n)` and decrypt the message, but this would take forever.
Smarter approach would be to use RSA-CRT, so calculate `c^d mod p1`, `c^d mod p2`... where `p1 = 3^14XX`, `p2 = 5^14XX` etc, and then we use Chinese Reminder Theorem to calculate the final value.

But this again takes a very very long time to calculate.
We even tried to speed this up using Hensel lifting when calculating each of the values, but this didn't help that much.

Therefore we simply decided we missed something here because it's just stupid to force us to run hours of computations.
Apparently we didn't and this was the intended solution...

###PL version

To było bardzo źle zaprojektowane zadanie.
Napisaliśmy do niego solver, ale nie uzyskaliśmy flagi zwyczajnie dlatego, ze uznaliśmy że to nie może być poprawne rozwiązanie.
Najwyraźniej autor uznał za świetny pomysł zadanie wymagające wielu godzin (!) równoległych obliczeń.

Dostajemy [dane](data.txt) z bardzo bardzo długim ciphertextem oraz bardzo bardzo długim modulusem.
Niemniej łatwo zauważyc, ze modulus jest podzielny przez 5, a szybkie sprawdzenie pozwala stwierdzić że w ogóle rozkłada sie na iloczyn liczb pierwszych <=251.
Jedyny problem jest taki, że każdej z tych liczb jest około 1500 więc modulus to coś w stylu:

`n = 3^14XX * 5^14XX * ... * 251^14XX`

Możemy to szybko rozłożyć prostym sitem.

Naiwne podejście to policzyć `d` oraz `fi(n)` a potem odszyfrować wiadomość, ale to trwałoby wieki.
Lepsze podejście to użyć RSA-CRT, policzyć `c^d mod p1`, `c^d mod p2`... gdzie `p1 = 3^14XX`, `p2 = 5^14XX` itd a potem złożyć te rozwiązania za pomocą Chińskiego Twierdzenia o Resztach.

Ale to mimo wszystko trwa bardzo długo.
Próbowaliśmy przyspieszyć to za pomocą liftingu Hensela przy liczeniu kolejnych wartości, ale to specjalnie nie pomogło.

W związku z tym uznaliśmy, że coś przeoczyliśmy, no przecież idiotycznym pomysłem byłoby wykonywać wielogodzinne obliczenia.
Okazało się jednak, że wg autora to wcale nie takie głupie i takie właśnie było oczekiwane rozwiązanie...
