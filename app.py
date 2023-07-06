# -*- coding: utf-8 -*-
# @Time    : 2023/7/6 10:27
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : app.py
# @Software: PyCharm
import os

from flask import Flask
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "hello world"


if __name__ == '__main__':
    os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, host="0.0.0.0", use_reloader=False)
