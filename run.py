# encoding = utf-8

from app import app

HOST = app.config['HOST']
PORT = app.config['PORT']
app.run(host=HOST, port=PORT)

