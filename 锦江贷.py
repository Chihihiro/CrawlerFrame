# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月25日 23:15
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : 锦江贷.py
# @Software: PyCharm
# @Describe: 

from scrapy import Selector
from Frame.Crawler import BaseSpider
from Frame.Request import Request
from time import sleep
import time

class Spider(BaseSpider, Request):
    def __init__(self, account):
        super(Spider, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="login_box"]/form/input[2]',
            "password": '//*[@id="login_box"]/form/input[3]',
            "login_button": '//*[@id="login_box"]/form/button',
            "message_code": '',
            "check_code": '',
            "code_image": '',
            "success_ele": '//*[@id="lists"]/li[1]'
        }
        # 获取Cookie值
        cookie = self.login(xpath_info)
        # page的url
        page_url = "http://www.jinjiangdai.com/index/index/user.html"
        # 设置参数
        html = self.request(page_url, cookie_dict=cookie, method="get")
        # 获取结果
        info = Selector(text=html)
        result = {
            "注册人数": info.xpath('//*[@id="divs"]/div[1]/table//tr[2]/td[1]/text()').extract()[0],
            "实名人数": "null",
            "申请人数": info.xpath('//*[@id="divs"]/div[1]/table//tr[2]/td[2]/text()').extract()[0],
            "放款人数": "null",
            "备注": "",
            "地区": self.area,
            "产品要求": self.requirements
        }
        self.write_sql(result)


SH = {
    "login_url": "http://www.jinjiangdai.com/index/index/login.html",
    "area": 0,
    "product": "锦江贷",
    "username": "18658195177",
    "password": "123456",
    "message_code": "",
    "channel": "",
    "requirements": "",
    "remark": ""
}


account_info = [SH]

while True:
    for i in account_info:
        product = Spider(i)
        product.get_info()
    time.sleep(1200)

























