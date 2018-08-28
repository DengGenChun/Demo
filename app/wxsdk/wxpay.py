# encoding = utf-8

import time
import string
import random
import requests
import hashlib
from flask import request
from app.wxsdk.base import WXError
from xml.etree import cElementTree as ET

__all__ = ("WXPayError", "WXPay")

SUCCESS = 'SUCCESS'
FAIL = 'FAIL'


class WXPayError(WXError):
    def __init__(self, msg):
        super(WXPayError, self).__init__(msg)


class WXPay(object):
    """
    支付API: https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_1
    """
    PAY_HOST = "https://api.mch.weixin.qq.com"

    def __init__(self, app_id, mch_id, mch_key, notify_url, key=None, cert=None):
        self.app_id = app_id
        self.mch_id = mch_id
        self.mch_key = mch_key
        self.notify_url = notify_url
        self.key = key
        self.cert = cert
        self.sess = requests.Session()

    def unified_order(self, **data):
        """
        统一下单
        out_trade_no、body、total_fee、trade_type必填
        app_id, mchid, nonce_str, sign自动填写
        spbill_create_ip 在flask框架下可以自动填写, 非flask框架需要主动传入此参数
        """
        url = self.PAY_HOST + '/pay/unifiedorder'

        # 必填参数
        if "out_trade_no" not in data:
            raise WXPayError("缺少统一支付接口必填参数out_trade_no")
        if "body" not in data:
            raise WXPayError("缺少统一支付接口必填参数body")
        if "total_fee" not in data:
            raise WXPayError("缺少统一支付接口必填参数total_fee")
        if "trade_type" not in data:
            raise WXPayError("缺少统一支付接口必填参数trade_type")

        # 关联参数
        if data["trade_type"] == "JSAPI" and "openid" not in data:
            raise WXPayError("trade_type为JSAPI时，openid为必填参数")
        if data["trade_type"] == "NATIVE" and "product_id" not in data:
            raise WXPayError("trade_type为NATIVE时，product_id为必填参数")
        data.setdefault('notify_url', self.notify_url)
        if "spbill_create_ip" not in data:
            data.setdefault('spbill_create_ip', self.remote_addr)

        return self._fetch(url, data)

    def jsapi(self, **kwargs):
        """
        生成给JavaScript调用的数据
        详细规则参考 https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=7_7&index=6
        """
        kwargs.setdefault('trade_type', 'JSAPI')

        raw = self.unified_order(**kwargs)
        package = 'prepay_id={0}'.format(raw['prepay_id'])
        timestamp = str(int(time.time()))
        nonce_str = self.nonce_str
        data = {
            "appId": self.app_id,
            "timeStamp": timestamp,
            "nonceStr": nonce_str,
            "package": package,
            "signType": 'MD5',
        }
        sign = self.sign(data)
        data.setdefault("paySign", sign)

        return data

    def order_query(self, **data):
        """
        订单查询
        transaction_id, out_trade_no 至少填一个
        """
        url = self.PAY_HOST + "/pay/orderquery"

        if "transaction_id" not in data and "out_trade_no" not in data:
            raise WXPayError("订单查询接口中，out_trade_no、transaction_id至少填一个")
        return self._fetch(url, data)

    def close_order(self, out_trade_no, **data):
        """
        关闭订单
        out_trade_no 必填
        """
        url = self.PAY_HOST + "/pay/closeorder"

        data.setdefault("out_trade_no", out_trade_no)
        return self._fetch(url, data)

    def refund(self, **data):
        """
        申请退款
        out_trade_no、transaction_id 至少填一个
        out_refund_no、total_fee、refund_fee、op_user_id 为必填参数
        """
        url = self.PAY_HOST + "/secapi/pay/refund"

        if not self.key or not self.cert:
            raise WXPayError("退款申请接口需要双向证书")
        if "out_trade_no" not in data and "transaction_id" not in data:
            raise WXPayError("退款申请接口中，out_trade_no、transaction_id至少填一个")
        if "out_refund_no" not in data:
            raise WXPayError("退款申请接口中，缺少必填参数out_refund_no")
        if "total_fee" not in data:
            raise WXPayError("退款申请接口中，缺少必填参数total_fee")
        if "refund_fee" not in data:
            raise WXPayError("退款申请接口中，缺少必填参数refund_fee")

        return self._fetch(url, data, True)

    def refund_query(self, **data):
        """
        查询退款
        提交退款申请后，通过调用该接口查询退款状态。退款有一定延时，
        用零钱支付的退款20分钟内到账，银行卡支付的退款3个工作日后重新查询退款状态。

        out_refund_no、out_trade_no、transaction_id、refund_id 四个参数必填一个
        """
        url = self.PAY_HOST + "/pay/refundquery"
        if "out_refund_no" not in data and "out_trade_no" not in data \
                and "transaction_id" not in data and "refunc_id" not in data:
            raise WXPayError("退款查询接口中，out_refund_no、out_trade_no、transaction_id、refund_id四个参数必填一个")

        return self._fetch(url, data)

    def download_bill(self, bill_date, bill_type="ALL", **data):
        """
        下载对账单
        bill_date、bill_type 为必填参数
        """
        url = self.PAY_HOST + "/pay/downloadbill"
        data.setdefault("bill_date", bill_date)
        data.setdefault("bill_type", bill_type)

        return self._fetch(url, data)

    @property
    def remote_addr(self):
        return request.remote_addr

    @property
    def nonce_str(self):
        chars = string.ascii_letters + string.digits
        return "".join(random.choice(chars) for _ in range(32))

    def sign(self, dic):
        """
        生成签名
        详细规则参考:https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=4_3
        """
        s = ['{}={}'.format(key, dic[key]) for key in sorted(dic.keys()) if key != 'appkey']
        s = '&'.join(s)
        s = s + '&key=' + self.mch_key
        return hashlib.md5(s.encode('utf-8')).hexdigest().upper()

    def check_sign(self, dic):
        sign = dic.pop('sign')
        return sign == self.sign(dic)

    def to_xml(self, dic):
        s = ''
        for k, v in dic.items():
            s += "<{0}>{1}</{0}>".format(k, v)
        s = "<xml>{0}</xml>".format(s)
        return s.encode('utf-8')

    def to_dict(self, xml):
        dic = {}
        root = ET.fromstring(xml)
        for child in root:
            key = child.tag
            value = child.text
            dic[key] = value
        return dic

    def _fetch(self, url, data, use_cert=False):
        data.setdefault('appid', self.app_id)
        data.setdefault('mch_id', self.mch_id)
        data.setdefault('nonce_str', self.nonce_str)
        data.setdefault('sign', self.sign(data))

        if use_cert:
            resp = self.sess.post(url, data=self.to_xml(data), cert=(self.cert, self.key))
        else:
            resp = self.sess.post(url, data=self.to_xml(data))

        content = resp.content.decode('utf-8')
        if 'return_code' in content:
            data = self.to_dict(content)
            if data['return_code'] == FAIL:
                raise WXPayError(data['return_msg'])
            if 'result_code' in content and data['result_code'] == FAIL:
                raise WXPayError(data['err_code_des'])
            return data
        return content

    def reply(self, msg, ok=True):
        code = SUCCESS if ok else FAIL
        return self.to_xml(dict(return_code=code, return_msg=msg))
