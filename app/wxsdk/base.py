# encoding = utf-8


class WXError(Exception):
    def __init__(self, msg):
        super(WXError, self).__init__(msg)
