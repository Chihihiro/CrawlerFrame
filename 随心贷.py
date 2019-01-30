#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/28 0028 13:08 
# @Author : Chihiro 
# @Site :  
# @File : 随心贷.py 
# @Software: PyCharm



import time
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
            "username": '//*[@id="rrapp"]/div[2]/div[1]/input',
            "password": '//*[@id="rrapp"]/div[2]/div[2]/input',
            "login_button": '//*[@id="rrapp"]/div[2]/div[4]/div[2]/button',
            "message_code": '',
            "check_code": '//*[@id="rrapp"]/div[2]/div[3]/input',
            "code_image": '//*[@id="rrapp"]/div[2]/div[3]/img',
            "success_ele": '//*[@id="rrapp"]/header/nav/div[2]/ul/li[2]/a'
        }
        cookies = self.login(xpath_info, image_size=(1018, 441, 1113, 476), image_type="305000001")
        url = f"http://139.224.76.73//getRegisterCount?_search=false&nd={str(int(time.time()*1000))}&size=10&current=1&sidx=&order=asc&startTime={self.today}&endTime={self.today}&channelCode=youjie2&_={str(int(time.time()*1000))}"
        info = json.loads(self.request(
            url=url,
            cookie_dict=cookies,
            method="get"
        ))["records"][0]
        print(info)

        # 最终结果
        result = {
            "注册人数": info['registerCount'],
            "实名人数": "null",
            "申请人数": info['applyCount'],
            "放款人数": info['payCount'],
            "备注": "",
            "地区": self.area,
            "产品要求": self.requirements
        }
        # print(result)
        self.write_sql(result)


AH = {
    "login_url": "http://139.224.76.73/login.html",
    "product": "随心贷",
    "username": "优借",
    "password": "66668888",
    "message_code": "",
    "channel": "",
    "requirements": "实名40% 下款3%",
    "remark": "",
    "area": 1
}

account_info = [AH]

while True:
    for i in account_info:
        product = Spider(i)
        product.get_info()
    sleep(600)














































