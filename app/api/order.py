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
        return utils.ret_err(-1, '无效的商品')
    if product.inventory < 1:
        return utils.ret_err(-1, '库存不足')

    p_count = request.args.get('p_count', 0, int)
    if p_count <= 0:
        return utils.ret_err(-1, '商品数量必须大于0')
    if p_count > product.inventory:
        return utils.ret_err(-1, '库存不足')

    username = request.args.get('username', '')
    if username == '' or len(username) > 16:
        return utils.ret_err(-1, '姓名为空或过长')
    phone = request.args.get('phone', '')
    if phone == '' or len(phone) > 16:
        return utils.ret_err(-1, '手机号为空或过长')
    address = request.args.get('address', '')
    if address == '' or len(address) > 128:
        return utils.ret_err(-1, '收货地址为空或过长')
    raw_address = request.args.get('raw_address', '')
    if raw_address == '' or len(raw_address) > 128:
        return utils.ret_err(-1, 'raw收货地址为空或过长')
    record_address = request.args.get("record_address", '')
    if record_address == '' or not (record_address == "YES" or record_address == "NO"):
        record_address = "NO"
    comment = request.args.get('comment', '')
    if len(comment) > 128:
        return utils.ret_err(-1, '留言过长')
    postcode = request.args.get('postcode', '')
    if len(postcode) > 8:
        return utils.ret_err(-1, '邮政编码过长')
    promotion_path = request.args.get("promotion_path", '')
    if len(promotion_path) > 64:
        return utils.ret_err(-1, 'promotion_path is too long')

    order = Order(p_id, p_count, username, phone, address, raw_address, comment)
    order.price_sum = p_count * product.price
    order.postcode = postcode
    order.record_address = record_address
    order.promotion_path = promotion_path
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
        return utils.ret_err(-1, str(e))

    db.session.add(order)
    db.session.commit()

    obj = {
        "data": raw,
        "order_no": str(order.order_no)
    }
    return utils.ret_objs(obj)


@bp.route('/notifyOrder', methods=['POST'])
def notify_order():
    """
    微信支付结果回调
    """
    dic = wxsdk.to_dict(request.data)
    if dic['return_code'] == "FAIL":
        return wxsdk.reply("支付失败", False)

    out_trade_no = dic["out_trade_no"]
    order = Order.query.filter_by(order_no=int(out_trade_no)).first()
    if order.notify_state == "CHECKED":
        # 支付结果已经成功接收到并处理
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
    """
    验证订单
    向微信请求验证订单的状态
    :param order_no: 订单号
    :return: True if 支付成功, False if 支付失败
    """
    order = Order.query.filter_by(order_no=order_no).first()
    if order is None:
        return False
    if order.trade_state == "SUCCESS":
        # 已经支付成功直接返回, 避免再次发送请求验证订单
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
        # 支付失败
        db.session.commit()
        return False

    # 支付成功
    order.transaction_id = data["transaction_id"]
    order.pay_time = utils.str2timestamp(data["time_end"])
    order.product.inventory -= order.p_count
    order.product.sale_count += order.p_count
    db.session.commit()
    return True


@bp.route('/listOrder', methods=['GET'])
def list_order():
    """
    查询订单
    @args: trade_state 订单状态[SUCCESS, NOTPAY] 详见https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_2
    @args: order_by_time 按时间排序[asc, desc], 默认是 desc
    :return:
    """
    openid = request.cookies.get("openid")
    if not openid:
        openid = request.args.get("openid")
        if not openid:
            return utils.ret_err(-1, "ERR_INVALID_OPENID")

    stat = Order.query.filter_by(openid=openid)

    order_no = request.args.get('order_no', '')
    if order_no:
        stat = stat.filter_by(order_no=order_no)
        _order = stat.first()
        if _order is None:
            return utils.ret_err(-1, '订单不存在')
        if not verify_order(order_no):
            return utils.ret_err(-1, _order.trade_state_desc)

    trade_state = request.args.get('trade_state')
    if trade_state:
        stat = stat.filter_by(trade_state=trade_state)
    order_by_time = request.args.get("order_by_time")
    if order_by_time:
        if order_by_time == "asc":
            stat = stat.order_by(Order.create_time.asc())
        else:
            stat = stat.order_by(Order.create_time.desc())

    objs = []
    orders = stat.all()
    for order in orders:
        p = order.product
        obj = {
            "order_no": str(order.order_no),
            "p_id": str(p.p_id),
            "transaction_id": order.transaction_id,
            "promotion_path": order.promotion_path,
            "p_name": p.name,
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
            "raw_address": order.raw_address,
            "record_address": order.record_address,
            "comment": order.comment,
            "order_time": order.create_time,
            "pay_time": order.pay_time,
            "track_no": order.track_no,
            "track_state": order.track_state,
            "track_time": order.track_time,
            "is_sign": order.is_sign,
            "sign_time": order.sign_time,
            "postcode": order.postcode
        }
        objs.append(obj)

    return utils.ret_objs(objs)
