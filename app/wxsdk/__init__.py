# encoding = utf-8

from .base import WXError
from .wxlogin import WXLogin
from .wxpay import WXPay

__all__ = "WXSDK"


class WXSDK(WXLogin, WXPay):
    """
    微信SDK
    """
    def __init__(self, config=None):
        if config is not None:
            self.config = config
            self.init(config)

    def init(self, config):
        self.config = config

        app_id = config.get("WX_APP_ID")
        app_secret = config.get("WX_APP_SECRET")
        mch_id = config.get("WX_MCH_ID")
        mch_key = config.get("WX_MCH_KEY")
        mch_key_file = config.get("WX_MCH_KEY_FILE")
        mch_cert_file = config.get("WX_MCH_CERT_FILE")
        notify_url = config.get("WX_NOTIFY_URL")

        if app_id and app_secret:
            WXLogin.__init__(self, app_id, app_secret)
        if app_id and mch_id and mch_key and notify_url:
            WXPay.__init__(self, app_id, mch_id, mch_key, notify_url, mch_key_file, mch_cert_file)
