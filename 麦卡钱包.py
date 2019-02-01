#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/30 0030 14:09 
# @Author : Chihiro 
# @Site :  
# @File : 麦卡钱包.py 
# @Software: PyCharm


from datetime import date, datetime
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
            "username": '//*[@id="username$text"]',
            "password": '//*[@id="pwd$text"]',
            "login_button": '//*[@id="loginForm"]/table/tbody/tr[3]/td[2]/a[1]/span/span',
            "message_code": '',
            "check_code": '',
            "code_image": '',
            "success_ele": '//*[@id="1$cell$3"]'
        }
        # 获取Cookie值
        cookie = self.login(xpath_info)
        # page的url
        page_url = "http://www.mashpay.live/admin/data/channels.php?method=channelRegisterUsersList"
        # 设置参数
        t1 = date.today()
        now = int(time.mktime(t1.timetuple()))

        arg = {
            'startTime': now,
            'endTime': now,
            'pageIndex': 0,
            'pageSize': 10,
            'sortField': "",
            'sortOrder': ""
        }
        info = json.loads(self.request(page_url, cookie_dict=cookie, method="post", args=arg))
        # 获取结果
        print(info)
        result = {
            "注册人数": info['total'],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": "",
            "地区": self.area,
            "产品要求": self.requirements
        }
        self.write_sql(result)


SH = {
    "login_url": "http://www.mashpay.live/loginLayout.html",
    "area": 0,
    "product": "麦卡钱包",
    "username": "jsd24",
    "password": "123456",
    "message_code": "",
    "channel": "",
    "requirements": "下款3%",
    "remark": ""
}


account_info = [SH]

while True:
    for i in account_info:
        product = Spider(i)
        product.get_info()
    time.sleep(1200)
