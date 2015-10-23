## GuessTheNumber (ppc, 150+80p)

	The teacher of your programming class gave you a tiny little task: just write a guess-my-number script that beats his script. He also gave you some hard facts:
	he uses some LCG with standard glibc LCG parameters
	the LCG is seeded with server time using number format YmdHMS (python strftime syntax)
	numbers are from 0 up to (including) 99
	numbers should be sent as ascii string
	You can find the service on school.fluxfingers.net:1523

### PL
[ENG](#eng-version)

Pierwsze podejście do zadania polegało na implementacji opisanego w zadaniu LCG i próbie dopasowania wyników do zgadywanki z serwera. Jednak bardzo szybko uznaliśmy, że możliwości jest bardzo dużo i nie ma sensu ich analizować skoro da się to zadanie wykonać dużo prościej.
Do zgadnięcia mamy zaledwie 100 liczb pod rząd a rozdzielczość zegara na serwerze to 1s. W związku z tym uznaliśmy, że prościej i szybciej będzie po prostu oszukiwać w tej grze :)

Wiemy że liczby generowane są przez LCG co oznacza, że dla danego seeda liczby do zgadnięcia są zawsze takie same. W szczególności jeśli dwóch użytkowników połączy się w tej samej sekundzie to wszystkie 100 liczb do zgadnięcia dla nich będzie takie samo. Dodatkowo serwer zwraca nam liczbę której oczekiwał jeśli się pomylimy.

Nasze rozwiązanie jest dość proste:

* Uruchamiamy 101 wątków, które w tej samej sekundzie łączą się z docelowym serwerem.
* Synchronizujemy wątki tak, żeby wszystkie zgadywały jedną turę w tej samej chwili a następnie czekały aż wszystkie skończą.
* W każdej turze wszystkie wątki oprócz jednego czekają na liczbę do wysłania.
* W każdej iteracji jeden wątek "poświęca się" wysyłając -1 jako odpowiedź, a następnie odbiera od serwera poprawną odpowiedź i informuje o niej pozostałe wątki.
* W efekcie co turę "tracimy" jeden wątek, ale wszystkie pozostałe przechodzą do następnej tury podając poprawną odpowiedź.

Każdy wątek realizuje poniższy kod:

```python
max = 101
threads = Queue()
correct_values = Queue()
init_barier = threading.Barrier(max)
init_barier_seeds = threading.Barrier(max)
bar = [threading.Barrier(max - i) for i in range(max)]
seeds = set()


def worker(index):
    threads.get()
    init_barier.wait()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("school.fluxfingers.net", 1523))
    initial_data = str(s.recv(4096))
    seeds.add(parse_seed(initial_data))
    init_barier_seeds.wait()
    if len(seeds) != 1:  # make sure we all start with the same seed, otherwise quit
        threads.task_done()
        return
    for i in range(max):
        bar[i].wait() #wait on the barrier for all other threads
        if i == index:  # suicide thread
            value = -1
        else:
            value = correct_values.get()
        s.send(bytes(str(value) + "\n", "ASCII"))
        data = str(s.recv(4096))
        print("thread " + str(index) + " iteration " + str(i) + " " + data)
        if "wrong" in data.lower():
            correct = re.compile("'(\d+)'").findall(data)[0]
            for j in range(max - i - 1):  # tell everyone what is the right number
                correct_values.put(correct)
            break
    threads.task_done()
```

Kompletny skrypt dostępny [tutaj](guess.py)

Uruchamiamy skrypt i dostajemy:
```
thread 98 iteration 97 b'Correct! Guess the next one!\n'
thread 99 iteration 97 b'Correct! Guess the next one!\n'
thread 100 iteration 97 b'Correct! Guess the next one!\n'
thread 98 iteration 98 b"Wrong! You lost the game. The right answer would have been '38'. Quitting."
thread 99 iteration 98 b'Correct! Guess the next one!\n'
thread 100 iteration 98 b'Correct! Guess the next one!\n'
thread 99 iteration 99 b"Wrong! You lost the game. The right answer would have been '37'. Quitting."
thread 100 iteration 99 b"Congrats! You won the game! Here's your present:\nflag{don't_use_LCGs_for_any_guessing_competition}"
```

`flag{don't_use_LCGs_for_any_guessing_competition}`

### ENG version

Initial attempt for this task was to implement described LCG and trying to match the output for the results on the server. But we instantly decided that there are too many possibilities and there is no point in wasting time for analysis when we can do it much easier.
We need to guess only 100 numbers in a row and the clock resolution on the server is just 1s. So we decided that it will be better and faster just to cheat the game :)

We know that the numbers are generated with LCG which means that for given seed the numbers are always the same. In particular, if two users connect at the same time the 100 numbers to guess will be identical. On top of that the server returns the expected number if we make a mistake.

Our solution was quite simple:

* Run 101 threads, which will connect to the server at the same time.
* Synchronize the threads so that they all execute a single turn and the wait for the rest.
* In each turn all threads but one are waiting for the number to send.
* In each turn one thread "sacrifices himself" sending -1 as answer, and the collects the correct number form server response and informs rest of the threads about it.
* As a result in each turn we "lose" one thread but all the others pass to the next round.

Eaach thread executes:

```python
max = 101
threads = Queue()
correct_values = Queue()
init_barier = threading.Barrier(max)
init_barier_seeds = threading.Barrier(max)
bar = [threading.Barrier(max - i) for i in range(max)]
seeds = set()


def worker(index):
    threads.get()
    init_barier.wait()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("school.fluxfingers.net", 1523))
    initial_data = str(s.recv(4096))
    seeds.add(parse_seed(initial_data))
    init_barier_seeds.wait()
    if len(seeds) != 1:  # make sure we all start with the same seed, otherwise quit
        threads.task_done()
        return
    for i in range(max):
        bar[i].wait() #wait on the barrier for all other threads
        if i == index:  # suicide thread
            value = -1
        else:
            value = correct_values.get()
        s.send(bytes(str(value) + "\n", "ASCII"))
        data = str(s.recv(4096))
        print("thread " + str(index) + " iteration " + str(i) + " " + data)
        if "wrong" in data.lower():
            correct = re.compile("'(\d+)'").findall(data)[0]
            for j in range(max - i - 1):  # tell everyone what is the right number
                correct_values.put(correct)
            break
    threads.task_done()
```

Complete script is [here](guess.py).

We run the script and we get:
```
thread 98 iteration 97 b'Correct! Guess the next one!\n'
thread 99 iteration 97 b'Correct! Guess the next one!\n'
thread 100 iteration 97 b'Correct! Guess the next one!\n'
thread 98 iteration 98 b"Wrong! You lost the game. The right answer would have been '38'. Quitting."
thread 99 iteration 98 b'Correct! Guess the next one!\n'
thread 100 iteration 98 b'Correct! Guess the next one!\n'
thread 99 iteration 99 b"Wrong! You lost the game. The right answer would have been '37'. Quitting."
thread 100 iteration 99 b"Congrats! You won the game! Here's your present:\nflag{don't_use_LCGs_for_any_guessing_competition}"
```

`flag{don't_use_LCGs_for_any_guessing_competition}`