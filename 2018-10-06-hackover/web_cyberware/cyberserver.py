#!/usr/bin/python3
from threading import Thread
from sys import argv
from sys import getsizeof
from time import sleep
from socketserver import ThreadingMixIn
from http.server import SimpleHTTPRequestHandler
from http.server import HTTPServer
from re import search
from os.path import exists
from os.path import isdir


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


class CyberServer(SimpleHTTPRequestHandler):
    def version_string(self):
        return f'Linux/cyber'

    def do_GET(self):
        self.protocol_version = 'HTTP/1.1'

        referer = self.headers.get('Referer')
        path = self.path[1:] or ''

        if referer:
            self.send_response(412, 'referer sucks')
            self.send_header('Content-type', 'text/cyber')
            self.end_headers()
            self.wfile.write(b"Protected by Cyberware 10.1")
            return

        if not path:
            self.send_response(200, 'cyber cat')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            for animal in ['cat', 'fox', 'kangaroo', 'sheep']:
                self.wfile.write("<a href='{0}.txt'>{0}.txt</a></br>"
                                 .format(animal).encode())
            return

        if path.endswith('/'):
            self.send_response(403, 'You shall not list!')
            self.send_header('Content-type', 'text/cyber')
            self.end_headers()
            self.wfile.write(b"Protected by Cyberware 10.1")
            return

        if path.startswith('.'):
            self.send_response(403, 'Dots are evil')
            self.send_header('Content-type', 'text/cyber')
            self.end_headers()
            self.wfile.write(b"Protected by Cyberware 10.1")
            return

        if path.startswith('flag.git') or search('\\w+/flag.git', path):
            self.send_response(403, 'U NO POWER')
            self.send_header('Content-type', 'text/cyber')
            self.end_headers()
            self.wfile.write(b"Protected by Cyberware 10.1")
            return

        if not exists(path):
            self.send_response(404, 'Cyber not found')
            self.send_header('Content-type', 'cyber/error')
            self.end_headers()
            self.wfile.write(b"Protected by Cyberware 10.1")
            return

        if isdir(path):
            self.send_response(406, 'Cyberdir not accaptable')
            self.send_header('Content-type', 'cyber/error')
            self.end_headers()
            self.wfile.write(b"Protected by Cyberware 10.1")
            return

        try:
            with open(path, 'rb') as f:
                content = f.read()

            self.send_response(200, 'Yippie')
            self.send_header('Content-type', 'text/cyber')
            self.send_header('Content-length', getsizeof(content))
            self.end_headers()
            self.wfile.write(content)
        except Exception:
            self.send_response(500, 'Cyber alert')
            self.send_header('Content-type', 'cyber/error')
            self.end_headers()
            self.wfile.write("Cyber explosion: {}"
                             .format(path).encode())


class CyberServerThread(Thread):
    server = None

    def __init__(self, host, port):
        Thread.__init__(self)
        self.server = ThreadingSimpleServer((host, port), CyberServer)

    def run(self):
        self.server.serve_forever()
        return


def main(host, port):
    print(f"Starting cyberware at {host}:{port}")
    cyberProtector = CyberServerThread(host, port)
    cyberProtector.server.shutdown
    cyberProtector.daemon = True
    cyberProtector.start()
    while True:
        sleep(1)


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 1337
    if len(argv) >= 2:
        host = argv[1]
    if len(argv) >= 3:
        port = int(argv[3])
    main(host, port)
