#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/29 0029 15:22 
# @Author : Chihiro 
# @Site :  
# @File : 壹點到.py
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
            "username": '//*[@id="loginform-username"]',
            "password": '//*[@id="loginform-password"]',
            "login_button": '//*[@id="loginForm"]/div[4]/div/button',
            "check_code": '//*[@id="loginform-verifycode"]',
            "code_image": '//*[@id="captchaimg"]',
            "success_ele": '//*[@id="header"]/nav/div[3]/ul/li[1]/button'
        }
        # 获取token
        cookies = self.login(xpath_info, image_size=(1044, 521, 1166, 575), image_type="10400")
        # 设置参数

        info = self.request(
                url=f"https://ydd-agent.dinpinkj.com/agent/customer?tag=new&_csrf=mc-H8cv59AuKN1ycbTOXcxjSK5SHiUbQztxCdokoPsKPNi60BforL8liRtdD_W3CC7lAb5knuglKNIeu8hFRQw%3D%3D&agentId=&rqq={self.today}&rqz={self.today}",
                method="get",
                cookie_dict=cookies
            )
        html = Selector(text=info)
        # print(info)
        num = html.xpath('//div[@class="gopa"]/span[1]/text()').re('共\d+页，(\d+)条数据')
        if num:
            num = num[0]
        else:
            num = len(html.xpath('//*[@id="agent"]/table/tbody/tr'))

        # 最终结果
        result = {
            "注册人数": num,
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": "",
            "地区": self.area,
            "产品要求": self.requirements
        }
        self.write_sql(result)


SH = {
    "login_url": "https://ydd-agent.dinpinkj.com/site/login",
    "product": "壹點到",
    "username": "th15",
    "password": "a123456",
    "message_code": "",
    "channel": "",
    "requirements": "",
    "remark": "",
    "area": 0
}



account_info = [SH]

while True:
    for i in account_info:
        product = Spider(i)
        product.get_info()
    sleep(600)

