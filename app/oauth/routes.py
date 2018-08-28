# encoding = utf-8

from datetime import datetime, timedelta
from app import wxsdk
from app.oauth import bp
from flask import request, redirect, url_for


@bp.route('/login')
def login():
    openid = request.cookies.get("openid")
    next = request.args.get("next") or "/"
    if openid:
        return redirect(next)

    redirect_uri = url_for("oauth.access_token", next=next, _external=True)
    url = wxsdk.authorize(redirect_uri, "snsapi_base")
    return redirect(url)


@bp.route('/access_token')
def access_token():
    code = request.args.get("code")
    if not code:
        return "ERR_INVALID_CODE", 400
    data = wxsdk.access_token(code)
    openid = data["openid"]
    expires = datetime.now() + timedelta(days=1)
    next = request.args.get("next", "/")

    resp = redirect(next)
    resp.set_cookie("openid", openid, expires=expires)
    return resp
