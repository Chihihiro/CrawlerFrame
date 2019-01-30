# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月25日 14:31
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : Proxy.py
# @Software: PyCharm
# @Describe: 

import requests


def get_proxy():
    # ip接口
    url = "http://api.ip.data5u.com/dynamic/get.html?order=6a1f20e0bc74d19794a6b3d2df4a6107&sep=3"
    # 请求接口
    response = requests.get(url)
    return response.text


if __name__ == '__main__':
    print(get_proxy())


























