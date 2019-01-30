# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月25日 22:48
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : 钱包借.py
# @Software: PyCharm
# @Describe: 

import json
from time import sleep
from Frame.Crawler import BaseSpider
from Frame.Request import Request


class Spider(BaseSpider, Request):
    def __init__(self, account):
        super(Spider, self).__init__(account)

    def get_info(self):
        # xpath信息
        xpath_info = {
            "username": '//*[@id="form"]/div[1]/input',
            "password": '//*[@id="form"]/div[2]/input',
            "login_button": '//*[@id="form"]/div[3]/input',
            "message_code": '',
            "check_code": '',
            "code_image": '',
            "success_ele": '/html/body/div/div[1]/nav/div/div/button[1]/i'
        }
        cookie = self.login(xpath_info)  # 获取cookie
        # json的url地址
        json_url = f"https://hzf.358fintech.com/drainage/getDrainageInfoListByPartner?pageSize=10&pageNum=0&startDate={self.today}&endDate={self.today}&channelsCode=2&_=1547803151503"
        info = json.loads(
            self.request(json_url, method="get", cookie_dict=cookie)
        )["result"][0]
        # 最终结果
        result = {
            "注册人数": info["channelsShowNumber"],
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
    "login_url": "https://hzf.358fintech.com/user/login;JSESSIONID=7abd854c-ba2a-46c9-bf64-ffaf756284ba",
    "area": 0,
    "product": "钱包借",
    "username": "xcs",
    "password": "xcs123",
    "message_code": "",
    "channel": "",
    "requirements": "下款3% 申请40%",
    "remark": "",

}

account_info = [SH]

while True:
    for i in account_info:
        product = Spider(i)
        product.get_info()
    sleep(1200)








