# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月26日 0:19
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : 万金花.py
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
            "username": '//*[@id="app"]/div/div[2]/form/div[1]/div/div/input',
            "password": '//*[@id="app"]/div/div[2]/form/div[2]/div/div/input',
            "login_button": '//*[@id="app"]/div/div[2]/form/div[3]/button',
            "message_code": '',
            "check_code": '',
            "code_image": '',
            "success_ele": '//*[@id="app"]/div/div[2]/div/a/div/div/h3'
        }
        cookie = self.login(xpath_info)  # 获取cookie
        # json的url地址
        json_url = "https://admin.92douddou.com/admin/channel/list_channel_datail.json"
        args = {
            "limit": "1500",
            "offset": "0",
            'endTime': f"{self.today} 23:59:59",
            'startTime': f"{self.today} 00:00:00"
        }
        info = json.loads(
            self.request(json_url, method="post", cookie_dict=cookie, args=args, payload=True)
        )['data']['items']
        # 最终结果
        result = {
            "注册人数": len(info),
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
    "login_url": "https://admin.92douddou.com/login",
    "product": "万金花",
    "username": "wm10_admin",
    "password": "88888888",
    "message_code": "",
    "channel": "",
    "requirements": "下款3%",
    "remark": "",
    "area": 1

}

while True:
    product = Spider(account_info)
    product.get_info()
    sleep(300)


























