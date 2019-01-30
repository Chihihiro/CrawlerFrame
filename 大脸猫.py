#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/29 0029 16:42 
# @Author : Chihiro 
# @Site :  
# @File : 大脸猫.py 
# @Software: PyCharm





import time
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
            "username": '//*[@id="name"]',
            "password": '//*[@id="login"]/div[2]/input',
            "login_button": '//*[@id="login"]/div[4]/div[2]/button',
            "message_code": '',
            "check_code": '//*[@id="login"]/div[3]/input',
            "code_image": '//*[@id="captcha"]',
            "success_ele": '/html/body/div/div[1]/ul[2]/li[2]/a'
        }
        cookies = self.login(xpath_info, image_size=(950, 420, 1070, 456), image_type="30400")
        url = 'https://channel.9281e.cn/index/index.shtml'
        info = self.request(
            url=url,
            cookie_dict=cookies,
            method="get"
        )
        print(info)
        html = Selector(text=info)
        num = html.xpath('/html/body/div/table[1]/tbody/tr/td[1]/text()').extract()[0]
        order = html.xpath('/html/body/div/table[1]/tbody/tr/td[2]/text()').extract()[0]
        # 最终结果
        result = {
            "注册人数": num,
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": order,
            "备注": "",
            "地区": self.area,
            "产品要求": self.requirements
        }
        # print(result)
        self.write_sql(result)


AH = {
    "login_url": "https://channel.9281e.cn/login/login.shtml",
    "product": "大脸猫",
    "username": "fx157",
    "password": "66668888",
    "message_code": "",
    "channel": "",
    "requirements": "下款3%",
    "remark": "",
    "area": 1
}

account_info = [AH]

while True:
    for i in account_info:
        product = Spider(i)
        product.get_info()
    sleep(600)














































