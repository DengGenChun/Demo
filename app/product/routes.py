# encoding = utf-8

from flask import request
from app import db
from app import utils
from app.product import bp
from app.models import Product


@bp.route('/add', methods=['GET'])
@utils.check_admin
def add():
    name = request.args.get('name', '')
    price = request.args.get('price', 0, float)
    inventory = request.args.get('inventory', 0, int)
    if name == '':
        return utils.ret_err(-1, 'name is requested')
    if price <= 0:
        return utils.ret_err(-1, 'price must > 0')
    if inventory <= 0:
        return utils.ret_err(-1, 'inventory must > 0')

    product = Product(name, price, inventory)
    product.title = request.args.get('title', '')
    product.detail = request.args.get('detail', '')
    db.session.add(product)
    db.session.commit()
    return utils.ret_msg_objs('Suceess', product)


@bp.route('/delete', methods=['GET'])
@utils.check_admin
def delete():
    p_id = request.args.get('p_id')
    if p_id is None or p_id == '':
        return utils.ret_err(-1, "p_id is required")
    product = Product.query.filter_by(p_id=p_id).first()
    if product is None:
        return utils.ret_err(-1, "Product doesn't exists")
    db.session.delete(product)
    db.session.commit()
    return utils.ret_msg('Success')


@bp.route('/update', methods=['GET'])
@utils.check_admin
def update():
    p_id = request.args.get('p_id')
    if p_id is None or p_id == '':
        return utils.ret_err(-1, "p_id is required")
    product = Product.query.filter_by(p_id=p_id).first()
    if product is None:
        return utils.ret_err(-1, "Product doesn't exists")
    params = {}
    name = request.args.get('name', '')
    if name != '':
        params["name"] = name
    price = request.args.get('price', 0, int)
    if price > 0:
        params["price"] = price
    inventory = request.args.get('inventory', 0, int)
    if inventory > 0:
        params["inventory"] = inventory
    title = request.args.get('title')
    if title is not None:
        params["title"] = title
    detail = request.args.get('detail')
    if detail is not None:
        params["detail"] = detail

    if bool(params):
        Product.query.filter_by(p_id=p_id).update(params)
        db.session.commit()
        return utils.ret_msg_objs('Success', product)
    return utils.ret_msg('Nothing happen')


@bp.route('/list', methods=['GET'])
@utils.check_admin
def list_product():
    p_id = request.args.get('p_id')
    if p_id is None or p_id == '':
        return utils.ret_err(-1, "p_id is required")
    product = Product.query.filter_by(p_id=p_id).first()
    return utils.ret_objs(product)


@bp.route('/listAll', methods=['GET'])
@utils.check_admin
def list_all_product():
    products = Product.query.all()
    return utils.ret_objs(products)


@bp.route('/listOrder', methods=['GET'])
@utils.check_admin
def list_order_by_product_id():
    p_id = request.args.get('p_id')
    if p_id is None or p_id == '':
        return utils.ret_err(-1, "p_id is required")
    product = Product.query.filter_by(p_id=p_id).first()
    if product is not None:
        return utils.ret_objs(product.orders)
    return utils.ret_err(-1, "Product doesn't exists")
