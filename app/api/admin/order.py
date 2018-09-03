# encoding = utf-8

from flask import request

from app import utils
from app.api.admin import bp
from app.decor import admin_required
from app.models import Order
from app.models import Product


@bp.route('/listOrder', methods=['GET'])
@admin_required
def list_order():
    order_no = request.args.get('order_no')
    if order_no:
        order = Order.query.filter_by(order_no=order_no).first()
        return utils.ret_objs(order)

    p_id = request.args.get('p_id')
    if p_id:
        product = Product.query.filter_by(p_id=p_id).first()
        if product:
            return utils.ret_objs(product.orders)
        return utils.ret_err(-1, "p_id is wrong")

    return utils.ret_err(-1, "order_no or p_id is required")


@bp.route('/listAllOrder', methods=['GET'])
@admin_required
def list_all_order():
    filters = dict()

    trade_state = request.args.get('trade_state')
    if trade_state:
        filters['trade_state'] = trade_state

    orders = Order.query.filter_by(**filters).all()
    return utils.ret_objs(orders)
