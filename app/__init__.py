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

PWD = app.config['ADMIN_PASSWORD']
USR = app.config['ADMIN_ACCOUNT']

from app import views
from app.api.admin import bp as bp_admin
from app.api.oauth import bp as bp_oauth
from app.api import bp as bp_api
app.register_blueprint(bp_admin, url_prefix='/api/admin')
app.register_blueprint(bp_oauth, url_prefix='/api/oauth')
app.register_blueprint(bp_api, url_prefix='/api')

engine = create_engine(app.config['MYSQL_ENGINE'])
engine.execute(app.config['MYSQL_CREATE_DATABASE'])

from app.models import Product
from app.models import Order
db.create_all()


