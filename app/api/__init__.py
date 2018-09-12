# encoding = utf-8

from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api')

from app.api import admin
from app.api import oauth
from app.api import order
from app.api import sf_query
