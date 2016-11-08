# Top Kek (crypto 50)


###ENG
[PL](#pl-version)

In the task we get encrypted data:

```
KEK! TOP!! KEK!! TOP!! KEK!! TOP!! KEK! TOP!! KEK!!! TOP!! KEK!!!! TOP! KEK! TOP!! KEK!! TOP!!! KEK! TOP!!!! KEK! TOP!! KEK! TOP! KEK! TOP! KEK! TOP! KEK!!!! TOP!! KEK!!!!! TOP!! KEK! TOP!!!! KEK!! TOP!! KEK!!!!! TOP!! KEK! TOP!!!! KEK!! TOP!! KEK!!!!! TOP!! KEK! TOP!!!! KEK!! TOP!! KEK!!!!! TOP!! KEK! TOP!!!! KEK!! TOP!! KEK!!!!! TOP! KEK! TOP! KEK!!!!! TOP! KEK! TOP!!!!! KEK! TOP! KEK! TOP!!!!! KEK! TOP! KEK! TOP!!!!! KEK! TOP! KEK! TOP!!!!! KEK! TOP! KEK! TOP!!!!! KEK! TOP! KEK! TOP!!!!! KEK!! TOP!! KEK!!! TOP! KEK! TOP!! KEK! TOP!! KEK! TOP! KEK! TOP! KEK! TOP!!!!! KEK! TOP!! KEK! TOP! KEK!!!!! TOP!! KEK! TOP! KEK!!! TOP! KEK! TOP! KEK! TOP!! KEK!!! TOP!! KEK!!! TOP! KEK! TOP!! KEK! TOP!!! KEK!! TOP! KEK!!! TOP!!! KEK! TOP! KEK! TOP!!!!! KEK! TOP! KEK!!! TOP!! KEK!! TOP!!! KEK! TOP! KEK! TOP! KEK! TOP! KEK!! TOP!!! KEK!! TOP! KEK! TOP!!!!! KEK! TOP!!! KEK!! TOP! KEK!!! TOP!! KEK!!! TOP! KEK! TOP!! KEK!! TOP!!! KEK! TOP! KEK!! TOP! KEK!!!! TOP!!! KEK! TOP! KEK!!! TOP! KEK! TOP!!!!! KEK! TOP!! KEK! TOP!!! KEK!!! TOP!! KEK!!!!! TOP! KEK! TOP! KEK! TOP!!! KEK! TOP! KEK! TOP!!!!! KEK!! TOP!! KEK! TOP! KEK!!! TOP! KEK! TOP! KEK!! TOP! KEK!!! TOP!! KEK!! TOP!! KEK! TOP! KEK! TOP!!!!! KEK! TOP!!!! KEK!! TOP! KEK!! TOP!! KEK!!!!! TOP!!! KEK! TOP! KEK! TOP! KEK! TOP! KEK! TOP!!!!! KEK! TOP!! KEK! TOP! KEK!!!!! TOP!! KEK! TOP! KEK!!! TOP!!! KEK! TOP!! KEK!!! TOP!! KEK!!! TOP! KEK! TOP!! KEK! TOP!!! KEK!! TOP!! KEK!! TOP!!! KEK! TOP! KEK! TOP!!!!! KEK! TOP!! KEK!! TOP!! KEK!! TOP!!! KEK! TOP! KEK! TOP! KEK! TOP!! KEK! TOP!!! KEK!! TOP! KEK! TOP!!!!! KEK! TOP! KEK! TOP!!!!! KEK! TOP! KEK! TOP!!!!! KEK! TOP! KEK! TOP!!!!! KEK! TOP! KEK! TOP!!!!! KEK! TOP! KEK! TOP!!!!! KEK! TOP! KEK!! TOP! KEK! TOP!! KEK!! TOP!! KEK!! TOP!! KEK! TOP! KEK!! TOP! KEK! TOP!! KEK!! TOP! KEK!!!! TOP! KEK!! TOP! KEK!!!! TOP! KEK!! TOP! KEK!!!! TOP! KEK! TOP!!!!! KEK! TOP!
```

We initially thought this is some kind of esolang similar to Ook! but then we figured that it has to be simpler - there is only alternating `TOP` and `KEK` and `!` after them.
After a while we finally guessed that this can be simply binary code with `TOP` or `KEK` signaling 0/1 and `!` signaling repeats.

So we prepared a code:

```python
import codecs

with codecs.open("data.txt") as input_file:
    data = input_file.read()
    result = ""
    for entry in data.split(" "):
        repeat = len(entry) - 3
        if entry[0] == "T":
            result += "1" * repeat
        else:
            result += "0" * repeat
    print(result)
    chunked = [result[i:i + 8] for i in range(0, len(result) - 7, 8)]
    print(chunked)
    converted = [chr(int(c, 2)) for c in chunked]
    print("".join(converted))
```

Which gave us the flag: `flag{T0o0o0o0o0P______1m_h4V1nG_FuN_r1gHt_n0W_4R3_y0u_h4v1ng_fun______K3K!!!}`

###PL version

W zadaniu dostajemy zakodowane dane:

```
KEK! TOP!! KEK!! TOP!! KEK!! TOP!! KEK! TOP!! KEK!!! TOP!! KEK!!!! TOP! KEK! TOP!! KEK!! TOP!!! KEK! TOP!!!! KEK! TOP!! KEK! TOP! KEK! TOP! KEK! TOP! KEK!!!! TOP!! KEK!!!!! TOP!! KEK! TOP!!!! KEK!! TOP!! KEK!!!!! TOP!! KEK! TOP!!!! KEK!! TOP!! KEK!!!!! TOP!! KEK! TOP!!!! KEK!! TOP!! KEK!!!!! TOP!! KEK! TOP!!!! KEK!! TOP!! KEK!!!!! TOP! KEK! TOP! KEK!!!!! TOP! KEK! TOP!!!!! KEK! TOP! KEK! TOP!!!!! KEK! TOP! KEK! TOP!!!!! KEK! TOP! KEK! TOP!!!!! KEK! TOP! KEK! TOP!!!!! KEK! TOP! KEK! TOP!!!!! KEK!! TOP!! KEK!!! TOP! KEK! TOP!! KEK! TOP!! KEK! TOP! KEK! TOP! KEK! TOP!!!!! KEK! TOP!! KEK! TOP! KEK!!!!! TOP!! KEK! TOP! KEK!!! TOP! KEK! TOP! KEK! TOP!! KEK!!! TOP!! KEK!!! TOP! KEK! TOP!! KEK! TOP!!! KEK!! TOP! KEK!!! TOP!!! KEK! TOP! KEK! TOP!!!!! KEK! TOP! KEK!!! TOP!! KEK!! TOP!!! KEK! TOP! KEK! TOP! KEK! TOP! KEK!! TOP!!! KEK!! TOP! KEK! TOP!!!!! KEK! TOP!!! KEK!! TOP! KEK!!! TOP!! KEK!!! TOP! KEK! TOP!! KEK!! TOP!!! KEK! TOP! KEK!! TOP! KEK!!!! TOP!!! KEK! TOP! KEK!!! TOP! KEK! TOP!!!!! KEK! TOP!! KEK! TOP!!! KEK!!! TOP!! KEK!!!!! TOP! KEK! TOP! KEK! TOP!!! KEK! TOP! KEK! TOP!!!!! KEK!! TOP!! KEK! TOP! KEK!!! TOP! KEK! TOP! KEK!! TOP! KEK!!! TOP!! KEK!! TOP!! KEK! TOP! KEK! TOP!!!!! KEK! TOP!!!! KEK!! TOP! KEK!! TOP!! KEK!!!!! TOP!!! KEK! TOP! KEK! TOP! KEK! TOP! KEK! TOP!!!!! KEK! TOP!! KEK! TOP! KEK!!!!! TOP!! KEK! TOP! KEK!!! TOP!!! KEK! TOP!! KEK!!! TOP!! KEK!!! TOP! KEK! TOP!! KEK! TOP!!! KEK!! TOP!! KEK!! TOP!!! KEK! TOP! KEK! TOP!!!!! KEK! TOP!! KEK!! TOP!! KEK!! TOP!!! KEK! TOP! KEK! TOP! KEK! TOP!! KEK! TOP!!! KEK!! TOP! KEK! TOP!!!!! KEK! TOP! KEK! TOP!!!!! KEK! TOP! KEK! TOP!!!!! KEK! TOP! KEK! TOP!!!!! KEK! TOP! KEK! TOP!!!!! KEK! TOP! KEK! TOP!!!!! KEK! TOP! KEK!! TOP! KEK! TOP!! KEK!! TOP!! KEK!! TOP!! KEK! TOP! KEK!! TOP! KEK! TOP!! KEK!! TOP! KEK!!!! TOP! KEK!! TOP! KEK!!!! TOP! KEK!! TOP! KEK!!!! TOP! KEK! TOP!!!!! KEK! TOP!
```

Początkowo myśleliśmy że to jakiś ezoteryczny język programowania podobny do Ook! ale potem doszliśmy do wniosku, że musi być jeszcze prościej - mamy w końcu tylko naprzemienne `TOP` i `KEK` oraz `!` za każdym z nich.
Po pewnym czasie zgadliśmy wreszcie, że to może być po prostu kod binarny gdzie `TOP` lub `KEK` określają 0/1 a `!` oznacza powtórzenia.

Napisaliśmy prosty skrypt:

```python
import codecs

with codecs.open("data.txt") as input_file:
    data = input_file.read()
    result = ""
    for entry in data.split(" "):
        repeat = len(entry) - 3
        if entry[0] == "T":
            result += "1" * repeat
        else:
            result += "0" * repeat
    print(result)
    chunked = [result[i:i + 8] for i in range(0, len(result) - 7, 8)]
    print(chunked)
    converted = [chr(int(c, 2)) for c in chunked]
    print("".join(converted))
```

Który dał nam flagę: `flag{T0o0o0o0o0P______1m_h4V1nG_FuN_r1gHt_n0W_4R3_y0u_h4v1ng_fun______K3K!!!}`
