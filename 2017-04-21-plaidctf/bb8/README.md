# BB-8 (crypto, 200p)

## ENG
[PL](#pl-version)

In the task we get a [source code](server.py) of service we can connect to.
We also get a lengthly [description](README.txt) of the protocol we are working with.

It is basically a standard BB-84 Quantum Key Distribution protocol.
The service we can connect to is a Man-in-the-middle infrastructure placed between Alice and Bob.

We know that Alice will sent Bob 600 qbits with 2 possible bases each, then Alice will confirm which bases Bob guessed right (statistically about half), then Bob will send to Alice half of the correct values he got, to make sure no-one modified the data on the way.
Finally from the remaining correct bit values Bob and Alice will take 128 and create AES-ECB-128 key and exchange encrypoted messages.

What we will do here is basically spoofing the entire communication, so that Alice and Bob in reality agree on the key with us, and not with the expected recipient.

This is trivial to do, since we can simply follow the protocol with both of them independently.
It will, however, not give us the whole flag!
This is because in the end there is the verification phase when parties exchange half of the correct values, and if we agreed on different number with Alice and with Bob then sadly we will have at some point to send wrong message to one of them (since we have to send one message to Alice and one message to Bob each time), which will trigger closing the channel.

So what we really want to do is to make sure we agree on the same number of correct values with both parties, using some heurustic and a bit of luck.

The whole idea is:

1. We collect values sent by Alice, for simplicity we always try base Z.
2. We send to Bob only values 1 all encoded in base Z, for simplicity :)
3. During the verification phase we verify how many bits we got right from Alice, by sending her always base Z and checking if she responded with -1 or 1
4. During verification phase we verify how many bits Bob got right, by checking if he tried base Z (we always encoded our 1 in Z when sending to him)
5. We introduce small heuristic to lie to Bob if he is getting too many good guesses, to lower his score. We could also lie the other way, as long as we make sure we're doing this on even bits, since only odd bits will be used as AES key, but this was not necessary.
6. Now we have set of qbit values agreed with Alice and we confirmed Bob with all the 1s he got right. Hopefully at this point the both counters are equal. It requires a bit of luck so we simply run this multiple times.
7. Next phase is trivial, we simply send to Alice half of the qbits we got right and we send ACK to Bob every time.
8. Now we agreed to have AES key with Bob which contains only 1s and we agreed with Alice on the key from the leftover qbits.
9. If the counters were equal both parties will now transmit their part of the flag. If the counters are not equal we will get only half of the flag and we will have to run again to get the other half!
10. We simply decode the results!

