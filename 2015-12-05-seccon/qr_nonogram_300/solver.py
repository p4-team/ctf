import requests
from bs4 import BeautifulSoup
from pwn import *
from PIL import Image, ImageDraw
import re
import qrtools

session = requests.Session()

def get_image(answer):
    source = session.post('http://qrlogic.pwn.seccon.jp:10080/game/', data={'ans': answer}).content
    soup = BeautifulSoup(source)

    #print source
    print re.findall('Stage: (\d+) / 30', source)

    def parse(cls):
        return [[span.contents[0] for span in th.find_all('span')] for th in soup.find_all('th', class_=cls)]

    rows = parse('rows')
    cols = parse('cols')

    solver = process('nonogram-0.9/nonogram')
    solver.sendline("%d %d" % (len(cols), len(rows)))

    for row in rows:
        solver.sendline(' '.join(row))

    for col in cols:
        solver.sendline(' '.join(col))

    solver.shutdown()

    qr_text = []
    for i in range(0, len(rows)):
        solver.recvuntil('|')
        qr_text.append(solver.recvuntil('|')[:-1])

    #print qr_text

    size = 20
    image = Image.new('RGB', ((len(qr_text) * size), (len(qr_text[0]) * size) / 2))
    draw = ImageDraw.Draw(image)

    text = ''

    #print len(qr_text)
    #print len(qr_text[0])

    for i in range(0, len(qr_text)):
        for j in range(0, len(qr_text[0]) / 2):
            text += qr_text[i][j * 2]
            pos = ((j * size, i * size), (j * size + size, i * size + size))
            draw.rectangle(pos, 'black' if qr_text[i][j * 2] == '#' else 'white')
        text += '\n'

    #print text

    image.save('qrcode.png')


def get_qrcode():
    qr = qrtools.QR()
    qr.decode('qrcode.png')
    return qr.data

answer = ''
for i in range(0, 100):
    get_image(answer)
    answer = get_qrcode()
    print answer


