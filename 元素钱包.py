# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月25日 10:44
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : 小牛牛.py
# @Software: PyCharm
# @Describe:

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
            "username": '//*[@id="userMobile"]',
            "password": '//*[@id="userPassword"]',
            "login_button": '//*[@id="jvForm"]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[4]/td/input',
            "message_code": '',
            "check_code": '',
            "code_image": '',
            "success_ele": '//*[@id="header"]/div[1]/ul[1]/li[3]/a'
        }

        step = [
            ("dian", '//*[@id="sidebar"]/div/div[2]/ul/li/div/a', "click")
        ]
        html = self.login(xpath_info, operation=step)
        html = Selector(text=html)
        num = html.xpath('//*[@id="pagerForm"]/div[2]/div[2]/div[2]/div/table/tbody/tr[1]/td[5]/text()').extract()[0].strip()
        fang = html.xpath('//*[@id="pagerForm"]/div[2]/div[2]/div[2]/div/table/tbody/tr[1]/td[7]/text()').extract()[0].strip()
        applications = html.xpath('//*[@id="pagerForm"]/div[2]/div[2]/div[2]/div/table/tbody/tr[1]/td[6]/text()').extract()[0].strip()
        # 最终结果
        result = {
            "注册人数": num,
            "实名人数": "null",
            "申请人数":  applications,
            "放款人数": fang,
            "备注": "",
            "地区": self.area,
            "产品要求": self.requirements
        }
        # print(result)
        self.write_sql(result)


SH = {
    "login_url": "http://back.yuansuqianbao.com/backcashman/back/indexBack#14",
    "product": "元素钱包",
    "username": "15827320005",
    "password": "xrd123456",
    "message_code": "",
    "channel": "",
    "requirements": "下款4%",
    "remark": "",
    "area": 1
}

account_info = [SH]

while True:
    for i in account_info:
        product = Spider(i)
        product.get_info()
    sleep(600)





















