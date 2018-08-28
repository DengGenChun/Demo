# encoding = utf-8

from flask import Blueprint

bp = Blueprint('oauth', __name__, url_prefix='/oauth')

from app.oauth import routes