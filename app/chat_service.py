# -*- coding: utf-8 -*-
# @Time    : 2023/7/6 11:29
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : chat_service.py
# @Software: PyCharm
import json
import random

import openai
import requests

from config import CONFIG_PATH
from config.config import model_programming_translate, \
    model_gpt_35_turbo, api_key_list
from utils.LogHandler import log


# QA问题
def question_answer_turbo_api(req_data):
    """

        {
        "systemContent" : "你好，我是小智，你可以问我任何问题，我会尽力回答你的问题。",
        "question": "后续预测一下中国房地产的问题？",
        "sessionLog": [
            {
                "question":"你怎么看待中国的发展趋势",
                "answer":"中国实施了一系列发展战略和政策，包括两个一百年目标和新发展格局，旨在推动国家的经济、社会和科技进步。同时，中国积极参与全球化进程，加强与其他国家的合作，并在全球事务中扮演着越来越重要的角色。然而，国家的发展趋势是一个复杂的问题，涉及许多方面，包括政治、经济、社会和环境等。未来的发展趋势将取决于各种因素，如内外部环境、政策导向、国际关系和全球经济等"
            }
        ]
    }

    :param req_data:
    :return:
    """
    company_name = 'openai'
    ## 角色
    system_content = req_data.get('systemContent')
    # 问题
    question = req_data.get('question')
    # 历史记录
    session_log = req_data.get('sessionLog')
    # 最大长度
    max_tokens = 1024

    '''
    :param quester: 问题
    :return: 答案
    '''
    last_question = {
        "role": "user",
        "content": question
    }
    last_count = 3
    # 消息类表
    messages = []
    if system_content:
        system = {"role": "system", "content": system_content}
        messages.append(system)
    if session_log:
        session_log = session_log[-last_count:]
        for sl in session_log:
            messages.append(
                {
                    'role': 'user',
                    'content': sl['question']
                }
            )
            messages.append(
                {
                    'role': 'assistant',
                    'content': sl['answer']
                }
            )
    messages.append(last_question)
    log.info('messages:{}'.format(messages))

    # 重试
    retry_time = 3
    # 访问连接
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "model": model_gpt_35_turbo,
        "temperature": 0.7,
        'top_p': 1,
        'frequency_penalty': 0.2,
        'presence_penalty': 0.2,
    }
    for i in range(0, retry_time):

        api_key = random.choice(api_key_list)

        headers['Authorization'] = 'Bearer {}'.format(api_key)
        data['messages'] = messages
        data['temperature'] = random.uniform(0.3, 0.8)
        data['max_tokens'] = max_tokens
        try:
            resp = requests.post(url, headers=headers, data=json.dumps(data))
            status_code = resp.status_code
            json_data = resp.json()
            log.info('请求ChatGPT结果：{}'.format(json_data))
            if status_code == 200:
                choices = json_data['choices']
                if len(choices) > 0:
                    text = choices[0]['message']['content']
                    usage = json_data['usage']
                    completion_tokens = usage['completion_tokens']
                    prompt_tokens = usage['prompt_tokens']
                    total_tokens = usage['total_tokens']
                res = {
                    'result': text.strip().replace('作为AI语言模型，', ''),
                    'completionTokens': completion_tokens
                }
                return res
            else:
                error_message = json_data['error']['message']
                log.error('请求ChatGPT失败：{}'.format(error_message))
                if status_code == 429:
                    continue
                elif status_code == 401:
                    continue
                elif status_code == 400:
                    if system_content:
                        messages.pop(1)
                        messages.pop(1)
                    else:
                        messages.pop(0)
                        messages.pop(0)
        except Exception as e:
            log.error('请求ChatGPT失败：{}'.format(e))
            pass
    raise openai.OpenAIError


# 编程语言转换
def programming_language_translate(original, object, text):
    account_list = json.load(open(f'{CONFIG_PATH}/openai_account.json', 'r'))
    auth = random.choice(account_list)
    openai.organization = auth['organization'].strip()
    openai.api_key = auth['api_key'].strip()
    # print('本次使用的账号信息：', auth)
    '''
    :param original: 需要转换的语言
    :param object: 目标语言
    :param text: 需要转换的内容
    :return: 目标语言内容
    '''
    response = openai.Completion.create(
        model=model_programming_translate,
        prompt='''
##### 将{}转换成{}
### {} ###{}
      '''.format(original, object, text, object),
        temperature=0,
        max_tokens=512,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=['###']
    )
    if len(response.get('choices')) > 0:
        # print(response.get('choices'))
        return response.get('choices')[0]['text']
    else:
        return None
