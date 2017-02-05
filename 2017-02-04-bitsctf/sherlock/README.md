# Sherlock (crypto)

```
Sherlock has a mystery in front of him. Help him to find the flag. 
```

###ENG
[PL](#pl-version)

In the task we get a [book](sherlock.txt).
We figured we could compare it to the [original text from Project Gutenberg](sherlock_orig.txt).

We had to make it lowercase and remove the ToC but other than that the comparison was simple:

```python
import codecs


def main():
    with codecs.open("sherlock.txt", "r") as input_file:
        task_data = input_file.read()
        task_data.replace("\n\n", "\n")
    with codecs.open("sherlock.txt", "r") as input_file:
        original_data = input_file.read()
        original_data = original_data.lower()
        original_data.replace("\n\n", "\n")
    result = "".join([task_data[i] for i in range(len(task_data)) if task_data[i] != original_data[i]])
    print(result)


main()
```

This gave us a long string with `ZEROONEZERO...`.
We changed this into a number and interpreted as text:

```python
from crypto_commons.generic import long_to_bytes

    result = result.replace("ZERO", "0")
    result = result.replace("ONE", "1")
    print(long_to_bytes(int(result, 2)))
```

And we got `BITSCTF{h1d3_1n_pl41n_5173}`

###PL version

W zadaniu dostajemy [książkę](sherlock.txt).
Postanowiliśmy porównać ją z [oryginalnym tekstem z Project Gutenberg](sherlock_orig.txt).

Musieliśmy zmienić ją na lowercase i usunąć spis treści, ale cała reszta była prosta:

```python
import codecs


def main():
    with codecs.open("sherlock.txt", "r") as input_file:
        task_data = input_file.read()
        task_data.replace("\n\n", "\n")
    with codecs.open("sherlock.txt", "r") as input_file:
        original_data = input_file.read()
        original_data = original_data.lower()
        original_data.replace("\n\n", "\n")
    result = "".join([task_data[i] for i in range(len(task_data)) if task_data[i] != original_data[i]])
    print(result)


main()
```

To dało nam długi string `ZEROONEZERO...`.
Po zmianie tego na liczbę a następnie zinterpretowaniu jako tekst:

```python
from crypto_commons.generic import long_to_bytes

    result = result.replace("ZERO", "0")
    result = result.replace("ONE", "1")
    print(long_to_bytes(int(result, 2)))
```

Dostaliśmy `BITSCTF{h1d3_1n_pl41n_5173}`
