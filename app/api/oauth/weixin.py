# encoding = utf-8

from datetime import datetime, timedelta

from flask import request, redirect, url_for

from app import wxsdk
from app.api.oauth import bp


@bp.route('/wx_login')
def wx_login():
    openid = request.cookies.get("openid")
    next = request.args.get("next") or request.referrer or "/"
    if openid:
        return redirect(next)

    redirect_uri = url_for("api.oauth.wx_access_token", next=next, _external=True)
    url = wxsdk.authorize(redirect_uri, "snsapi_base")
    return redirect(url)


@bp.route('/wx_access_token')
def wx_access_token():
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