```python
import re
from crypto_commons.netcat.netcat_commons import nc, receive_until, send, receive_until_match, interactive


def select_agreed_values(qbits_from_alice, correct_base_guesses_from_alice):
    return [qbits_from_alice[i] for i in range(600) if correct_base_guesses_from_alice[i] == 1]


def main():
    url = 'bb8.chal.pwning.xxx'
    port = 20811
    s = nc(url, port)
    print(receive_until(s, "..."))
    qbits_from_alice = []
    print('spoofing initial communication')
    for i in range(1199):  # 600 qbits from Alice to Bob and 599 ACK from Bob to Alice
        c = receive_until(s, "?")
        print(i, c)
        if "Bob" in c:
            send(s, "y")  # intercept qbit to bob
            send(s, "Z")  # measure in Z
            send(s, "Y")  # replace
            send(s, "Z")  # Z axis
            send(s, "1")  # always send value 1
            data = receive_until_match(s, "value 1", 10.0)
            qbits_from_alice.append(int(re.findall("measured (-?\d+)", data)[0]))
        else:
            send(s, "N")  # don't touch ACKs
    print("alice qbits we got", qbits_from_alice)
    bases_from_bob = []
    correct_base_guesses_from_alice = []
    bob_correct = 0
    alice_correct = 0
    for i in range(1200):  # 600 qbit base guesses from Bob to Alice and 600 answers from Alice to Bob
        c = receive_until(s, "?")
        print(i, c)
        if "Alice" in c:  # intercept qbit base guess to Alice
            send(s, "y")
            send(s, "Z")  # measure in Z
            send(s, "Y")  # replace
            send(s, "Z")  # Z axis
            send(s, "-1")  # value -1 indicating Z base, we guess only Z base
            data = receive_until_match(s, "value -1", 10.0)
            bases_from_bob.append(int(re.findall("measured (-?\d+)", data)[0]))
        else:  # intercept alice answer
            send(s, "y")
            send(s, "Z")  # measure in Z
            data = receive_until_match(s, "measured (-?\d+)", 10.0)
            alice_answer = int(re.findall("measured (-?\d+)", data)[0])
            correct_base_guesses_from_alice.append(alice_answer)
            if alice_answer == 1:
                alice_correct += 1
            send(s, "Y")  # replace
            send(s, "Z")  # Z axis
            if bases_from_bob[-1] == -1:  # bob guessed Z axis
                if i > 1150 and alice_correct > bob_correct:  # slow down bob to get similar result len
                    send(s, "-1")
                else:
                    bob_correct += 1
                    send(s, "1")
            else:
                send(s, "-1")  # bob tried Y axis
            data = receive_until_match(s, "value -?\d+", 10.0)
    print("bases from bob", bases_from_bob)
    print("correct base guesses from alice", correct_base_guesses_from_alice)
    agreed_qbit_values = select_agreed_values(qbits_from_alice, correct_base_guesses_from_alice)
    print("agreed qbit values", len(agreed_qbit_values),
          agreed_qbit_values)  # qbit values where we correctly guessed the base
    print("bob was correct", bob_correct)
    print("we were correct with alice", alice_correct)

    alice_key = [agreed_qbit_values[i * 2 + 1] for i in range(128)]
    bob_key = [1 for _i in range(128)]  # we sent only 1 to bob, so all he got right must be 1s
    print('alice key', alice_key)
    print('bob key', bob_key)

    for i in range(max(bob_correct, alice_correct)):
        c = receive_until(s, "?")
        print(i, c)
        if "aborted" in c:
            interactive(s)
        elif "Alice" in c:
            send(s, "y")  # intercept Bob verification qbit
            send(s, "Z")  # measure in Z
            send(s, "Y")  # replace
            send(s, "Z")  # Z axis
            new_value = str(agreed_qbit_values[i])
            send(s, new_value)  # replace with value we got correct from Alice
            data = receive_until_match(s, "value " + new_value, 10.0)
        else:
            send(s, "N")  # pass ACK along
    c = receive_until(s, "?")
    print(c)
    interactive(s)


main()
```

This code gets us AES messages from both sides which we decode:

```python
def decode_flag():
    ct = '80dc59ce81e30bcd02198059b556731597ce5cf597481229ac9b2d523516c83e0f65896ce3b51cc2eb5b120adca55ed8'.decode(
        "hex")
    cipher = AES.new("\xff" * 16, AES.MODE_ECB)
    pt1 = cipher.decrypt(ct)
    ct2 = "34c7bb71814ff4f06e0d586e6f419364faf33270afed759e2593b36ac5b430f1".decode("hex")
    agreed_qbits = [1, -1, 1, 1, -1, -1, -1, 1, 1, -1, 1, 1, 1, 1, 1, -1, -1, -1, 1, 1, -1, 1, -1, 1, -1, -1, -1, 1, 1,
                    -1, -1, -1, -1, 1, 1, -1, 1, -1, -1, -1, 1, -1, -1, 1, -1, 1, 1, 1, -1, 1, 1, -1, -1, 1, 1, -1, -1,
                    -1, 1, 1, 1, -1, 1, -1, 1, -1, -1, 1, -1, 1, -1, 1, 1, 1, -1, -1, 1, -1, 1, -1, -1, 1, 1, -1, 1, 1,
                    -1, 1, 1, 1, 1, 1, -1, 1, -1, 1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, 1, -1, 1, -1, 1, 1,
                    -1, 1, -1, -1, -1, -1, 1, -1, 1, -1, 1, -1, 1, 1, -1, -1, -1, 1, 1, 1, 1, -1, 1, -1, 1, -1, -1, -1,
                    -1, 1, -1, -1, -1, -1, 1, -1, 1, -1, -1, 1, 1, -1, 1, -1, -1, 1, -1, -1, -1, -1, 1, -1, 1, -1, 1, 1,
                    1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, 1, -1, 1, -1, -1, 1, -1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, 1,
                    -1, 1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1, 1, -1, 1, -1, 1, -1, -1, 1, -1, -1, -1, -1, 1, 1, 1, -1,
                    1, 1, -1, -1, 1, -1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, -1, -1, -1, -1, -1, -1, 1, 1, -1, -1, 1, 1,
                    1, -1, -1, 1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, 1, 1, -1, -1, 1, 1, 1, 1, -1,
                    -1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1, -1, 1]
    key_qbits = [agreed_qbits[i * 2 + 1] for i in range(128)]
    key_bitstring = "".join(['1' if c == 1 else '0' for c in key_qbits])
    print(key_bitstring)
    key = int(key_bitstring, 2)
    k = long_to_bytes(key)
    cipher = AES.new(k, AES.MODE_ECB)
    pt2 = cipher.decrypt(ct2)
    print(pt2.strip()+pt1.strip())
```

