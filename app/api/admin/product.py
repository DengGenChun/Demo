# encoding = utf-8

from flask import request

from app import db
from app import utils
from app.api.admin import bp
from app.decor import admin_required
from app.models import Product
from app.models import Order


@bp.route('/addProduct', methods=['GET'])
@admin_required
def add_product():
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
    product.color = request.args.get('color', '')
    product.icon = request.args.get('icon', '')
    db.session.add(product)
    db.session.commit()
    return utils.ret_msg_objs('Suceess', product)


@bp.route('/delProduct', methods=['GET'])
@admin_required
def del_product():
    p_id = request.args.get('p_id')
    if p_id is None or p_id == '':
        return utils.ret_err(-1, "p_id is required")
    product = Product.query.filter_by(p_id=p_id).first()
    if product is None:
        return utils.ret_err(-1, "Product doesn't exists")
    db.session.delete(product)
    db.session.commit()
    return utils.ret_msg('Success')


@bp.route('/updateProduct', methods=['GET'])
@admin_required
def update_product():
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
    price = request.args.get('price', 0, float)
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
    sale_count = request.args.get('sale_count')
    if sale_count is not None:
        params["sale_count"] = sale_count
    color = request.args.get('color')
    if color is not None:
        params["color"] = color
    icon = request.args.get('icon')
    if icon is not None:
        params["icon"] = icon

    if bool(params):
        Product.query.filter_by(p_id=p_id).update(params)
        db.session.commit()
        return utils.ret_msg_objs('Success', product)
    return utils.ret_msg('Nothing happen')


@bp.route('/listProduct', methods=['GET'])
@admin_required
def list_product():
    p_id = request.args.get('p_id')
    if p_id:
        product = Product.query.filter_by(p_id=p_id).first()
        return utils.ret_objs(product)

    order_no = request.args.get('order_no')
    if order_no:
        order = Order.query.filter_by(order_no=order_no).first()
        if order:
            return utils.ret_objs(order.product)
        return utils.ret_err(-1, "order_no is wrong")

    return utils.ret_err(-1, "p_id or order_no is required")


@bp.route('/listAllProduct', methods=['GET'])
@admin_required
def list_all_product():
    products = Product.query.all()
    return utils.ret_objs(products)