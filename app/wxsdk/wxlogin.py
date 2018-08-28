# encoding = utf-8

import json
import requests
from app.wxsdk.base import WXError


class WXLoginError(WXError):
    def __init__(self, msg):
        super(WXLoginError, self).__init__(msg)


class WXLogin(object):
    """
    微信网页授权API
    https://mp.weixin.qq.com/wiki?action=doc&id=mp1421140842&t=0.9481976669034491&token=&lang=zh_CN
    """

    def __init__(self, app_id, app_secret):
        self.sess = requests.Session()
        self.app_id = app_id
        self.app_secret = app_secret

    def _get(self, url, params):
        resp = self.sess.get(url, params=params)
        data = json.loads(resp.content.decode('utf-8'))
        if data.get('errcode'):
            msg = "%(errcode)d %(errmsg)s" % data
            raise WXLoginError(msg)
        return data

    def authorize(self, redirect_uri, scope="snsapi_base", state=None):
        """
        生成微信认证地址并且跳转

        :param redirect_uri: 跳转地址
        :param scope: 微信认证方式，有`snsapi_base`和`snsapi_userinfo`两种
        :param state: 认证成功后会原样带上此字段
        """
        url = "https://open.weixin.qq.com/connect/oauth2/authorize"
        assert scope in ["snsapi_base", "snsapi_userinfo"]
        data = dict()
        data.setdefault("appid", self.app_id)
        data.setdefault("redirect_uri", redirect_uri)
        data.setdefault("response_type", "code")
        data.setdefault("scope", scope)
        if state:
            data.setdefault("state", state)
        data = [(k, data[k]) for k in sorted(data.keys()) if data[k]]
        s = "&".join("=".join(kv) for kv in data if kv[1])
        return "{0}?{1}#wechat_redirect".format(url, s)

    def access_token(self, code):
        """
        获取令牌

        :param code: code作为换取access_token的票据，每次用户授权带上的code将不一样，
                     code只能使用一次，5分钟未被使用自动过期
        """
        url = "https://api.weixin.qq.com/sns/oauth2/access_token"
        args = dict()
        args.setdefault("appid", self.app_id)
        args.setdefault("secret", self.app_secret)
        args.setdefault("code", code)
        args.setdefault("grant_type", "authorization_code")

        return self._get(url, args)

    def refresh_token(self, refresh_token):
        """
        刷新 access_token

        :param refresh_token: 获取 access_token 时得到的 refresh_token
        """
        url = "https://api.weixin.qq.com/sns/oauth2/refresh_token"
        args = dict()
        args.setdefault("appid", self.app_id)
        args.setdefault("grant_type", "refresh_token")
        args.setdefault("refresh_token", refresh_token)

        return self._get(url, args)

    def userinfo(self, access_token, openid):
        """
        获取用户信息
        如果网页授权作用域为snsapi_userinfo，则此时开发者可以通过access_token和openid拉取用户信息了

        :param access_token: 令牌
        :param openid:       用户的唯一标识
        """
        url = "https://api.weixin.qq.com/sns/userinfo"
        args = dict()
        args.setdefault("access_token", access_token)
        args.setdefault("openid", openid)
        args.setdefault("lang", "zh_CN")

        return self._get(url, args)

    def auth(self, access_token, openid):
        """
        检验授权凭证

        :param access_token: 网页授权接口调用凭证
        :param openid: 用户的唯一标识
        """
        url = "https://api.weixin.qq.com/sns/auth"
        args = dict()
        args.setdefault("access_token", access_token)
        args.setdefault("openid", openid)

        return self._get(url, args)

    def jscode2session(self, js_code):
        """
        小程序获取 session_key 和 openid
        :param js_code: 登录时获取的 code
        """
        url = "https://api.weixin.qq.com/sns/jscode2session"
        args = dict()
        args.setdefault("appid", self.app_id)
        args.setdefault("secret", self.app_secret)
        args.setdefault("js_code", js_code)
        args.setdefault("grant_type", "authorization_code")

        return self._get(url, args)
