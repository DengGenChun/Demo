# encoding = utf-8

from app.decor import wx_login_required
from app import app
from flask import request
from app.models import Product
from app import utils


@app.route('/VwqXrMRgdzjBpP69cSt6LhLHYAwCwyFA', methods=['GET'])
@app.route('/F6xHBqT3LlUhHmcj7PbkkuSYRfBYLsrd', methods=['GET'])
@app.route('/jYis4ENd3UjqcnkcknwYQ5PeKuj8DRBw', methods=['GET'])
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
    p_id1 = 852153686806096018
    p_id2 = 657153685373696368
    products = Product.query.filter(Product.p_id.in_([p_id1, p_id2])).all()

    ary = []
    for product in products:
        ary.append(product.asdict())

    obj = {
        "html_title": "",
        "first_image": "file/W1_F_01.jpg",
        "detail_image": [
            "file/W1_01.jpg",
            "file/W1_02.jpg",
            "file/W1_03.jpg"
        ],
        "products": ary
    }
    return utils.ret_objs(obj)


@app.route('/F6xHBqT3LlUhHmcj7PbkkuSYRfBYLsrd.json', methods=['GET'])
def F6xHBqT3LlUhHmcj7PbkkuSYRfBYLsrd_json():
    p_id1 = 613153727106665462
    products = Product.query.filter(Product.p_id.in_([p_id1])).all()

    ary = []
    for product in products:
        ary.append(product.asdict())

    obj = {
        "html_title": "",
        "first_image": "file/T1_F_01.jpg",
        "detail_image": [
            "file/T1_01.jpg",
            "file/T1_02.jpg",
            "file/T1_03.jpg"
        ],
        "products": ary
    }
    return utils.ret_objs(obj)


@app.route('/jYis4ENd3UjqcnkcknwYQ5PeKuj8DRBw.json', methods=['GET'])
def jYis4ENd3UjqcnkcknwYQ5PeKuj8DRBw_json():
    p_id1 = 722153723099865505
    p_id2 = 116153723136665511
    products = Product.query.filter(Product.p_id.in_([p_id1, p_id2])).all()

    ary = []
    for product in products:
        ary.append(product.asdict())

    obj = {
        "html_title": "",
        "first_image": "file/W1_F_01.jpg",
        "detail_image": [
            "file/W1_01.jpg",
            "file/W1_02.jpg",
            "file/W1_03.jpg"
        ],
        "products": ary
    }
    return utils.ret_objs(obj)