And we have a flag: `PCTF{perhaps_secrecy_aint_the_same_thing_as_authentication}`

## PL version

W zadaniu dostajemy [kod](server.py) serwisu do którego możemy się połączyć.
Dostajemy też długi [opis](README.txt) protokołu z którym pracujemy.

To jest standardowy protokół BB-84 Kwantowej Wymiany Klucza.
Serwis z którym się komunikujemy pozwala na atak Man-in-the-middle pomiędzy Alice i Bobem.

Wiemy że Alice wyśle do Boba 600 qbitów, każdy w jednej z 2 baz, następnie Alice potwierdzi Bobowi które bazy zgadł poprawnie (statystycznie połowę), następnie Bob wyśle do Alice połowę poprawnych wartości które uzyskał, żeby upewnić się że nikt nie zmienił danych po drodze.
Na koniec z pozostałych poprawnych wartości Bob i Alice wezmą 128 bitów i utworzą z nich wspólny klucz AES-ECB-128 którym zaszyfrują swoje wiadomości.

My zamierzamy spoofować całą komunikacje, tak że w rzeczywistości Alice i Bob zgodzą się na klucze z nami a nie ze sobą nawzajem.

To generalnie jest trywialne, bo możemy po prostu postępować zgodnie z protokołem dla każdego z nich z osobna.
To niestety nie da nam całej flagi!
Jest tak, ponieważ na końcu jest faza weryfikacji kiedy Bob wysyła połowę poprawnych wartości do Alice i jeśli uzgodnimy  znimi różną liczbę poprawnych wartości to w pewnej chwili będziemy musieli do jednej ze stron wysłać nieoczekiwaną wartość (ponieważ możemy wysyłać jedynie qbity raz do Alice i raz do Boba), a to spowoduje zerwanie połączenia przez jedną ze stron.

Chcemy więc mieć pewność że uzgodnimy taką samą liczbę poprawnych wartości z obiema stronami, stosując trochę heurystyk i szczęścia.

Idea jest taka:

