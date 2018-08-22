# encoding = utf-8

from flask import request
from app import db
from app import utils
from app.product import bp
from app.models import Product


@bp.route('/add', methods=['GET'])
def add():
    name = request.args.get('name', '')
    price = request.args.get('price', 0, int)
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


@bp.route('/delete/<int:product_id>', methods=['GET'])
def delete(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if product is None:
        return utils.ret_err(-1, "Product doesn't exists")
    db.session.delete(product)
    db.session.commit()
    return utils.ret_msg('Success')


@bp.route('/update/<int:product_id>', methods=['GET'])
def update(product_id):
    product = Product.query.filter_by(id=product_id).first()
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
        pro = Product.query.filter_by(id=product_id).update(params)
        return utils.ret_msg_objs('Success', pro)
    return utils.ret_msg('Nothing happen')


@bp.route('/list/<int:product_id>', methods=['GET'])
def list_product(product_id):
    product = Product.query.filter_by(id=product_id).first()
    return utils.ret_objs(product)


@bp.route('/list', methods=['GET'])
def list_all_product():
    products = Product.query.all()
    return utils.ret_objs(products)


@bp.route('/<int:product_id>/listOrder', methods=['GET'])
def list_order_by_product_id(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if product is not None:
        return utils.ret_objs(product.orders)
    return utils.ret_err(-1, "Product doesn't exists")
