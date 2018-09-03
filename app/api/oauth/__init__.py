# encoding = utf-

from flask import Blueprint

bp = Blueprint('api.oauth', __name__, url_prefix='/api/oauth')

from app.api.oauth import weixin