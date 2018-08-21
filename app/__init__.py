# encoding = utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.default')
app.config.from_pyfile('config.py')

engine = create_engine(app.config['MYSQL_ENGINE'])
engine.execute(app.config['MYSQL_CREATE_DATABASE'])

db = SQLAlchemy(app)

from app.models import Order