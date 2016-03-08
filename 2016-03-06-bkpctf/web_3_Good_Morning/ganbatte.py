#!/usr/bin/env python

from flask import Flask, render_template, Response
from flask_sockets import Sockets
import json
import MySQLdb

app = Flask(__name__)
sockets = Sockets(app)

with open("config.json") as f:
 connect_params = json.load(f)

connect_params["db"] = "ganbatte"

# Use Shift-JIS for everything so it uses less bytes
Response.charset = "shift-jis"
connect_params["charset"] = "sjis"

questions = [
  "name",
  "quest",
  "favorite color",
]

# List from http://php.net/manual/en/function.mysql-real-escape-string.php
MYSQL_SPECIAL_CHARS = [
  ("\\", "\\\\"),
  ("\0", "\\0"),
  ("\n", "\\n"),
  ("\r", "\\r"),
  ("'", "\\'"),
  ('"', '\\"'),
  ("\x1a", "\\Z"),
]
def mysql_escape(s):
  for find, replace in  MYSQL_SPECIAL_CHARS:
    s = s.replace(find, replace)
  return s

@sockets.route('/ws')
def process_questsions(ws):
  i = 0
  conn = MySQLdb.connect(**connect_params)
  with conn as cursor:
    ws.send(json.dumps({"type": "question", "topic": questions[i], "last": i == len(questions)-1}))
    while not ws.closed:
      message = ws.receive()
      if not message: continue
      message = json.loads(message)
      if message["type"] == "answer":
        question = mysql_escape(questions[i])
        answer = mysql_escape(message["answer"])
        cursor.execute('INSERT INTO answers (question, answer) VALUES ("%s", "%s")' % (question, answer))
        conn.commit()
        i += 1
        if i < len(questions):
          ws.send(json.dumps({"type": "question", "topic": questions[i], "last": i == len(questions)-1}))
      elif message["type"] == "get_answer":
        question = mysql_escape(message["question"])
        answer = mysql_escape(message["answer"])
        cursor.execute('SELECT * FROM answers WHERE question="%s" AND answer="%s"' % (question, answer))
        ws.send(json.dumps({"type": "got_answer", "row": cursor.fetchone()}))
      print message

@app.route('/')
def hello():
  return app.send_static_file("index.html")

if __name__ == "__main__":
  from gevent import pywsgi
  from geventwebsocket.handler import WebSocketHandler
  addr = ('localhost', 5000)

  server = pywsgi.WSGIServer(addr, app, handler_class=WebSocketHandler)
  server.serve_forever()
