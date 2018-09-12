# encoding = utf-8

from app.decor import wx_login_required
from app import app
from flask import request


@app.route('/VwqXrMRgdzjBpP69cSt6LhLHYAwCwyF', methods=['GET'])
@wx_login_required
def promotion():
    return app.send_static_file('promotion.html')


@app.route('/order_list.html', methods=['GET'])
@app.route('/order_detail.html', methods=['GET'])
@app.route('/trade_result.html', methods=['GET'])
@wx_login_required
def _hook():
    return app.send_static_file(request.path[1:])


@app.route('/scss/<path:path>')
def dont_send_scss(path):
    return '404'
