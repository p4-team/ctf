## It's Prime Time! (PPC, 60p)

	Description: We all know that prime numbers are quite important in cryptography. Can you help me to find some? 
	
###ENG
[PL](#pl-version)

The server sends input as:

	Hi, you know that prime numbers are important, don't you? Help me calculating the next prime!
	Level 1.: Find the next prime number after 8:
	
And our task is to provide next prime numer after given number. 
Numbers were small so we could have implemented a naive algorithm or a sieve, but instead we just used `gmpy2.next_prime`:

```python
import re
import socket
import gmpy2
from time import sleep


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("188.166.133.53", 11059))
    regex = "Level \d+\.: .* (\d+)"
    initial_data = str(s.recv(4096))
    print(initial_data)
    while True:
        sleep(1)
        task = str(s.recv(4096))
        m = re.search(regex, task)
        print(task)
        previous_number = int(m.group(1))
        result = int(gmpy2.next_prime(previous_number))
        print("result = "+str(result))
        s.sendall(str(result) + "\n")
    pass

main()
```

And after 100 examples we got a flag: `IW{Pr1m3s_4r3_!mp0rt4nt}`

###PL version

Serwer przysyła dane w formacie:

	Hi, you know that prime numbers are important, don't you? Help me calculating the next prime!
	Level 1.: Find the next prime number after 8:
	
A naszym zadaniem jest zwrócić kolejną liczbę pierwszą po podnanej liczbie.
Liczby były bardzo małe więc mogliśmy użyć algorytmu naiwnego albo sita, ale zamiast tego użyliśmy gotowego `gmpy2.next_prime`:

```python
import re
import socket
import gmpy2
from time import sleep


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("188.166.133.53", 11059))
    regex = "Level \d+\.: .* (\d+)"
    initial_data = str(s.recv(4096))
    print(initial_data)
    while True:
        sleep(1)
        task = str(s.recv(4096))
        m = re.search(regex, task)
        print(task)
        previous_number = int(m.group(1))
        result = int(gmpy2.next_prime(previous_number))
        print("result = "+str(result))
        s.sendall(str(result) + "\n")
    pass

main()
```

I po 100 przykładach dostaliśmy flagę: `IW{Pr1m3s_4r3_!mp0rt4nt}`
