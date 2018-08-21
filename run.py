# encoding = utf-8

from app import app


PORT = app.config['PORT']
app.run(port=PORT)

