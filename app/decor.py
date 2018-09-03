# encoding = utf-8

from functools import wraps

from flask import request, redirect, url_for

from app import USR, PWD
from app.utils import md5


def wx_login_required(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        openid = request.cookies.get("openid")
        if openid:
            return func(*args, **kwargs)
        url = url_for("api.oauth.wx_login", next=request.url, _external=True)
        return redirect(url)
    return wrapper_func


def admin_required(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        usr = request.args.get('usr', '')
        pwd = request.args.get('pwd', '')
        if usr == USR and md5(pwd) == PWD:
            return func(*args, **kwargs)
        return '<h1>404</h1>'
    return wrapper_func