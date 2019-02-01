#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/28 0028 14:27 
# @Author : Chihiro 
# @Site :  
# @File : 来客优钱包.py 
# @Software: PyCharm



import time
import json
from time import sleep
from Frame.Crawler import BaseSpider
from Frame.Request import Request
from scrapy import Selector
from datetime import date, datetime

class Spider(BaseSpider, Request):
    def __init__(self, account):
        super(Spider, self).__init__(account)

    def get_info(self):
        # xpath信息
        xpath_info = {
            "username": '//*[@id="app"]/div/div/div[2]/div/div[2]/div[1]/form/div[1]/div/div/input',
            "password": '//*[@id="app"]/div/div/div[2]/div/div[2]/div[1]/form/div[2]/div/div/input',
            "login_button": '//*[@id="app"]/div/div/div[2]/div/div[2]/div[1]/div',
            "message_code": '',
            "check_code": '//*[@id="app"]/div/div/div[2]/div/div[2]/div[1]/form/div[3]/div/div/input',
            "code_image": '//*[@id="app"]/div/div/div[2]/div/div[2]/div[1]/form/div[3]/div/img',
            "success_ele": '//*[@id="app"]/div/div[2]/div[2]/div/span[1]'
        }
        cookies = self.login(xpath_info, image_size=(1019, 355, 1113, 392), image_type="10400")
        url = "http://payday-likeyou.lkdjhls.cn/admin_agent/mySCustomerList"
        t1 = date.today()
        now = int(time.mktime(t1.timetuple()))
        arg = {
            'page': 1,
            'agentid': self.channel,
            'startTime': int(now),
            'endTime': int(now+60*60*24),
        }
        print(arg)
        info = json.loads(self.request(
            url=url,
            cookie_dict=cookies,
            method="post",
            args=arg
        ))['body']
        result = {
            "注册人数": info['total'],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": self.remark,
            "地区": self.area,
            "产品要求": self.requirements
        }
        # print(result)
        self.write_sql(result)


AH = {
    "login_url": "http://payday-likeyou.lkdjhls.cn/admin/likeyou.html#/sign-in",
    "product": "来客优钱包",
    "username": "huan1",
    "password": "123456",
    "message_code": "",
    "channel": 30868702,
    "requirements": "申请40% 下款3%",
    "remark": "全国",
    "area": 1
}

SH = {
    "login_url": "http://payday-likeyou.lkdjhls.cn/admin/likeyou.html#/sign-in",
    "product": "来客优钱包",
    "username": "huan7",
    "password": "123456",
    "message_code": "",
    "channel": 30873139,
    "requirements": "申请40% 下款3%",
    "remark": "",
    "area": 0
}

account_info = [SH]

while True:
    try:
        for i in account_info:
            product = Spider(i)
            product.get_info()
            sleep(600)
    except:
        continue


