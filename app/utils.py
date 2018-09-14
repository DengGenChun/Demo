# encoding = utf-8

import datetime
import random
import time
import hashlib
import json
import string


# 生成随机整数(18位)
# 毫秒数(3位) + 时间戳(前5位) + 随机数(5位) + 时间戳(后5位)
def random_id():
    date = str(round(time.time()))
    rand = str(random.randrange(10000, 99999))
    millis = datetime.datetime.utcnow().strftime('%f')[:-3]
    return int(millis + date[:5] + rand + date[5:])


def random_str():
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(32))


def timestamp():
    return int(round(time.time() * 1000))


def str2timestamp(s):
    return int(time.mktime(time.strptime(s, "%Y%m%d%H%M%S")) * 1000)


def md5(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


def ret_err(code, msg):
    data = {
        "code": code,
        "msg": msg
    }
    return json.dumps(data)


def ret_msg(msg):
    data = {
        "code": 0,
        "msg": msg
    }
    return json.dumps(data)


def ret_objs(objs):
    result = []
    if isinstance(objs, list) or isinstance(objs, tuple):
        for obj in objs:
            if hasattr(obj, 'asdict'):
                result.append(obj.asdict())
            else:
                result.append(obj)
    elif hasattr(objs, 'asdict'):
        result = objs.asdict()
    else:
        result = objs

    data = {
        "code": 0,
        "result": result
    }
    return json.dumps(data)


def ret_msg_objs(msg, objs):
    result = []
    if isinstance(objs, list) or isinstance(objs, tuple):
        for obj in objs:
            result.append(obj.asdict())
    elif hasattr(objs, 'asdict'):
        result = objs.asdict()
    else:
        result = objs

    data = {
        "code": 0,
        "msg": msg,
        "result": result
    }
    return json.dumps(data)