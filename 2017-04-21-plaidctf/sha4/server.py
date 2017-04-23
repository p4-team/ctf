from flask import Flask, render_template, request, render_template_string
from pyasn1.codec.ber.decoder import decode
from pyasn1.type.univ import OctetString
from urllib2 import urlopen
from sha4 import hash
import string

app = Flask(__name__)
bad     = """
<h2>yo that comment was bad, we couldn't parse it</h2>"""
unsafe  = """
<h2>that comment decoded to some weird junk</h2>"""
comment = """
<h2>Thank you for your SHA-4 feedback. Your comment, %s, is very important to us</h2>"""

def is_unsafe(s):
  for c in s:
    if c not in (string.ascii_letters + string.digits + " ,.:()?!-_'+=[]\t\n<>"):
      return True
  return False

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/comments", methods=['POST'])
def comments():
  try:
    encoded = request.form['comment']
    encoded.replace("\n","\r")
    ber = encoded.decode("hex")
  except TypeError:
    return render_template_string(bad)
  f = "/var/tmp/comments/%s.txt"%hash(ber).encode("hex")
  
  out_text = str(decode(ber))
  open(f, "w").write(out_text)

  if is_unsafe(out_text):
    return render_template_string(unsafe)

  commentt = comment % open(f).read()
  return render_template_string(commentt, comment=out_text.replace("\n","<br/>"))

@app.route("/upload", methods=['POST'])
def upload():
  try:
    comment = urlopen(request.form['url']).read(1024*1024)
    open("/var/tmp/comments/%s.file"%hash(comment).encode("hex"), "w").write(comment)
    return comment
  except:
    return render_template_string(bad)

if __name__ == "__main__":
  app.run()