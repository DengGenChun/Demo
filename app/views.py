# encoding = utf-8

from app.decor import wx_login_required
from app import app
from flask import request
from app.models import Product
from app import utils


@app.route('/VwqXrMRgdzjBpP69cSt6LhLHYAwCwyFA', methods=['GET'])
@wx_login_required
def VwqXrMRgdzjBpP69cSt6LhLHYAwCwyFA():
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


@app.route('/VwqXrMRgdzjBpP69cSt6LhLHYAwCwyFA.json', methods=['GET'])
def VwqXrMRgdzjBpP69cSt6LhLHYAwCwyFA_json():
    p_id1 = 657153685373696368
    p_id2 = 852153686806096018
    products = Product.query.filter(Product.p_id.in_([p_id1, p_id2])).all()

    ary = []
    for product in products:
        ary.append(product.asdict())

    obj = {
        "first_image": "file/W1_F_01.jpg",
        "detail_image": [
            "file/W1_01.jpg",
            "file/W1_02.jpg"
        ],
        "products": ary
    }
    return utils.ret_objs(obj)
