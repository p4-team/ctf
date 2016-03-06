## A numbers game (PPC, 50p)

	Description: People either love or hate math. Do you love it? Prove it! You just need to solve a bunch of equations without a mistake. 
	
###ENG
[PL](#pl-version)

Server sends input in format:

	Hi, I heard that you're good in math. Prove it!
	Level 1.: x - 18 = -12

And we are supposed to send the solution to the equation. 
So for the example above we parse `-` as operation, `18` as operand and `-12` as result, and thus the solution is `-12 + 18`.
We automate is wih a simple script that parses operation, operand and result and then applies corresponding operation (eg. + for -).

```python
import re
import socket
from time import sleep


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("188.166.133.53", 11027))
    regex = "Level \d+\.: x (.) (\d+) = (.+)"
    initial_data = str(s.recv(4096))
    print(initial_data)
    while True:
        sleep(1)
        task = str(s.recv(4096))
        m = re.search(regex, task)
        print(task)
        operation = m.group(1)
        operand = int(m.group(2))
        result = int(m.group(3))
        x = result
        if operation == "+":
            x = result - operand
        elif operation == "-":
            x = result + operand
        elif operation == "*":
            x = result / operand
        elif operation == "/":
            x = result * operand
        s.sendall(str(x) + "\n")
    pass

main()
```

After 100 examples we get a flag: `IW{M4TH_1S_34SY}`

###PL version

Serwer dostarcza dane w formacie:

	Hi, I heard that you're good in math. Prove it!
	Level 1.: x - 18 = -12

A naszym zadaniem jest rozwiązać podane równanie.
Dla przykładu powyżej parsujemy `-` jako operacje, `18` jako operand oraz `-12` jako wynik, więc rozwiązaniem jest `-12 + 18`.
Automatyzujemy to skryptem który parsuje operacje, operand oraz wynik a nastepnie wykorzystuje operacje przeciwną (np. + dla -).

```python
import re
import socket
from time import sleep


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("188.166.133.53", 11027))
    regex = "Level \d+\.: x (.) (\d+) = (.+)"
    initial_data = str(s.recv(4096))
    print(initial_data)
    while True:
        sleep(1)
        task = str(s.recv(4096))
        m = re.search(regex, task)
        print(task)
        operation = m.group(1)
        operand = int(m.group(2))
        result = int(m.group(3))
        x = result
        if operation == "+":
            x = result - operand
        elif operation == "-":
            x = result + operand
        elif operation == "*":
            x = result / operand
        elif operation == "/":
            x = result * operand
        s.sendall(str(x) + "\n")
    pass

main()
```

Po 100 przykładach dostajemy flagę: `IW{M4TH_1S_34SY}`
