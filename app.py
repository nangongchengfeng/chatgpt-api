# -*- coding: utf-8 -*-
# @Time    : 2023/7/6 10:27
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : app.py
# @Software: PyCharm
import os

from flask import Flask, jsonify, make_response

from app.chat import chat
from utils.response_util import ResponseUtils

app = Flask(__name__)
app.register_blueprint(chat, url_prefix='/chat')


@app.route('/')
def index():
    return ResponseUtils.success()


@app.route('/actuator/health', methods=['GET', 'HEAD'])
def health():
    return jsonify({'online': True})


@app.errorhandler(400)
@app.errorhandler(404)
def handle_error(error):
    error_code = str(error.code)
    error_msg = '请求参数不合法' if error.code == 400 else '页面未找到'
    return make_response(jsonify({'code': error_code, 'msg': error_msg}), error.code)


if __name__ == '__main__':
    os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, host="0.0.0.0", use_reloader=False)
