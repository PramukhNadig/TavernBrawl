from gevent import monkey
# Monkey-patching standart Python library for async working
monkey.patch_all()
from gevent.pywsgi import WSGIServer
from flask import Flask
from threading import Thread

app = Flask('')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def home():
    return "Battle ready \n - - Tavern initiated - - \n Enabled!"

def run():
  http_server = WSGIServer(('0.0.0.0', 8080), app)
  http_server.serve_forever()

def keep_alive():
    t = Thread(target=run)
    t.start()
