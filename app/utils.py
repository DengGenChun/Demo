# encoding = utf-8

import datetime
import uuid
import random
import time


# 生成订单号
# 机器编号[前4位] + 时间戳 + 随机4位数 + 毫秒数
def order_no():
    mac = str(uuid.UUID(int=uuid.getnode()).int)[:4]
    date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    rand = str(random.randrange(1000, 9999))
    mills = datetime.datetime.utcnow().strftime('%f')[:-3]
    return mac + date + rand + mills


def timestamp():
    return int(round(time.time() * 1000))