1. Pobieramy wartości od Alice, dla ułatwienia zawsze próbujemy bazę Z.
2. Wysyłamy do Boba same 1 w bazie Z, dla ułatwienia :)
3. Podczas weryfikacji uzgadniamy ile bitów od Alice wyznaczyliśmy poprawnie, wysyłając jej zawsze bazę Z i sprawdzając czy odpowiedziała -1 czy 1
4. Podczas weryfikacji sprawdzamy ile bitów Bob dobrze odkodował, testujac czy użył bazy Z (zawsze wysyłaliśmy mu 1 w bazie Z).
5. Wprowadzamy heurystykę, żeby kłamać Bobowi jeśli idzie mu za dobrze, żeby obniżyć jego wynik. Możemy kłamać też w drugą stronę, ale musimy uważać żeby robić to tylko dla parzystych bitów, bo te nie trafią potem do klucza AES, ale nie było to finalnie konieczne.
6. Teraz mamy listę qbitów od Alice które odczytaliśmy dobrze i wiemy też ile 1 Bob odczytał dobrze. Miejmy nadzieje że obie wartości są sobie równe. Wymaga to trochę szczęścia więc uruchomiliśmy solver kilka razy dla pewności.
7. Następna faza jest trywialna, po prostu wysyłamy do Alice połowę qbitów które dobrze od niej odczytaliśmy a do Boba wysyłamy ACK za każdym razem.
8. Teraz uzgodniliśmy z Bobe klucz złożony z samych 1 a z Alice ten z pozostałych bitów.
9. Jeśli liczniki były równe to teraz Bob i Alice wymienią się wiadomościami szyfrowanymi AESem. Jeśli liczniki nie były równe to dostaniemy tylko połowę flagi, bo jedna ze stron zerwie połączenie i będziemy musieli uruchomić to jeszcze raz.
10. Na koniec deszyfrujemy AESa!.

```python
import re
from crypto_commons.netcat.netcat_commons import nc, receive_until, send, receive_until_match, interactive


def select_agreed_values(qbits_from_alice, correct_base_guesses_from_alice):
    return [qbits_from_alice[i] for i in range(600) if correct_base_guesses_from_alice[i] == 1]


def main():
    url = 'bb8.chal.pwning.xxx'
    port = 20811
    s = nc(url, port)
    print(receive_until(s, "..."))
    qbits_from_alice = []
    print('spoofing initial communication')
    for i in range(1199):  # 600 qbits from Alice to Bob and 599 ACK from Bob to Alice
        c = receive_until(s, "?")
        print(i, c)
        if "Bob" in c:
            send(s, "y")  # intercept qbit to bob
            send(s, "Z")  # measure in Z
            send(s, "Y")  # replace
            send(s, "Z")  # Z axis
            send(s, "1")  # always send value 1
            data = receive_until_match(s, "value 1", 10.0)
            qbits_from_alice.append(int(re.findall("measured (-?\d+)", data)[0]))
        else:
            send(s, "N")  # don't touch ACKs
    print("alice qbits we got", qbits_from_alice)
    bases_from_bob = []
    correct_base_guesses_from_alice = []
    bob_correct = 0
    alice_correct = 0
    for i in range(1200):  # 600 qbit base guesses from Bob to Alice and 600 answers from Alice to Bob
        c = receive_until(s, "?")
        print(i, c)
        if "Alice" in c:  # intercept qbit base guess to Alice
            send(s, "y")
            send(s, "Z")  # measure in Z
            send(s, "Y")  # replace
            send(s, "Z")  # Z axis
            send(s, "-1")  # value -1 indicating Z base, we guess only Z base
            data = receive_until_match(s, "value -1", 10.0)
            bases_from_bob.append(int(re.findall("measured (-?\d+)", data)[0]))
        else:  # intercept alice answer
            send(s, "y")
            send(s, "Z")  # measure in Z
            data = receive_until_match(s, "measured (-?\d+)", 10.0)
            alice_answer = int(re.findall("measured (-?\d+)", data)[0])
            correct_base_guesses_from_alice.append(alice_answer)
            if alice_answer == 1:
                alice_correct += 1
            send(s, "Y")  # replace
            send(s, "Z")  # Z axis
            if bases_from_bob[-1] == -1:  # bob guessed Z axis
                if i > 1150 and alice_correct > bob_correct:  # slow down bob to get similar result len
                    send(s, "-1")
                else:
                    bob_correct += 1
                    send(s, "1")
            else:
                send(s, "-1")  # bob tried Y axis
            data = receive_until_match(s, "value -?\d+", 10.0)
    print("bases from bob", bases_from_bob)
    print("correct base guesses from alice", correct_base_guesses_from_alice)
    agreed_qbit_values = select_agreed_values(qbits_from_alice, correct_base_guesses_from_alice)
    print("agreed qbit values", len(agreed_qbit_values),
          agreed_qbit_values)  # qbit values where we correctly guessed the base
    print("bob was correct", bob_correct)
    print("we were correct with alice", alice_correct)

    alice_key = [agreed_qbit_values[i * 2 + 1] for i in range(128)]
    bob_key = [1 for _i in range(128)]  # we sent only 1 to bob, so all he got right must be 1s
    print('alice key', alice_key)
    print('bob key', bob_key)

    for i in range(max(bob_correct, alice_correct)):
        c = receive_until(s, "?")
        print(i, c)
        if "aborted" in c:
            interactive(s)
        elif "Alice" in c:
            send(s, "y")  # intercept Bob verification qbit
            send(s, "Z")  # measure in Z
            send(s, "Y")  # replace
            send(s, "Z")  # Z axis
            new_value = str(agreed_qbit_values[i])
            send(s, new_value)  # replace with value we got correct from Alice
            data = receive_until_match(s, "value " + new_value, 10.0)
        else:
            send(s, "N")  # pass ACK along
    c = receive_until(s, "?")
    print(c)
    interactive(s)


main()
```

