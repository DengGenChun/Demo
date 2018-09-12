# encoding = utf-8

from app import db
from app import utils


class Order(db.Model):
    __tablename__ = 't_order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_no = db.Column(db.BigInteger, nullable=False, unique=True, index=True)
    p_id = db.Column(db.BigInteger, db.ForeignKey('t_product.p_id'), nullable=False)
    p_count = db.Column(db.Integer, nullable=False)
    price_sum = db.Column(db.Float, nullable=False)
    username = db.Column(db.String(16), nullable=False)
    phone = db.Column(db.String(16), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    comment = db.Column(db.String(128), default='')
    openid = db.Column(db.String(128), nullable=False)
    transaction_id = db.Column(db.String(32), nullable=False, default='')
    trade_type = db.Column(db.String(16), nullable=False)
    trade_state = db.Column(db.String(32), nullable=False)
    trade_state_desc = db.Column(db.String(256), nullable=False, default='')
    notify_state = db.Column(db.String(16), nullable=False, default='UNCHECKED')
    create_time = db.Column(db.BigInteger, nullable=False)
    pay_time = db.Column(db.BigInteger, nullable=False)
    track_no = db.Column(db.String(32), default='')
    track_state = db.Column(db.String(128), default='')
    is_sign = db.Column(db.String(8), default='NO')
    sign_time = db.Column(db.BigInteger, nullable=False)

    def __init__(self, p_id, p_count, username, phone, address, comment=''):
        self.p_id = p_id
        self.p_count = p_count
        self.username = username
        self.phone = phone
        self.address = address
        self.comment = comment
        self.order_no = utils.random_id()
        self.create_time = utils.timestamp()
        self.pay_time = 0
        self.sign_time = 0

    def __repr__(self):
        return '<Order order_no=%d, p_count=%d, price_sum=%f, username=%s, phone=%s, create_time=%s>' \
               % (self.order_no, self.p_count, self.price_sum, self.username, self.phone, self.create_time)

    def asdict(self):
        return {
            "order_no": str(self.order_no),
            "p_id": str(self.p_id),
            "p_count": self.p_count,
            "price_sum": self.price_sum,
            "username": self.username,
            "phone": self.phone,
            "address": self.address,
            "comment": self.comment,
            "openid": self.openid,
            "trade_type": self.trade_type,
            "trade_state": self.trade_state,
            "trade_state_desc": self.trade_state_desc,
            "notify_state": self.notify_state,
            "create_time": self.create_time,
            "pay_time": self.pay_time,
            "track_no": self.track_no,
            "track_state": self.track_state,
            "is_sign": self.is_sign,
            "sign_time": self.sign_time
        }


class Product(db.Model):
    __tablename__ = 't_product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    p_id = db.Column(db.BigInteger, nullable=False, unique=True, index=True)
    name = db.Column(db.String(32), nullable=False)
    price = db.Column(db.Float, nullable=False)
    inventory = db.Column(db.Integer, nullable=False, default=0)
    title = db.Column(db.String(64), default='')
    detail = db.Column(db.String(128), default='')
    color = db.Column(db.String(16), default='')
    icon = db.Column(db.String(128), default='')
    modify_time = db.Column(db.BigInteger, nullable=False)
    create_time = db.Column(db.BigInteger, nullable=False)
    orders = db.relationship('Order', backref='product')

    def __init__(self, name, price, inventory, title='', detail='', color=''):
        self.name = name
        self.price = price
        self.inventory = inventory
        self.title = title
        self.detail = detail
        self.color = color
        self.p_id = utils.random_id()
        timestamp = utils.timestamp()
        self.create_time = timestamp
        self.modify_time = timestamp

    def __repr__(self):
        return '<Product id=%d, name=%s, price=%d, inventory=%d>' % (self.p_id, self.name, self.price, self.inventory)

    def asdict(self):
        return {
            'product_id': str(self.p_id),
            'name': self.name,
            'price': self.price,
            'inventory': self.inventory,
            'title': self.title,
            'detail': self.detail,
            'color': self.color,
            'icon': self.icon,
            'modify_time': self.modify_time,
            'create_time': self.create_time
        }
