#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/28 0028 15:08 
# @Author : Chihiro 
# @Site :  
# @File : 淘钱宝.py 
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
        # xpath信息
        xpath_info = {
            "username": '//*[@id="loginform-username"]',
            "password": '//*[@id="loginform-password"]',
            "login_button": '//*[@id="login-form"]/div[3]/div[2]/button',
            "message_code": '',
            "check_code": '',
            "code_image": '',
            "success_ele": '/html/body/div/header/nav/div/ul/li[4]/a/span'
        }
        cookie = self.login(xpath_info)  # 获取cookie
        url = f"http://agent.taoqian123.com/site/view?time={self.today}+-+{self.tomorrow}&info_id=820"
        info = self.request(url, method="get", cookie_dict=cookie)
        # 最终结果
        print(info)
        html = Selector(text=info)

        result = {
            "注册人数": html.xpath('/html/body/div[1]/div[1]/section[2]/div/div/div/div[2]/div/div/table/tbody/tr[1]/td[2]/text()').extract()[0],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": "",
            "地区": self.area,
            "产品要求": self.requirements
        }
        # print(result)
        self.write_sql(result)


SH = {
    "login_url": "http://agent.taoqian123.com/site/login",
    "area": 1,
    "product": "淘钱宝",
    "username": "米来",
    "password": "123456",
    "message_code": "",
    "channel": "",
    "requirements": "申请40% 下款3%",
    "remark": ""
}


account_info = [SH]

while True:
    for i in account_info:
        product = Spider(i)
        product.get_info()
    sleep(600)



