To daje nam wiadomości szyfrowanego AESem oraz klucze:

```python
def decode_flag():
    ct = '80dc59ce81e30bcd02198059b556731597ce5cf597481229ac9b2d523516c83e0f65896ce3b51cc2eb5b120adca55ed8'.decode(
        "hex")
    cipher = AES.new("\xff" * 16, AES.MODE_ECB)
    pt1 = cipher.decrypt(ct)
    ct2 = "34c7bb71814ff4f06e0d586e6f419364faf33270afed759e2593b36ac5b430f1".decode("hex")
    agreed_qbits = [1, -1, 1, 1, -1, -1, -1, 1, 1, -1, 1, 1, 1, 1, 1, -1, -1, -1, 1, 1, -1, 1, -1, 1, -1, -1, -1, 1, 1,
                    -1, -1, -1, -1, 1, 1, -1, 1, -1, -1, -1, 1, -1, -1, 1, -1, 1, 1, 1, -1, 1, 1, -1, -1, 1, 1, -1, -1,
                    -1, 1, 1, 1, -1, 1, -1, 1, -1, -1, 1, -1, 1, -1, 1, 1, 1, -1, -1, 1, -1, 1, -1, -1, 1, 1, -1, 1, 1,
                    -1, 1, 1, 1, 1, 1, -1, 1, -1, 1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, 1, -1, 1, -1, 1, 1,
                    -1, 1, -1, -1, -1, -1, 1, -1, 1, -1, 1, -1, 1, 1, -1, -1, -1, 1, 1, 1, 1, -1, 1, -1, 1, -1, -1, -1,
                    -1, 1, -1, -1, -1, -1, 1, -1, 1, -1, -1, 1, 1, -1, 1, -1, -1, 1, -1, -1, -1, -1, 1, -1, 1, -1, 1, 1,
                    1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, 1, -1, 1, -1, -1, 1, -1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, 1,
                    -1, 1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1, 1, -1, 1, -1, 1, -1, -1, 1, -1, -1, -1, -1, 1, 1, 1, -1,
                    1, 1, -1, -1, 1, -1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, -1, -1, -1, -1, -1, -1, 1, 1, -1, -1, 1, 1,
                    1, -1, -1, 1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, 1, 1, -1, -1, 1, 1, 1, 1, -1,
                    -1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1, -1, 1]
    key_qbits = [agreed_qbits[i * 2 + 1] for i in range(128)]
    key_bitstring = "".join(['1' if c == 1 else '0' for c in key_qbits])
    print(key_bitstring)
    key = int(key_bitstring, 2)
    k = long_to_bytes(key)
    cipher = AES.new(k, AES.MODE_ECB)
    pt2 = cipher.decrypt(ct2)
    print(pt2.strip()+pt1.strip())
```

I dostajemy flagę: `PCTF{perhaps_secrecy_aint_the_same_thing_as_authentication}`
