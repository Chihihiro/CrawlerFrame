# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月25日 19:50
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : 借了发.py
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
        # xpath信息
        xpath_info = {
            "username": '//*[@id="app"]/div/form/div[1]/div/div[1]/input',
            "password": '//*[@id="app"]/div/form/div[2]/div/div[1]/input',
            "login_button": '//*[@id="app"]/div/form/div[3]/div/button',
            "message_code": '',
            "check_code": '',
            "code_image": '',
            "success_ele": '//*[@id="app"]/div/div/div[1]/ul/a/li/span'
        }
        cookie = self.login(xpath_info)  # 获取cookie
        # json的url地址
        json_url = f"http://crm.channel.51zhihe.com/backend/statistics?page=1&data=%7B%22search%22:%7B%22start%22:%22{self.today}%22,%22end%22:%22{self.today}%22,%22name%22:%22%22%7D%7D"
        info = json.loads(
            self.request(json_url, method="get", cookie_dict=cookie)
        )["data"]["lists"]["data"][0]
        # 最终结果
        result = {
            "注册人数": info["registers"],
            "实名人数": "null",
            "申请人数": info["applications"],
            "放款人数": "null",
            "备注": "",
            "地区": self.area,
            "产品要求": self.requirements
        }
        # print(result)
        self.write_sql(result)


SH = {
    "login_url": "http://crm.channel.51zhihe.com/#/",
    "area": 0,
    "product": "借了发",
    "username": "jielefa1",
    "password": "123456",
    "message_code": "",
    "channel": "",
    "requirements": "下款3%",
    "remark": ""
}
AH = {
    "login_url": "http://crm.channel.51zhihe.com/#/",
    "area": 1,
    "product": "借了发",
    "username": "jielefa2",
    "password": "123456",
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
























