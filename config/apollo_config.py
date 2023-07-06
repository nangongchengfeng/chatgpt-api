# -*- coding: utf-8 -*-
# @Time    : 2023/7/6 11:10
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : apollo_config.py.py
# @Software: PyCharm
import os

"""
这个文件是用来从apollo配置中心获取配置的

如果你的项目不需要从apollo配置中心获取配置，可以删除这个文件

直接在 api_key_list 中添加你的API KEY即可
"""

from pyapollos import ApolloClient

from utils.LogHandler import log

log.info("加载apollo配置")
APOLLO_CONFIG_URL = "config-server-dev.ownit.top"
client = ApolloClient(app_id="chatgpt-api", cluster="default",
                      config_server_url='http://' + APOLLO_CONFIG_URL)

AppKey1 = client.get_value('api-key1')
AppKey2 = client.get_value('api-key2')

if __name__ == '__main__':
    print(AppKey1)
