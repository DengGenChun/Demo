# encoding = utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from app.wxsdk import WXSDK
import logging

# logging.basicConfig(filename="logger.log", level=logging.INFO)

app = Flask(__name__, instance_relative_config=True, static_url_path='')
app.config.from_object('config.default')
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
wxsdk = WXSDK(app.config)

USR = app.config['ADMIN_ACCOUNT']
PWD = app.config['ADMIN_PASSWORD']

from app import views
from app.product import bp as product_bp
from app.order import bp as order_bp
from app.oauth import bp as oauth_bp
app.register_blueprint(product_bp, url_prefix='/product')
app.register_blueprint(order_bp, url_prefix='/order')
app.register_blueprint(oauth_bp, url_prefix='/oauth')

engine = create_engine(app.config['MYSQL_ENGINE'])
engine.execute(app.config['MYSQL_CREATE_DATABASE'])

from app.models import Product
from app.models import Order
db.create_all()


