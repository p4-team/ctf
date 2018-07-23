#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import hmac
import socket
from hashlib import sha1
from Crypto.Cipher import AES
from struct import pack, unpack
from threading import Thread, Lock
from base64 import standard_b64encode
from time import time, sleep, strftime


class SecureServer:

    def __init__(self):
        self.msg_end = '</msg>'
        self.msg_not_found = 'NOT_FOUND'
        self.msg_wrong_pin = 'BAD_PIN'
        self.lock = Lock()
        self.log_path = '../top_secret/server.log'
        self.real_flag = '../top_secret/real.flag'
        self.aes_key = '../top_secret/aes.key'
        self.totp_key = 'totp.secret'
        self.files_available = [
                                    'lorem.txt',
                                    'flag.txt',
                                    'admin.txt',
                                    'password.txt'
                                ]

        self.host = '0.0.0.0'
        self.port = 7331
        self.buff_size = 1024

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(50)

        self.listener = Thread(target=self.listen)
        self.listener.daemon = True
        self.listener.start()

        self.log('Server started')

    def listen(self):
        while True:
            try:
                client, address = self.sock.accept()
                client.settimeout(30)
                sock_thread = Thread(target=self.handle, args=(client, address))
                sock_thread.daemon = True
                sock_thread.start()

                self.log('Client {0} connected'.format(address[0]))

            except Exception as ex:
                self.log(ex)

    def handle(self, client, address):
        data = self.recv_until(client, self.msg_end)
        self.log('Got message from client {0}: {1}'.format(address[0], data))

        args = data.split(' ', 1)
        command = args[0].strip()

        if command == 'list':
            self.send_list_files(client, address)
        elif command == 'login':
            self.send_login_time(client, address)
        elif command == 'file':
            if len(args) != 2:
                self.send(client, 'Bad request')
            else:
                self.send_file_data(args[1], client, address)
        elif command == 'admin':
            if len(args) != 2:
                self.send(client, 'Bad request')
            else:
                self.send_admin_token(args[1], client, address)
        else:
            self.send(client, 'Bad request or timed out')

        client.close()

    def send_list_files(self, client, address):
        self.send(client, ','.join(self.files_available))
        self.log('Sending available files list to client {0}'.format(address[0]))

    def send_login_time(self, client, address):
        self.send(client, int(time()))
        self.log('Client auth from {0}'.format(address[0]))

    def send_file_data(self, file, client, address):
        content = self.read_file(file)
        response = '{0}: {1}'.format(file, content)
        encrypted_response = self.encrypt(response)
        self.send(client, encrypted_response)
        self.log('Sending file "{0}" to client {1}'.format(file, address[0]))

    def send_admin_token(self, client_pin, client, address):
        try:
            if self.check_totp(client_pin):
                response = 'flag: {0}'.format(open(self.real_flag).read())
                self.send(client, response)
                self.log('Sending admin token to client {0}'.format(address[0]))
            else:
                self.send(client, self.msg_wrong_pin)
                self.log('Wrong pin from client {0}'.format(address[0]))

        except Exception as ex:
            self.log(ex)
            self.send(client, 'Bad request')

    def check_totp(self, client_pin):
        try:
            secret = open(self.totp_key).read()
            server_pin = self.totp(secret)
            return client_pin == server_pin

        except Exception as ex:
            self.log(ex)
            return False

    def totp(self, secret):
        counter = pack('>Q', int(time()) // 30)
        totp_hmac = hmac.new(secret.encode('UTF-8'), counter, sha1).digest()
        offset = totp_hmac[19] & 15
        totp_pin = str((unpack('>I', totp_hmac[offset:offset + 4])[0] & 0x7fffffff) % 1000000)
        return totp_pin.zfill(6)

    def encrypt(self, data):
        block_size = 16

        data = data.encode('utf-8')
        pad = block_size - len(data) % block_size
        data = data + (pad * chr(pad)).encode('utf-8')

        key = open(self.aes_key).read()
        cipher = AES.new(key, AES.MODE_ECB)

        return standard_b64encode(cipher.encrypt(data)).decode('utf-8')

    def read_file(self, file):
        try:
            clean_path = self.sanitize(file)
            if clean_path is not None:
                return open(clean_path).read()
            else:
                return self.msg_not_found

        except Exception as ex:
            self.log(ex)
            return self.msg_not_found

    def sanitize(self, file):
        try:
            if file.find('\x00') == -1:
                file_name = file
            else:
                file_name = file[:file.find('\x00')]

            file_path = os.path.realpath('files/{0}'.format(file_name))

            if file_path.startswith(os.getcwd()):
                return file_path
            else:
                return None

        except Exception as ex:
            self.log(ex)
            return None

    def send(self, client, data):
        client.send('{0}{1}'.format(data, self.msg_end).encode('UTF-8'))

    def recv_until(self, client, end):
        try:
            recv = client.recv(self.buff_size).decode('utf-8')
            while recv.find(end) == -1:
                recv += client.recv(self.buff_size).decode('utf-8')
            return recv[:recv.find(end)]

        except Exception as ex:
            self.log(ex)
            return ''

    def log(self, data):
        self.lock.acquire()
        print('[{0}] {1}'.format(strftime('%d.%m.%Y %H:%M:%S'), data))
        sys.stdout.flush()
        self.lock.release()


if __name__ == '__main__':
    secure_server = SecureServer()

    while True:
        try:
            sleep(1)
        except KeyboardInterrupt:
            secure_server.log('Server terminated')
            exit(0)

