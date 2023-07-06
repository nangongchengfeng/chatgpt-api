# -*- coding: utf-8 -*-
# @Time    : 2023/7/6 10:30
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : chat.py
# @Software: PyCharm
import json

from flask import Blueprint, request

from app.chat_service import question_answer_turbo_api
from utils.LogHandler import log
from utils.response_util import ResponseUtils

chat = Blueprint('chat', __name__)


@chat.route('/api/', methods=["post"])
def question():
    req_data = json.loads(request.data.decode('utf-8'))
    log.info("请求参数: {}".format(req_data))
    res = question_answer_turbo_api(req_data)
    return ResponseUtils.success_with_data(res)

