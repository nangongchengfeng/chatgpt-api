# -*- coding: utf-8 -*-
# @Time    : 2023/7/6 10:30
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : chat.py
# @Software: PyCharm
from flask import Blueprint

chat = Blueprint('chat', __name__)


@chat.route('/api/')
def hello():
    return 'Hello from blueprint!'
