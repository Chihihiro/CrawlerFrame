#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/31 0031 15:27 
# @Author : Chihiro 
# @Site :  
# @File : 金猪闪贷.py 
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
            "username": '//*[@id="userName"]',
            "password": '//*[@id="userPwd"]',
            "login_button": '/html/body/div/div/div/label[4]/a',
            "message_code": '',
            "check_code": '',
            "code_image": '',
            "success_ele": '//*[@id="menu-user-face"]'
        }
        cookie = self.login(xpath_info)  # 获取cookie
        print(cookie)
        # json的url地址
        json_url = f"http://agent.3md.mzjgx.com/loan/agentPlatform/queryCPA?startTime={self.today}+00%3A00%3A00&endTime={self.tomorrow}+00%3A00%3A00&agentId=361&page=1&rows=25"
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
    "login_url": "http://partner.goldminesaas.com/partner/login.jsp",
    "area": 1,
    "product": "金猪闪贷",
    "username": "wyw",
    "password": "123456",
    "message_code": "",
    "channel": "",
    "requirements": "下款3%",
    "remark": "",
}

while True:
    product = Spider(account_info)
    product.get_info()
    sleep(600)
