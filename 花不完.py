# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月25日 15:46
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : 花不完.py
# @Software: PyCharm
# @Describe: 

from Frame.Crawler import BaseSpider
from Frame.Request import Request
from scrapy import Selector
from time import sleep


class Spider(BaseSpider, Request):
    def __init__(self, account):
        super(Spider, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="account"]',
            "password": '//*[@id="password"]',
            "login_button": '/html/body/div[2]/div/form/div[4]/button',
            "message_code": '',
            "check_code": '//input[@id="checkCode"]',
            "code_image": '//*[@id="check_code"]',
            "success_ele": '//*[@id="admin-offcanvas"]/div/ul/li[2]/a'
        }
        # 获取Cookie值
        cookie = self.login(
            xpath_info,
            image_size=(870, 363, 969, 400),
            image_type="10400"
        )
        # page的url
        page_url = f"https://tg.52yangjie.com/customer/list.htm"
        # 设置参数
        args = {
            "gmtCreateStart": f"{self.today}",
            "gmtCreateEnd": f"{self.today}"
        }
        # 获取数据
        info = self.request(page_url, cookie_dict=cookie, method="post", args=args)
        count = Selector(text=info).xpath(
            '/html/body/div[1]/div[2]/div/div[3]/div/div/div/div/p/span/text()'
        ).extract()
        # 获取结果
        result = {
            "注册人数": count[0],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            '备注': "",
            "地区": self.area,
            "产品要求": self.requirements
        }
        # print(result)
        self.write_sql(result)


SH = {
    "login_url": "https://tg.52yangjie.com/index.htm",
    "area": 0,
    "product": "花不完",
    "username": "22990001",
    "password": "123456",
    "message_code": "",
    "channel": "",
    "requirements": "下款4 认证50",
    "remark": ""
}


account_info = [SH]

while True:
    for i in account_info:
        product = Spider(i)
        product.get_info()
    sleep(600)



























