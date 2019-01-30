# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月23日 9:42
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : DealWithCookie.py
# @Software: PyCharm
# @Describe: 将Selenium获取到的Cookie信息转为字典格式


def cookie_to_dict(cookie_info):
    cookie_dict = {}
    for each in cookie_info:
        cookie_dict[each["name"]] = each["value"]
    return cookie_dict


























