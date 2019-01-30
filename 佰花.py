# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月26日 11:14
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : 佰花.py
# @Software: PyCharm
# @Describe: 

import time
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
            "username": '//*[@id="account"]',
            "password": '//*[@id="password"]',
            "login_button": '//*[@id="root"]/div/div/div[2]/div/form/div[4]/div/div/span/button',
            "message_code": '',
            "check_code": '//*[@id="imgCode"]',
            "code_image": '//*[@id="root"]/div/div/div[2]/div/form/div[3]/div/div/span/div/div[2]/img',
            "success_ele": '//*[@id="root"]/div/div/div[1]/div/div/span/span'
        }
        # 获取token
        token = self.login(xpath_info, image_size=(1056, 372, 1128, 422), image_type="30400", token_field="accessToken")
        # json的url地址
        print(token)
        json_url = f"http://47.110.6.255:2009/channel/admin/data"
        args = {
            'channelCode': self.channel,
            'merchantId': "0",
            'registerBeginDate': int(
                time.mktime(time.strptime(f"{self.today} 00:00:00", "%Y-%m-%d %H:%M:%S"))) * 1000,
            'registerEndDate': int(
                time.mktime(time.strptime(f"{self.tomorrow} 00:00:00", "%Y-%m-%d %H:%M:%S"))) * 1000
        }
        info = json.loads(
            self.request(json_url, method="post", token_info=("accessToken", token), args=args, payload=True)
        )['data']['channelDataList'][0]
        # print(info)
        # 最终结果
        result = {
            "注册人数": info['registerCount'],
            "实名人数": "null",
            "申请人数": info['applyCount'],
            "放款人数": info['loanCount'],
            "备注": "",
            "地区": self.area,
            "产品要求": self.requirements
        }
        # print(result)
        self.write_sql(result)


AH = {
    "login_url": "http://zjxg.zaixianjieshu.com/zjxg/H5/flowAdmin/index.html#/user/login",
    "product": "佰花",
    "username": "zfcps",
    "password": "888888",
    "message_code": "",
    "channel": "2019012913RXZEC",
    "requirements": "下款3%",
    "remark": "",
    "area": 1
}

account_info = [AH]

while True:
    for i in account_info:
        product = Spider(i)
        product.get_info()
    sleep(600)














































