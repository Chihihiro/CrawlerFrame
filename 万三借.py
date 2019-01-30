# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月25日 20:06
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : 万三借.py
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
            "username": '//*[@id="app"]/div/div[1]/input',
            "password": '//*[@id="app"]/div/div[2]/input',
            "login_button": '//*[@id="app"]/div/button/span',
            "message_code": '',
            "check_code": '',
            "code_image": '',
            "success_ele": '//*[@id="app"]/div/div/div/div[1]/ul/div/a'
        }
        step = [  # 操作步骤
            ("点击看板查看", '//*[@id="app"]/div/div/div/div[1]/ul/div/a', "click")
        ]
        selector = Selector(text=self.login(xpath_info, operation=step))
        info = selector.xpath('//*[@id="app"]/div/div/div/div[2]/div/div/div/div/div/p[2]/text()').re(r'今日注册数量：(\d+)')
        # 最终结果
        result = {
            "注册人数": info[0],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": ""
        }
        # print(result)
        self.write_sql(result)


account_info = {
    "login_url": "http://132.232.115.29/tdss-admin/#/",
    "area": "0",
    "product": "万三借(上海和四平)",
    "username": "56cs2019011203",
    "password": "123456",
    "message_code": "",
    "channel": "",
    "requirements":"",
}

while True:
    try:
        product = Spider(account_info)
        product.get_info()
    except:
        continue
    else:
        sleep(300)


















