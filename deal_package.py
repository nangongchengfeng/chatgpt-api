# -*- coding: utf-8 -*-
# @Time    : 2020/5/6 16:17
# @Author  : yu.lei

import os


def export_package():
    os.system("pipreqs ./ --encoding='utf-8' --force")


def input_package():
    os.system("pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple")


if __name__ == '__main__':
    export_package()
