#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/29 0029 13:39 
# @Author : Chihiro 
# @Site :  
# @File : 白菜.py 
# @Software: PyCharm




import json
from time import sleep
from Frame.Crawler import BaseSpider
from Frame.Request import Request
from scrapy import Selector

class Spider(BaseSpider, Request):
    def __init__(self, account):
        super(Spider, self).__init__(account)

    def get_info(self):
        url = 'http://kxhua.hztiantu.cn/jm-masterv2server/static/userstatlists?channelpwd=a643313119ac1fb5b77c0e7d93c1de6d'
        html = self.request(url=url, method="get")
        info = Selector(text=html)
        num = info.xpath('/html/body/div/table/tbody/tr/td[4]/text()').extract()[0]
        result = {
            "注册人数": num,
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": "",
            "地区": self.area,
            "产品要求": self.requirements
        }
        self.write_sql(result)




AH = {
    "login_url": "",
    "area": 0,
    "product": "白菜",
    "username": "",
    "password": "",
    "message_code": "",
    "channel": "",
    "requirements": "下款3%",
    "remark": ""
}

account_info = [AH]

while True:
    for i in account_info:
        product = Spider(i)
        product.get_info()
    sleep(1200)
