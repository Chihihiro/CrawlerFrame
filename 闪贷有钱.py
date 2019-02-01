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


class Spider(BaseSpider, Request):
    def __init__(self, account):
        super(Spider, self).__init__(account)

    def get_info(self):
        url = "http://www.youxinsign.com:13083/youka/ope-channel/getChannelRegist?encCode=E74D550F1A5F891C"
        json_info = self.request(url=url, method="get")
        info = json.loads(json_info)["data"]["datas"][0]["outRegistCount"]
        # print(html)
        # num = info.xpath('//table[@id="blocks"]/*')#.extract()[0]
        # print(info)
        result = {
            "注册人数": info,
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
    "product": "闪贷有钱",
    "username": "",
    "password": "",
    "message_code": "",
    "channel": "",
    "requirements": "",
    "remark": ""
}

account_info = [AH]

while True:
    for i in account_info:
        product = Spider(i)
        product.get_info()
        product.driver.quit()
    sleep(600)
