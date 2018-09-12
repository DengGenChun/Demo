# encoding = utf-8

import logging

from flask import request

from app import db, utils, wxsdk
from app.api import bp
from app.models import Order, Product
from app.wxsdk.wxpay import WXPayError


@bp.route('/createOrder', methods=['GET'])
def create_order():
    """
    @api {GET} /api/createOrder 创建订单
    @apiDescription 创建订单，生成并返回调用 jsapi 所需要的数据
    @apiPermission 要求当前用户已经微信登录
    @apiGroup Order
    @apiVersion 1.0.0
    @apiParam {Integer} p_id 商品id
    @apiParam {Integer} p_count 商品数量
    @apiParam {String} username 用户名
    @apiParam {String} phone 用户的手机号
    @apiParam {String} address 用户的收货地址
    @apiParam {String} [comment] 用户留言
    @apiExample {js} 用法:
    /api/createOrder?p_id=xxx&p_count=1&username=xxx&phone=13712341234&address=xxx&comment=xxx
    @apiSuccess {Integer} code 0 代表成功, -1 代表失败
    @apiSuccess {Json} data 调用jsapi所需要的数据
    @apiSuccess {String} order_no 订单号
    @apiSuccessExample {json} 返回结果:
    {
        "code": 0,
        "data": {
            "appId": "xxx",
            "timeStamp": "1536042748",
            "nonceStr": "xxx",
            "package": "prepay_id=xxx",
            "signType": "MD5",
            "paySign": "XXX"
        },
        "order_no": "xxx"
    }
    """
    openid = request.cookies.get("openid")
    if not openid:
        openid = request.args.get("openid")
        if not openid:
            return utils.ret_err(-1, "ERR_INVALID_OPENID")

    p_id = request.args.get('p_id')
    product = Product.query.filter_by(p_id=p_id).first()
    if product is None:
        return utils.ret_err(-1, 'p_id is wrong')
    if product.inventory < 1:
        return utils.ret_err(-1, '库存不足')

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
    order.trade_state = "NOTPAY"
    order.trade_type = "JSAPI"
    order.openid = openid

    data = dict()
    data["openid"] = openid
    data["out_trade_no"] = str(order.order_no)
    data["body"] = product.title
    data["total_fee"] = int(order.price_sum * 100)
    data["trade_type"] = order.trade_type

    raw = dict()
    try:
        raw = wxsdk.jsapi(**data)
    except WXPayError as e:
        logging.warning("createOrder: openid=%s, errmsg=%s" % (openid, str(e)))
        return utils.ret_err(-1, "createOrder: errmsg=%s" % str(e))

    db.session.add(order)
    db.session.commit()

    obj = {
        "data": raw,
        "order_no": str(order.order_no)
    }
    return utils.ret_objs(obj)


@bp.route('/notifyOrder', methods=['POST'])
def notify_order():
    dic = wxsdk.to_dict(request.data)
    if dic['return_code'] == "FAIL":
        return wxsdk.reply("支付失败", False)

    out_trade_no = dic["out_trade_no"]
    order = Order.query.filter_by(order_no=int(out_trade_no)).first()
    if order.notify_state == "CHECKED":
        return wxsdk.reply("OK")

    if not wxsdk.check_sign(dic):
        return wxsdk.reply("签名错误", False)
    if (order.price_sum * 100) != int(dic["total_fee"]):
        return wxsdk.reply("金额不对应", False)

    order.notify_state = "CHECKED"
    db.session.commit()
    verify_order(out_trade_no)

    return wxsdk.reply("OK")


def verify_order(order_no):
    order = Order.query.filter_by(order_no=order_no).first()
    if order is None:
        return False
    if order.trade_state == "SUCCESS":
        return True

    data = dict()
    try:
        data = wxsdk.order_query(out_trade_no=order_no)
    except WXPayError as e:
        logging.warning("verifyOrder: order_no=%s; errmsg=%s" % (order_no, str(e)))
        return False

    order.trade_state = data["trade_state"]
    order.trade_state_desc = data["trade_state_desc"]
    if order.trade_state != "SUCCESS":
        db.session.commit()
        return False

    order.transaction_id = data["transaction_id"]
    order.pay_time = utils.str2timestamp(data["time_end"])
    order.product.inventory -= 1
    db.session.commit()
    return True


@bp.route('/listOrder', methods=['GET'])
def list_order():
    openid = request.cookies.get("openid")
    if not openid:
        openid = request.args.get("openid")
        if not openid:
            return utils.ret_err(-1, "ERR_INVALID_OPENID")

    order_no = request.args.get('order_no', '')
    order = Order.query.filter_by(order_no=order_no, openid=openid).first()
    if order is None:
        return utils.ret_err(-1, 'order_no is wrong')

    if not verify_order(order_no):
        return utils.ret_err(-1, order.trade_state_desc)

    p = order.product
    obj = {
        "order_no": str(order.order_no),
        "transaction_id": order.transaction_id,
        "p_title": p.title,
        "p_detail": p.detail,
        "p_price": p.price,
        "p_color": p.color,
        "p_icon": p.icon,
        "p_count": order.p_count,
        "price_sum": order.price_sum,
        "username": order.username,
        "phone": order.phone,
        "address": order.address,
        "comment": order.comment,
        "order_time": order.create_time,
        "pay_time": order.pay_time
    }
    return utils.ret_objs(obj)


@bp.route('/listAllOrder', methods=['GET'])
def list_all_order():
    openid = request.cookies.get("openid")
    if not openid:
        openid = request.args.get("openid")
        if not openid:
            return utils.ret_err(-1, "ERR_INVALID_OPENID")

    filters = dict()
    filters.setdefault("openid", openid)

    trade_state = request.args.get('trade_state')
    if trade_state:
        filters['trade_state'] = trade_state

    stat = Order.query.filter_by(**filters)
    order_by_time = request.args.get("order_by_time")
    if order_by_time:
        if order_by_time == "asc":
            stat = stat.order_by(Order.create_time.asc())
        elif order_by_time == "desc":
            stat = stat.order_by(Order.create_time.desc())

    objs = []
    orders = stat.all()
    for order in orders:
        p = order.product
        obj = {
            "order_no": str(order.order_no),
            "transaction_id": order.transaction_id,
            "p_title": p.title,
            "p_detail": p.detail,
            "p_price": p.price,
            "p_color": p.color,
            "p_icon": p.icon,
            "p_count": order.p_count,
            "price_sum": order.price_sum,
            "username": order.username,
            "phone": order.phone,
            "address": order.address,
            "comment": order.comment,
            "order_time": order.create_time,
            "pay_time": order.pay_time
        }
        objs.append(obj)

    return utils.ret_objs(objs)
