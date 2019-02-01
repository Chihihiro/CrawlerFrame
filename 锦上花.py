# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月25日 23:15
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : 锦上花.py
# @Software: PyCharm
# @Describe: 

from scrapy import Selector
from Frame.Crawler import BaseSpider
from Frame.Request import Request
from time import sleep
import time
import json


class Spider(BaseSpider, Request):
    def __init__(self, account):
        super(Spider, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="userName"]',
            "password": '//*[@id="password"]',
            "login_button": '//*[@id="doLogin"]',
            "message_code": '',
            "check_code": '',
            "code_image": '',
            "success_ele": '/html/body/div/div/div[1]/ul[2]/li/a'
        }
        # 获取Cookie值
        cookie = self.login(xpath_info)
        # page的url
        page_url = "http://39.105.212.10:86/ChannelData/GetData"
        # 设置参数
        arg = {
            'page': 1,
            'limit': 10,
            'SubordinateChannel': '天狼60',
            'Province': "",
            'createTimeStart': f"{self.today}",
            'createTimeEnd': f'{self.tomorrow}',
            'DataPerfection': ""
        }
        info = json.loads(self.request(page_url, cookie_dict=cookie, method="post", args=arg))
        # 获取结果
        result = {
            "注册人数": info['count'],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": "",
            "地区": self.area,
            "产品要求": self.requirements
        }
        self.write_sql(result)


SH = {
    "login_url": "http://39.105.212.10:86/",
    "area": 1,
    "product": "锦上花",
    "username": "xiuxiu",
    "password": "112233Aa112233Aa",
    "message_code": "",
    "channel": "",
    "requirements": "",
    "remark": ""
}


account_info = [SH]

while True:
    for i in account_info:
        product = Spider(i)
        product.get_info()
    time.sleep(1200)

























