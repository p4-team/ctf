# Trump Trump (crypto 100)

###ENG
[PL](#pl-version)

In the task we get access to remote RSA signature service.
We also get a [picture](trump.jpg) we are supposed to sign with this service.
But the server refuses to sign this specific payload.

We can send some random payloads and check how it's signed since we know the `e` and `n` public key components.
We can figure out from this that RSA is unpadded!
The attack is quite simple - it's RSA blinding attack on homomorphic unpadded RSA.
In short: we can split the payload into parts, sign each one of the separately and then combine the signatures.

So we make a script:
```python
import codecs
import socket
import re
from time import sleep


def bytes_to_long(data):
    return int(data.encode('hex'), 16)


def long_to_bytes(flag):
    flag = str(hex(flag))[2:-1]
    return "".join([chr(int(flag[i:i + 2], 16)) for i in range(0, len(flag), 2)])


def get_payload(payload):
    url = "trumptrump.pwn.republican"
    port = 3609
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, port))
    data = s.recv(9999)
    print(data)
    sleep(1)
    s.sendall(str(payload) + "\r\n")
    sleep(1)
    data = s.recv(99999999)
    return data


def get_signature(payload):
    data = get_payload(payload)
    print(data)
    return int(re.findall("kid: (\d+)", data)[0])


def combine_sigs(sig1, sig2):
    N = 23377710160585068929761618506991996226542827370307182169629858568023543788780175313008507293451307895240053109844393208095341963888750810795999334637219913785780317641204067199776554612826093939173529500677723999107174626333341127815073405082534438012567142969114708624398382362018792541727467478404573610869661887188854467262618007499261337953423761782551432338613283104868149867800953840280656722019640237553189669977426208944252707288724850642450845754249981895191279748269118285047312864220756292406661460782844868432184013840652299561380626402855579897282032613371294445650368096906572685254142278651577097577263
    return (sig1 * sig2) % N


def find_divisor(picture_long):
    for i in xrange(2, 10000):
        if picture_long % i == 0:
            print(i)
            return i


def main():
    with codecs.open("trump.jpg", "rb") as input_file:
        picture = input_file.read()
        picture_long = bytes_to_long(picture)
        print(picture_long)
        divisor = find_divisor(picture_long)
        sig1 = get_signature(picture_long / divisor)
        sig2 = get_signature(divisor)
        result_sig = combine_sigs(sig1, sig2)
        print(result_sig)
        payload = get_payload(result_sig)
        with codecs.open("result.bin", "wb") as output:
            output.write(payload)
```

This code takes the payload to sign, finds integer divisor (in this case `3`), signs divisor and payload/divisor and then combines the signatures.
Combining the signatures is just multiplying them back modulo `n`.

Now there was a very confusing step - what to do with the signature?
Apparently author really likes guessing games...
It turnes out we had to send the signature again to the server as payload and this would give us in return the picture with a flag:

![](./output.jpg)

###PL version

W zadaniu dostajemy adres zdalnego serwera podpisującego dane za pomocą RSA.
Dostajemy też [obrazek](trump.jpg) który mamy podpisać.
Ale serwer odmawia podpisania tych konkretnych danych.

Możemy wysłać inne dane a potem sprawdzić jak zostały zaszyfrowane bo znamy `e` oraz `n` - elementy klucza publicznego.
Z tego dowiadujemy sie że RSA nie używa tu paddingu!
Atak jest dość prostu - to RSA blinding na homomorficzne RSA bez paddingu.
W skrócie: mozemy podzielić dane na kawałki, podpisać je osobno a potem złożyć sygnatury.

Piszemy do tego skrypt:

```python
import codecs
import socket
import re
from time import sleep


def bytes_to_long(data):
    return int(data.encode('hex'), 16)


def long_to_bytes(flag):
    flag = str(hex(flag))[2:-1]
    return "".join([chr(int(flag[i:i + 2], 16)) for i in range(0, len(flag), 2)])


def get_payload(payload):
    url = "trumptrump.pwn.republican"
    port = 3609
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, port))
    data = s.recv(9999)
    print(data)
    sleep(1)
    s.sendall(str(payload) + "\r\n")
    sleep(1)
    data = s.recv(99999999)
    return data


def get_signature(payload):
    data = get_payload(payload)
    print(data)
    return int(re.findall("kid: (\d+)", data)[0])


def combine_sigs(sig1, sig2):
    N = 23377710160585068929761618506991996226542827370307182169629858568023543788780175313008507293451307895240053109844393208095341963888750810795999334637219913785780317641204067199776554612826093939173529500677723999107174626333341127815073405082534438012567142969114708624398382362018792541727467478404573610869661887188854467262618007499261337953423761782551432338613283104868149867800953840280656722019640237553189669977426208944252707288724850642450845754249981895191279748269118285047312864220756292406661460782844868432184013840652299561380626402855579897282032613371294445650368096906572685254142278651577097577263
    return (sig1 * sig2) % N


def find_divisor(picture_long):
    for i in xrange(2, 10000):
        if picture_long % i == 0:
            print(i)
            return i


def main():
    with codecs.open("trump.jpg", "rb") as input_file:
        picture = input_file.read()
        picture_long = bytes_to_long(picture)
        print(picture_long)
        divisor = find_divisor(picture_long)
        sig1 = get_signature(picture_long / divisor)
        sig2 = get_signature(divisor)
        result_sig = combine_sigs(sig1, sig2)
        print(result_sig)
        payload = get_payload(result_sig)
        with codecs.open("result.bin", "wb") as output:
            output.write(payload)
```

Ten kod bierze dane do podpisu, znajduje dzielnik całkowity (w tym przypadku `3`), podpisuje dzielnik oraz payload/dzielnik a następnie składa te dwa podpisy.
Składanie podpisów to po prostu przemnożenie ich modulo `n`.

Teraz nastąpił bardzo dziwny problem - co dalej zrobić z tym podpisem?
Autor bardzo lubi zgadywanki...
Okazało się, że należy wysłać ten podpis do serwera a serwer w odpowiedzi wyśle nam flagę:

![](./output.jpg)
