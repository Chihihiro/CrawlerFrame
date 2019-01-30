# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月26日 0:00
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : 锦鲤时代.py
# @Software: PyCharm
# @Describe: 

from scrapy import Selector
from Frame.Crawler import BaseSpider
from Frame.Request import Request
from time import sleep


class Spider(BaseSpider, Request):
    def __init__(self, account):
        super(Spider, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="main"]/div/div/div/div[2]/div/form/div[1]/div/div/input',
            "password": '//*[@id="main"]/div/div/div/div[2]/div/form/div[2]/div/div/input',
            "login_button": '//*[@id="main"]/div/div/div/div[2]/div/form/div[5]/div/button',
            "message_code": '//*[@id="main"]/div/div/div/div[2]/div/form/div[5]/div/button',
            "check_code": '//*[@id="main"]/div/div/div/div[2]/div/form/div[4]/div/div/input',
            "code_image": '//*[@id="s-canvas"]',
            "success_ele": '//*[@id="main"]/div/div[2]/div/div/div/div[2]/div/div/div/div[1]'
        }
        # 获取Cookie值
        html = self.login(xpath_info, image_size=(956, 457, 1130, 500), image_type="10400", operation=[[]])
        # 获取结果
        selector = Selector(text=html)
        result = {
            "注册人数": selector.xpath('//*[@id="main"]/div/div[2]/div/div/div/div[1]/div/div/div[1]/p/text()').re(r"(\d*)")[0],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": "",
            "地区": self.area,
            "产品要求": self.requirements
        }
        # print(result)
        self.write_sql(result)


AH = {
    "login_url": "http://carpcus.wilinkin.cn/#/login",
    "product": "锦鲤时代",
    "username": "jlsd0510",
    "password": "jlsd0510",
    "message_code": "",
    "channel": "",
    "requirements": "下款3 申请40%",
    "remark": "",
    "area": 1
}


account_info = [AH]

while True:
    for i in account_info:
        product = Spider(i)
        product.get_info()
    sleep(600)





