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
    title = request.args.get('title', '')
    price = request.args.get('price', 0, float)
    inventory = request.args.get('inventory', 0, int)
    if name == '' or len(name) > 32:
        return utils.ret_err(-1, 'name(32) is required or too long')
    if title == '' or len(title) > 64:
        return utils.ret_err(-1, 'title(64) is required or too long')
    if price <= 0:
        return utils.ret_err(-1, 'price must > 0')
    if inventory <= 0:
        return utils.ret_err(-1, 'inventory must > 0')

    original_price = request.args.get('original_price', 0, float)
    detail = request.args.get('detail', '')
    color = request.args.get('color', '')
    icon = request.args.get('icon', '')
    if original_price < 0:
        return utils.ret_err(-1, "original_price must > 0")
    if len(detail) > 128:
        return utils.ret_err(-1, "detail(128) is too long")
    if len(color) > 16:
        return utils.ret_err(-1, "color(16) is too long")
    if len(icon) > 128:
        return utils.ret_err(-1, "icon(128) is too long")

    product = Product(name, price, inventory, title)
    product.original_price = original_price
    product.detail = detail
    product.color = color
    product.icon = icon
    product.sale_count = request.args.get("sale_count", 0, int)
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
    if name != '' and len(name) < 32:
        params["name"] = name
    price = request.args.get('price', 0, float)
    if price > 0:
        params["price"] = price
    original_price = request.args.get('original_price', 0, float)
    if original_price > 0:
        params["original_price"] = original_price
    inventory = request.args.get('inventory', -1, int)
    if inventory >= 0:
        params["inventory"] = inventory
    title = request.args.get('title')
    if title and len(title) < 64:
        params["title"] = title
    detail = request.args.get('detail')
    if detail and len(detail) < 128:
        params["detail"] = detail
    sale_count = request.args.get('sale_count', type=int)
    if sale_count:
        params["sale_count"] = sale_count
    color = request.args.get('color')
    if color:
        params["color"] = color
    icon = request.args.get('icon')
    if icon:
        params["icon"] = icon

    if bool(params):
        Product.query.filter_by(p_id=p_id).update(params)
        db.session.commit()
        return utils.ret_msg_objs('Success', product)
    return utils.ret_msg('Nothing happen')


@bp.route('/listProduct', methods=['GET'])
@admin_required
def list_product():
    order_no = request.args.get('order_no')
    if order_no:
        order = Order.query.filter_by(order_no=order_no).first()
        if order:
            return utils.ret_objs(order.product)
        return utils.ret_err(-1, "order_no is wrong")

    stat = Product.query

    p_id = request.args.get('p_id')
    if p_id:
        stat = stat.filter_by(p_id=p_id)
    name = request.args.get('name')
    if name:
        stat = stat.filter(Product.name.like('%' + name + '%'))
    title = request.args.get('title')
    if title:
        stat = stat.filter(Product.title.like('%' + title + '%'))
    detail = request.args.get('detail')
    if detail:
        stat = stat.filter(Product.detail.like('%' + detail + '%'))
    color = request.args.get('color')
    if color:
        stat = stat.filter(Product.color.like('%' + color + '%'))
    min_price= request.args.get('min_price', type=float)
    if min_price:
        stat = stat.filter(Product.price >= min_price)
    max_price= request.args.get('max_price', type=float)
    if max_price:
        stat = stat.filter(Product.price <= max_price)

    return utils.ret_objs(stat.all())