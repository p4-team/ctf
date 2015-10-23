from queue import Queue
import socket
import threading
import re


def parse_seed(data):
    pattern = re.compile(".*(\d{2})\\.(\d{2})\\.(\d{4}).*(\d{2}):(\d{2}):(\d{2})", re.MULTILINE | re.DOTALL)
    seed = pattern.findall(data)[0]
    return int(str.format("{2}{1}{0}{3}{4}{5}", *seed))


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


def conn():
    for i in range(max):
        thread = threading.Thread(target=worker, args=[i])
        thread.daemon = True
        thread.start()
    for i in range(max):
        threads.put(i)
    threads.join()


conn()
