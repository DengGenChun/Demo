# encoding = utf-8

from flask import Blueprint

bp = Blueprint('order', __name__, url_prefix='/order')

from app.order import routes

