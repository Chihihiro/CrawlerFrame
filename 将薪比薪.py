# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月27日 12:33
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : 将薪比薪.py
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
            "check_code": '//*[@id="imgCode"]',
            "code_image": '//*[@id="root"]/div/div/div[2]/div/form/div[3]/div/div/span/div/div[2]/img',
            "success_ele": '//*[@id="root"]/div/div/div[2]/div[1]/div/ul/li[1]'
        }
        # 获取token
        token = self.login(xpath_info, image_size=(1056, 388, 1147, 424), image_type="30400", token_field="accessToken")
        # 设置参数
        args = {
            'channelCode': "2019010922NVKTI",
            'merchantId': "0",
            'registerBeginDate': int(
                time.mktime(time.strptime(f"{self.today} 00:00:00", "%Y-%m-%d %H:%M:%S"))) * 1000,
            'registerEndDate': int(
                time.mktime(time.strptime(f"{self.tomorrow} 00:00:00", "%Y-%m-%d %H:%M:%S"))) * 1000
        }
        info = json.loads(
            self.request(
                url="http://101.37.191.5:2003/channel/admin/data",
                method="post",
                args=args,
                token_info=("accessToken", token),
                payload=True
            )
        )['data']['channelDataList'][0]
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
        self.write_sql(result)


SH = {
    "login_url": "http://jhszjxbx.zaixianjieshu.com/jhszjxbx/H5/flowAdmin/index.html#/user/login",
    "product": "将薪比薪",
    "username": "tong",
    "password": "123456",
    "message_code": "",
    "channel": "",
    "requirements": "下款3%",
    "remark": "",
    "area": 0
}



account_info = [SH]

while True:
    for i in account_info:
        product = Spider(i)
        product.get_info()
    sleep(600)
























