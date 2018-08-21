# encoding = utf-8

from app.product import bp
from flask import request


@bp.route('/add', methods=['GET'])
def add():
    name = request.args.get('name')
    if name is None or name == '':
        print('name=None or empty')
    else:
        print('name=%s' % name)
    return 'Success'
