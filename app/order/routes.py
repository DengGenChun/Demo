# encoding = utf-8

from flask import request
from app import db, utils, wxsdk
from app.order import bp
from app.models import Order, Product
from app.wxsdk.wxpay import WXPayError
import logging


@bp.route('/testPost', methods=['POST'])
def testPost():
    xml = str(request.get_data(), encoding="utf-8")
    print("xml:")
    print(xml)
    return 'Success'


@bp.route('/createOrder', methods=['GET'])
def create_order():
    openid = request.cookies.get("openid")
    if not openid:
        return utils.ret_err(-1, "ERR_INVALID_OPENID")

    p_id = request.args.get('p_id')
    product = Product.query.filter_by(p_id=p_id).first()
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

    data = dict()
    try:
        data = wxsdk.order_query(out_trade_no=order_no)
    except WXPayError as e:
        logging.warning("verifyOrder: order_no=%s; errmsg=%s" % (order_no, str(e)))
        return False

    order.trade_state = data["trade_state"]
    db.session.commit()
    if order.trade_state != "SUCCESS":
        return False

    return True


@bp.route('/list', methods=['GET'])
@utils.check_admin
def list_order():
    order_no = request.args.get('order_no')
    if order_no is None or order_no == '':
        return utils.ret_err(-1, "order_no is required")
    order = Order.query.filter_by(order_no=order_no).first()
    return utils.ret_objs(order)


@bp.route('/listAll', methods=['GET'])
@utils.check_admin
def list_all_order():
    filters = dict()

    trade_state = request.args.get('trade_state')
    if trade_state:
        filters['trade_state'] = trade_state

    orders = Order.query.filter_by(**filters).all()
    return utils.ret_objs(orders)


@bp.route('/listProduct', methods=['GET'])
@utils.check_admin
def list_product_by_order_no():
    order_no = request.args.get('order_no')
    if order_no is None or order_no == '':
        return utils.ret_err(-1, "order_no is required")
    order = Order.query.filter_by(order_no=order_no).first()
    if order is not None:
        return utils.ret_objs(order.product)
    return utils.ret_err(-1, "Order doesn't exists")


@bp.route('orderSuccess', methods=['GET'])
def order_success():
    order_no = request.args.get('order_no', '')
    order = Order.query.filter_by(order_no=order_no).first()
    if order is None:
        return utils.ret_err(-1, 'order_no is worng')

    if order.trade_state != "SUCCESS":
        if not verify_order(order_no):
            return "<h2>交易失败</h2>"

    p = order.product
    return """
    <h2>交易成功</h2>
    <div>商品名称：<span>{0}</span></div>
    <div>商品详情：<span>{1}</span></div>
    <div>商品单价：<span>{2}</span></div>
    <div>商品数量：<span>{3}</span></div>
    <div>总价格：<span>{4}</span></div>
    <div>姓名：<span>{5}</span></div>
    <div>手机号：<span>{6}</span></div>
    <div>收货地址：<span>{7}</span></div>
    <div>留言：<span>{8}</span></div>
    """.format(p.title, p.detail, p.price, order.p_count, order.price_sum, order.username, order.phone, order.address, order.comment)


@bp.route('orderFail', methods=['GET'])
def order_fail():
    return "<h2>交易失败</h2>"
