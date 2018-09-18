# uncompyle6 version 2.11.5
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.15rc1 (default, Apr 15 2018, 21:51:34) 
# [GCC 7.3.0]
# Embedded file name: oceanOfSockets.py
import requests
import httplib
import sys
if len(sys.argv) < 2:
    sys.exit(0)
host = sys.argv[1]
port = sys.argv[2]

def request1():
    r = requests.get('http://{}/tmctf.html:{}'.format(host, port))
    for data in r.iter_content():
        if 'OceanOfSockets' not in data:
            r = requests.get('http://{}/index.html:{}'.format(host, port), headers={'content-type': 'text/html','user-agent': 'Edge/12'})
        else:
            break


def request2():
    r = requests.get('http://{}/tmctf.html:{}'.format(host, port))
    for data in r.iter_content():
        if 'OceanOfSockets' not in data:
            r = requests.get('http://{}/index.html:{}'.format(host, port), headers={'content-type': 'text/html','user-agent': 'Edge/12'})
        else:
            break


def request3():
    r = requests.get('http://{}/tmctf.html:{}'.format(host, port))
    for data in r.iter_content():
        if 'OceanOfSockets' not in data:
            r = requests.get('http://{}/index.html:{}'.format(host, port), headers={'content-type': 'text/html','user-agent': 'Edge/12'})
        else:
            break


def request3():
    r = requests.get('http://{}/tmctf.html:{}'.format(host, port))
    for data in r.iter_content():
        if 'OceanOfSockets' not in data:
            r = requests.get('http://{}/index.html:{}'.format(host, port), headers={'content-type': 'text/html','user-agent': 'Edge/12'})
        else:
            break


def request3():
    r = requests.get('http://{}/tmctf.html:{}'.format(host, port))
    for data in r.iter_content():
        if 'OceanOfSockets' not in data:
            r = requests.get('http://{}/index.html:{}'.format(host, port), headers={'content-type': 'text/html','user-agent': 'Edge/12'})
        else:
            break


def request3():
    r = requests.get('http://{}/tmctf.html:{}'.format(host, port))
    for data in r.iter_content():
        if 'OceanOfSockets' not in data:
            r = requests.get('http://{}/index.html:{}'.format(host, port), headers={'content-type': 'text/html','user-agent': 'Edge/12'})
        else:
            break


def request3():
    r = requests.get('http://{}/tmctf.html:{}'.format(host, port))
    for data in r.iter_content():
        if 'OceanOfSockets' not in data:
            r = requests.get('http://{}/index.html:{}'.format(host, port), headers={'content-type': 'text/html','user-agent': 'Edge/12'})
        else:
            break


def request():
    try:
        connection = httplib.HTTPConnection(sys.argv[1], sys.argv[2])
        connection.request('GET', '/tmctf.html')
        resTMCF = connection.getresponse()
        readData = resTMCF.read()
        if 'OceanOfSockets' in readData:
            headers = {'User-Agent': 'Mozilla Firefox, Edge/12','Content-type': 'text/html','Cookie': '%|r%uL5bbA0F?5bC0E9b0_4b2?N'}
            connection.request('GET', '/index.html', '', headers)
        else:
            sys.exit(0)
    except:
        pass


if __name__ == '__main__':
    request()