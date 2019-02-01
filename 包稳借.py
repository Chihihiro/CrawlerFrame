#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/31 0031 14:10 
# @Author : Chihiro 
# @Site :  
# @File : 包稳借.py 
# @Software: PyCharm


import json
from time import sleep
from Frame.Crawler import BaseSpider
from Frame.Request import Request


class Spider(BaseSpider, Request):
    def __init__(self, account):
        super(Spider, self).__init__(account)

    def get_info(self):
        # xpath信息
        xpath_info = {
            "username": '//*[@id="app"]/div/div/div/input[1]',
            "password": '//*[@id="app"]/div/div/div/input[2]',
            "login_button": '//body/div/div/div/div/div',
            "message_code": '',
            "check_code": '',
            "code_image": '',
            "success_ele": '//*[@id="header"]/div[2]/div[1]/div'
        }
        cookie = self.login(xpath_info)  # 获取cookie
        print(cookie)
        # json的url地址
        json_url = f"http://natiedai.51bifang.cn/admin/channel/customer/page?page=1&limit=10&channelId=&startTime={self.today}"
        info = json.loads(
            self.request(json_url, method="get", cookie_dict=cookie)
        )["data"]
        print(info)
        # 最终结果
        result = {
            "注册人数": info["total"],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": "",
            "地区": self.area,
            "产品要求": self.requirements
        }
        # print(result)
        self.write_sql(result)


account_info = {
    "login_url": "http://natiedai.51bifang.cn/#/login",
    "area": 1,
    "product": "包稳借",
    "username": "13023288608",
    "password": "a123456",
    "message_code": "",
    "channel": "",
    "requirements": "下款3%",
    "remark": "",
}

while True:
    product = Spider(account_info)
    product.get_info()
    sleep(600)

