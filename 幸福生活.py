# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月26日 10:51
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : 幸福生活.py
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
            "username": '//*[@id="form1"]/div[1]/input',
            "password": '//*[@id="form1"]/div[2]/input',
            "login_button": '//*[@id="form1"]/div[3]/input',
            "message_code": '',
            "check_code": '',
            "code_image": '',
            "success_ele": '/html/body/div/div/div[2]/div/nav/ul/li/a'
        }
        cookie = self.login(xpath_info)  # 获取cookie
        # json的url地址
        json_url = f"http://www.kycn6.com/?s=channel&action=getdatalist&page=1&limit=20"
        info = json.loads(
            self.request(json_url, method="post", cookie_dict=cookie)
        )
        # 最终结果
        result = {
            "注册人数": info["count"],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": "",
            "地区": self.area,
            "产品要求": self.requirements
        }
        # print(result)
        self.write_sql(result)


account_info = {
    "login_url": "http://www.kycn6.com/?s=channel",
    "area": 1,
    "product": "幸福生活",
    "username": "xfsh1",
    "password": "123456",
    "message_code": "",
    "channel": "",
    "requirements": "申请40% 下款3%",
    "remark": ""
}

while True:
    product = Spider(account_info)
    product.get_info()
    sleep(300)


























