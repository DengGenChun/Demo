# encoding = utf-8

from flask import Blueprint

bp = Blueprint('api.admin', __name__, url_prefix='/api/admin')

from app.api.admin import order
from app.api.admin import product
