# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月25日 16:15
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : 小心鑫.py
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
            "username": '//*[@id="fs-login-input-area"]/div[1]/input',
            "password": '//*[@id="fs-login-input-area"]/div[2]/input',
            "login_button": '//*[@id="fs-login-btn"]',
            "message_code": '',
            "check_code": '',
            "code_image": '',
            "success_ele": '//*[@id="fs-frame-menu"]/div[1]/div[1]/a/span[1]'
        }
        # 操作步骤
        step = [
            ('点击造意科技', '//*[@id="fs-frame-menu"]/div[1]/div[1]/div[2]/ul/li[1]/a', 'click'),
            ('点击米兔金融', '//*[@id="fs-frame-wrapper"]/div[3]/div/img', 'click')
        ]
        # 获取html
        html = self.login(xpath_info, operation=step, switch=True, frame_index=1)
        selector = Selector(text=html)
        info = selector.xpath('//*[@id="wrapper"]/div/div[1]/div/div/div[3]/div[2]/div/div[3]/div/div/div/div[3]/div[2]/div[1]/div[2]/div[4]/div/div/div[3]/div/div/div/text()').extract()
        # 获取结果
        result = {
            "注册人数": info[0],
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
    "login_url": "http://bi4.nongyaodai.com:8080/WebReport/ReportServer?op=fs_load&cmd=fs_signin&_=1548404022262",
    "area": 0,
    "product": "小心鑫",
    "username": "mitu",
    "password": "Ai5GHi",
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