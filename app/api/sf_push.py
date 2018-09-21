#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from app.api import bp
from app import db
import time
from xml.etree import cElementTree as ET
import requests
from flask import request
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from app.models import Order


@bp.route('/sfpush', methods=['POST'])
def sf_push():
    dic1 = to_dict(request.data)
    print(dic1)
    dic2 = {'Head': 'OK'}
    dic3 = {'Head': 'ERR','name':'ERROR','con':'系统发生数据错误或运行时异常'}

    order = Order.query.filter_by(track_no=dic1['mailno']).first()
    if not order:
        return to_xml(dic3,1)
    order.track_code = dic1['opCode']
    order.track_state = dic1['remark']
    order.track_time = int(time.mktime(time.strptime(dic1['acceptTime'], "%Y-%m-%d %H:%M:%S")) * 1000)
    if order.track_code == 80:
        order.is_sign = "YES"
        order.sign_time = order.track_time
    db.session.commit()

    if dic1:
        res = to_xml(dic2,0)
    else:
        res = to_xml(dic3,1)
    return res

def to_dict(xml):
    dic = {}
    tree = ET.fromstring(xml)
    for child in tree.iter('WaybillRoute'):
        dic = child.attrib
    return dic

def to_xml(dic,n):
    s = ''
    if n==0:
        for k, v in dic.items():
            s += "<{0}>{1}</{0}>".format(k, v)
    else:
        for k, v in dic.items():
            s += "<{0}>{1}</{0}>".format(k, v)
            break
        s += "<{name} code='4001'>{con}</{name}>".format(**dic)
    s = "<Response service='RoutePushService'>{0}</Response>".format(s)
    return s.encode('utf-8')

# filePath = './callExpressRequest/8.route.txt'
# file = open(filePath, 'r', encoding='utf-8')
# sXml = file.read()
# # 关闭打开的文件
# file.close()
# s=to_dict(sXml)
# print(s)

