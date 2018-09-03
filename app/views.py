# encoding = utf-8

from app.decor import wx_login_required
from app import app


@app.route('/VwqXrMRgdzjBpP69cSt6LhLHYAwCwyF', methods=['GET'])
@wx_login_required
def home():
    return app.send_static_file('home.html')
