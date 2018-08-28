# encoding = utf-8

from app import app


@app.route('/VwqXrMRgdzjBpP69cSt6LhLHYAwCwyFL', methods=['GET'])
def home():
    return app.send_static_file('home.html')
