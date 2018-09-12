#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from app.api import bp
from app import utils
from app import app
import xml.etree.ElementTree as ET
import requests
import json
import hashlib
import base64

@bp.route('/sfquery', methods=['GET'])
def sf_query():
    filePath = './callExpressRequest/5.route_queryByMailNo.txt'  # 路由查询-通过运单号
    # 打开相应请求报文txt文件
    file = open(filePath, 'r', encoding='utf8')
    reqXml = file.read()
    # 关闭打开的文件
    file.close()
    reqURL = 'https://bsp-oisp.sf-express.com/bsp-oisp/sfexpressService'
    clientCode = app.config['clientCode']
    checkword = app.config['checkword']  # 此处替换为您在丰桥平台获取的校验码
    myReqXml = reqXml.replace('SLKJ2019', clientCode)
    respXml = httpClient.callSfExpressServiceByCSIM(reqURL, myReqXml, clientCode, checkword)
    if respXml != '':
        tree = ET.fromstring(respXml)
        ary = []
        for child in tree.iter('Route'):
            r = child.attrib
            ary.append(r)
        sfq = utils.ret_msg(ary)
        return sfq

def callSfExpressServiceByCSIM(reqURL, myReqXml, clientCode, checkword):
    if reqURL == '':
        reqURL = 'https://bsp-oisp.sf-express.com/bsp-oisp/sfexpressService'
    str = myReqXml + checkword
    # 先md5加密然后base64加密
    m = hashlib.md5()
    m.update(str.encode('utf-8'))
    md5Str = m.digest()
    verifyCode = base64.b64encode(md5Str).decode('utf-8')
    data = {"xml": myReqXml, "verifyCode": verifyCode}
    # 发送post请求
    res = requests.post(reqURL, data=data)
    return res.text

# def ret_msg(msg):
#     data = {
#         "code": 0,
#         "msg": msg
#     }
#     return json.dumps(data,ensure_ascii=False)



