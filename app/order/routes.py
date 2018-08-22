# encoding = utf-8

from flask import request
from app import db
from app import utils
from app.order import bp
from app.models import Order
from app.models import Product


@bp.route('/add', methods=['GET'])
def add():
    p_id = request.args.get('p_id')
    product = Product.query.filter_by(id=p_id).first()
    if product is None:
        return utils.ret_err(-1, 'p_id is wrong')
    p_count = request.args.get('p_count', 0, int)
    if p_count <= 0:
        return utils.ret_err(-1, 'p_count must > 0')
    username = request.args.get('username', '')
    if username == '':
        return utils.ret_err(-1, 'username is required')
    phone = request.args.get('phone', '')
    if phone == '':
        return utils.ret_err(-1, 'phone is required')
    address = request.args.get('address', '')
    if address == '':
        return utils.ret_err(-1, 'address is required')
    comment = request.args.get('comment', '')

    order = Order(p_id, p_count, username, phone, address, comment)
    order.price_sum = p_count * product.price
    db.session.add(order)
    db.session.commit()
    return utils.ret_objs(order)


@bp.route('/list/<string:order_no>', methods=['GET'])
def list_order(order_no):
    order = Order.query.filter_by(order_no=order_no).first()
    return utils.ret_objs(order)


@bp.route('/list', methods=['GET'])
def list_all_order():
    orders = Order.query.all()
    return utils.ret_objs(orders)


@bp.route('/<string:order_no>/listProduct', methods=['GET'])
def list_product_by_order_no(order_no):
    order = Order.query.filter_by(order_no=order_no).first()
    if order is not None:
        return utils.ret_objs(order.product)
    return utils.ret_err(-1, "Order doesn't exists")
