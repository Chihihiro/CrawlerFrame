# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月25日 17:18
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : 鼎瑞应急.py
# @Software: PyCharm
# @Describe: 

import json
from time import sleep
from Frame.Crawler import BaseSpider
from Frame.Request import Request


class Spider(BaseSpider, Request):
    def __init__(self, account):
        super(Spider, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="rrapp"]/div[2]/div[1]/input',
            "password": '//*[@id="rrapp"]/div[2]/div[2]/input',
            "login_button": '//*[@id="rrapp"]/div[2]/div[4]/div[2]/button',
            "message_code": '',
            "check_code": '//*[@id="rrapp"]/div[2]/div[3]/input',
            "code_image": '//*[@id="rrapp"]/div[2]/div[3]/img',
            "success_ele": '//*[@id="rrapp"]/aside/section/ul/li[2]/a/span'
        }
        # 获取Cookie值
        cookie = self.login(
            xpath_info,
            image_size=(1020, 440, 1111, 475),
            image_type="305000001"
        )
        # json的url
        json_url = f"http://47.100.132.254//getRegisterCount?_search=false&nd=1548404740845&size=10&current=1&sidx=&order=asc&startTime={self.today}&endTime={self.today}&channelCode=xiaomao10&_=1548404721828"
        # 设置参数
        args = {
            '_search': 'false',
            'nd': '1548404721828',
            'size': '10',
            'current': '1',
            'sidx': "",
            'order': 'asc',
            'startTime': f"{self.today}",
            'endTime': f"{self.tomorrow}",
            'channelCode': self.channel,
            '_': '1548404721828',
        }
        # 获取数据
        info = json.loads(
            self.request(json_url, cookie_dict=cookie, method="post", args=args, payload=True)
        )['records'][0]

        # 获取结果
        result = {
            "注册人数": info["registerCount"],
            "实名人数": "null",
            "申请人数": info["applyCount"] if info["applyCount"]!="" else 0,
            "放款人数": info["payCount"] if info["payCount"]!="" else 0,
            '备注': "",
            "地区": self.area,
            "产品要求": self.requirements
        }
        # print(result)
        self.write_sql(result)


SH = {
    "login_url": "http://47.100.132.254/login.html",
    "area": 0,
    "product": "鼎瑞应急",
    "username": "xiaomao",
    "password": "123456",
    "message_code": "",
    "channel": "xiaomao10",
    "requirements": "下款6  认证50",
    "remark": ""

}


account_info = [SH]

while True:
    for i in account_info:
        product = Spider(i)
        product.get_info()
    sleep(600)

























