#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/31 0031 11:33 
# @Author : Chihiro 
# @Site :  
# @File : 租钱花.py 
# @Software: PyCharm



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
            "username": '/html/body/div/div/div/form/div[1]/input',
            "password": '/html/body/div/div/div/form/div[2]/input',
            "login_button": '/html/body/div/div/div/form/div[3]/div[1]/button',
            "message_code": '',
            "check_code": '',
            "code_image": '',
            "success_ele": '//*[@id="main-layout"]/div[2]/div[1]/ul/li/a'
        }
        cookie = self.login(xpath_info)  # 获取cookie
        # json的url地址
        url = f"http://zqh.lingzong.vip:8080/admin/admin/order/jjhyq?start={self.today}&end={self.tomorrow}&page=1"
        info = self.request(url, method="get", cookie_dict=cookie)
        # 最终结果
        html = Selector(text=info)
        num = html.xpath('//*[@id="node-1"]/td[1]/text()').extract()

        # print(html.xpath('//tbody/tr[last()]/td[1]/text()').extract())
        result = {
            "注册人数": num[-1],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": "",
            "地区": self.area,
            "产品要求": self.requirements
        }
        # print(result)
        self.write_sql(result)


SH = {
    "login_url": "http://zqh.lingzong.vip:8080/admin/login/jjhyq/88594834890c46288f9dfca036ef1adf",
    "area": 0,
    "product": "租钱花",
    "username": "jjhyq",
    "password": "222333",
    "message_code": "",
    "channel": "",
    "requirements": "下款3%",
    "remark": "",

}

account_info = [SH]

while True:
    for i in account_info:
        product = Spider(i)
        product.get_info()
    sleep(1200)








