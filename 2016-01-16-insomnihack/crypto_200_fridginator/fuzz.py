import requests
import time

# food, kkkkkkkkkkkkkkk
payload = '13739ab125b0e528d608eb4c4e5bb184108bf9b47d5cf18a633384a5a5d6c09ab9719c83f5ab5c0751937a39150c920d'.decode('hex')

# food, kkkkkkkkkkkkkkkk
payload = '13739ab125b0e528d608eb4c4e5bb184c177a61b4512eecea5e60327325a8a1ba090d54455e4763aa8594ffa98763ff0'.decode('hex')

url = 'http://fridge.insomnihack.ch/search/'
cookies = {'sessionid': 'u5imy1qivt4geo7uk7fden4pqt7itosq'}

known = []

x = 0
while x < 256 * 256:
    i = x // 256
    j = x % 256
    payload = payload[:-2] + chr(i) + chr(j)
    print payload[-2:].encode('hex'),
    r = requests.get(url + payload.encode('hex'), cookies=cookies)
    text = r.text

    ignored = "<input type='hidden' name='csrfmiddlewaretoken' value='"
    if ignored not in text and text not in known:
        print 'MATCH', len(known)
        known.append(text)
        print
        print text.encode('utf-8')
    elif ignored in text:
        print 'csrf'
        x -= 1
    else:
        print 'known', known.index(text)
    x += 1
    time.sleep(1)

