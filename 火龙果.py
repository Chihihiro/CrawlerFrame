# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月25日 23:41
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : 萌新记账.py
# @Software: PyCharm
# @Describe: 

import json
import time
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
        # 获取cookie
        cookies = self.login(xpath_info, image_size=(1002, 501, 1084, 536), image_type="10400")
        # 设置参数
        args = {
            'page': '1',
            'agentid': "",
            'startTime': str(int(time.mktime(time.strptime(f"{self.today} 00:00:00", "%Y-%m-%d %H:%M:%S")))),
            'endTime': str(int(time.mktime(time.strptime(f"{self.tomorrow} 00:00:00", "%Y-%m-%d %H:%M:%S"))))
        }
        url = f"https://hlg-agent.qidiandian168.com/agent/customer?tag=new&_csrf=BHQBR5SlQDyhyyadxNFu_wdlgpsoML6rSQwkSqPt6JSS2WU94h6DDYtFbxFXA_Nq8OQ-w5l3mhaCaAl90Y88wg%3D%3D&agentId=&rqq={self.today}&rqz={self.today}"
        html = self.request(
                url=url,
                cookie_dict=cookies,
                method="get",)
        # 最终结果
        info = Selector(text=html)
        num = info.xpath("//div[@class='gopa']/span[1]/text()").re('共\d+页，(\d+)条数据')[0]
        # print(num)
        result = {
            "注册人数": num,
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
    "login_url": "https://hlg-agent.qidiandian168.com/site/login",
    "product": "火龙果",
    "username": "kaxi44",
    "password": "123456",
    "message_code": "",
    "channel": "",
    "requirements": "下款3%",
    "area": 0,
    "remark": ""
}

WD = {
    "login_url": "https://hlg-agent.qidiandian168.com/site/login",
    "product": "火龙果",
    "username": "kaxi45",
    "password": "123456",
    "message_code": "",
    "channel": "",
    "requirements": "申请40% 下款3%",
    "area": 1,
    "remark": ""

}

account_info = [SH, WD]

while True:
    for i in account_info:
        product = Spider(i)
        product.get_info()
    sleep(1200)

























