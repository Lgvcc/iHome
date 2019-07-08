# coding:utf-8

from . import api
from home import db, models

@api.route('/index')
def index():
    return 'index page!'
