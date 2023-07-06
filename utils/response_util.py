# -*- coding: utf-8 -*-
# @Time    : 2023/7/6 10:46
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : response_util.py
# @Software: PyCharm
from flask import jsonify, make_response


class ResponseUtils(object):
    def __init__(self, code=0, data=None, msg=None, debug_info=None):
        self.code = code
        self.data = data
        self.msg = msg
        self.debug_info = debug_info

    def to_resp(self):
        return jsonify({
            "code": self.code,
            "data": self.data,
            "msg": self.msg,
            "debugInfo": self.debug_info,
        })

    @staticmethod
    def success():
        return ResponseUtils(code=0).to_resp()

    @staticmethod
    def success_with_data(data):
        return ResponseUtils(code=0, data=data).to_resp()

    @staticmethod
    def error(code=1, msg=None, debug_info=None):
        return ResponseUtils(code, msg=msg, debug_info=debug_info).to_resp()

    @staticmethod
    def warn(code, msg=None, debug_info=None):
        return ResponseUtils(code=code, msg=msg, debug_info=debug_info).to_resp()
