# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月27日 11:57
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : 仁信.py
# @Software: PyCharm
# @Describe: 

from scrapy import Selector
from time import sleep
from Frame.Crawler import BaseSpider
from Frame.Request import Request


class Spider(BaseSpider, Request):
    def __init__(self, account):
        super(Spider, self).__init__(account)

    def get_info(self):
        # xpath信息
        xpath_info = {
            "username": '//*[@id="account"]',
            "password": '//*[@id="password"]',
            "login_button": '/html/body/div/div/div/div/div/form/div[4]/button',
            "check_code": '//*[@id="imageCode"]',
            "code_image": '//*[@id="img"]',
            "success_ele": '//*[@id="list"]'
        }
        # 获取cookie
        cookies = self.login(xpath_info, image_size=(1040, 400, 1137, 434), image_type="30400")
        # 设置参数
        args = {
            'startTime': f"{self.today}",
            'endTime': f"{self.today}",
        }
        html = Selector(
            text=self.request(
                url="http://rxkoudai.com/merchant/list",
                cookie_dict=cookies,
                method="post",
                args=args
            )
        )
        # 最终结果
        result = {
            "注册人数": html.xpath('//*[@id="contentTable"]/tbody/tr/td[last()]/text()').extract()[0],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": "",
            "地区": self.area,
            "产品要求": self.requirements
        }
        self.write_sql(result)


SH = {
    "login_url": "http://rxkoudai.com/merchant/login",
    "product": "仁信",
    "username": "YD",
    "password": "a123456",
    "message_code": "",
    "channel": "",
    "requirements": "下款4 认证50",
    "remark": "",
    "area": 0
}

account_info = [SH]

while True:
    for i in account_info:
        product = Spider(i)
        product.get_info()
    sleep(600)



























