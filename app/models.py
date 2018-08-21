# encoding = utf-8

from app import db
import datetime
import uuid
import random


class Order(db.Model):
    __tablename__ = 't_order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_no = db.Column(db.String(32), unique=True, index=True, default=create_order_no())
    price = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(16), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(128), nullable=False)
    comment = db.Column(db.String(128))
    create_time = db.Column(db.TIMESTAMP, default=datetime.datetime)

    # 生成订单号
    # 机器编号[前4位] + 时间戳 + 随机4位数 + 毫秒数
    def create_order_no(self):
        mac = str(uuid.UUID(int=uuid.getnode()).int)[:4]
        date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        rand = str(random.randrange(1000, 9999))
        mills = datetime.datetime.utcnow().strftime('%f')[:-3]
        return mac + date + rand + mills