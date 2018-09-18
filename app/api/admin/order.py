# encoding = utf-8

from flask import request

from app import db
from app import utils
from app.api.admin import bp
from app.decor import admin_required
from app.models import Order
from app.models import Product


@bp.route('/listOrder', methods=['GET'])
@admin_required
def list_order():
    p_id = request.args.get('p_id')
    if p_id:
        product = Product.query.filter_by(p_id=p_id).first()
        if product:
            return utils.ret_objs(product.orders)
        return utils.ret_err(-1, "p_id is wrong")

    stat = Order.query

    order_no = request.args.get('order_no')
    if order_no:
        stat = stat.filter_by(order_no=order_no)

    track_no = request.args.get('track_no')
    if track_no:
        stat = stat.filter_by(track_no=track_no)
    track_code = request.args.get('track_code')
    if track_code:
        stat = stat.filter_by(track_code=track_code)
    promotion_path = request.args.get('promotion_path')
    if promotion_path:
        stat = stat.filter(Order.promotion_path.like('%' + promotion_path + '%'))
    username = request.args.get('username')
    if username:
        stat = stat.filter(Order.username.like('%' + username + '%'))
    phone = request.args.get('phone')
    if phone:
        stat = stat.filter(Order.phone.like('%' + phone + '%'))
    address = request.args.get('address')
    if address:
        stat = stat.filter(Order.address.like('%' + address + '%'))
    comment = request.args.get('comment')
    if comment:
        stat = stat.filter(Order.comment.like('%' + comment + '%'))
    trade_state = request.args.get('trade_state')
    if trade_state:
        stat = stat.filter(Order.trade_state.like('%' + trade_state + '%'))
    track_state = request.args.get('track_state')
    if track_state:
        stat = stat.filter(Order.track_state.like('%' + track_state + '%'))
    kjyp_state = request.args.get('kjyp_state')
    if kjyp_state:
        stat = stat.filter(Order.kjyp_state.like('%' + kjyp_state + '%'))

    order_by_time = request.args.get("order_by_time")
    if order_by_time:
        if order_by_time == "asc":
            stat = stat.order_by(Order.create_time.asc())
        else:
            stat = stat.order_by(Order.create_time.desc())

    return utils.ret_objs(stat.all())


@bp.route('/updateOrder', methods=['GET'])
@admin_required
def update_order():
    order_no = request.args.get('order_no')
    if order_no is None or order_no == '':
        return utils.ret_err(-1, "order_no is required")
    order = Order.query.filter_by(order_no=order_no).first()
    if order is None:
        return utils.ret_err(-1, "Order doesn't exists")

    params = {}
    track_no = request.args.get('track_no')
    if track_no:
        params["track_no"] = track_no
    track_state = request.args.get('track_state')
    if track_state:
        params["track_state"] = track_state
    kjyp_state = request.args.get('kjyp_state')
    if kjyp_state:
        params["kjyp_state"] = kjyp_state

    if bool(params):
        Order.query.filter_by(order_no=order_no).update(params)
        db.session.commit()
        return utils.ret_msg_objs("Success", order)
    return utils.ret_msg("Nothing happen")
