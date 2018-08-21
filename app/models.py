# encoding = utf-8

from app import db
from app import utils


class Order(db.Model):
    __tablename__ = 't_order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_no = db.Column(db.String(32), nullable=False, unique=True, index=True)
    p_id = db.Column(db.Integer, db.ForeignKey('t_product.id'))
    p_count = db.Column(db.Integer, nullable=False)
    price_sum = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(16), nullable=False)
    phone = db.Column(db.String(16), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    comment = db.Column(db.String(128))
    create_time = db.Column(db.BigInteger, nullable=False)

    def __init__(self):
        self.order_no = utils.order_no()
        self.create_time = utils.timestamp()

    def __repr__(self):
        return '<Order order_no=%s, p_count=%d, price_sum=%d, username=%s, phone=%d, create_time=%s>' \
               % (self.order_no, self.phone, self.price_sum, self.username, self.phone, self.create_time)


class Product(db.Model):
    __tablename__ = 't_product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    inventory = db.Column(db.Integer, nullable=False, default=0)
    title = db.Column(db.String(64), default='')
    detail = db.Column(db.String(128), default='')
    modify_time = db.Column(db.BigInteger, nullable=False)
    create_time = db.Column(db.BigInteger, nullable=False)
    orders = db.relationship('Order', backref='product')

    def __init__(self):
        timestamp = utils.timestamp()
        self.create_time = timestamp
        self.modify_time = timestamp

    def __repr__(self):
        return 'Product id=%d, name=%s, price=%d, inventory=%d' % (self.id, self.name, self.price, self.inventory)

