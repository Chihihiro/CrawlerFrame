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


class Spider(BaseSpider, Request):
    def __init__(self, account):
        super(Spider, self).__init__(account)

    def get_info(self):
        # xpath信息
        xpath_info = {
            "username": '//*[@id="app"]/div/div/div[2]/div/div[2]/div[1]/form/div[1]/div/div/input',
            "password": '//*[@id="app"]/div/div/div[2]/div/div[2]/div[1]/form/div[2]/div/div/input',
            "login_button": '//*[@id="app"]/div/div/div[2]/div/div[2]/div[1]/div',
            "check_code": '//*[@id="app"]/div/div/div[2]/div/div[2]/div[1]/form/div[3]/div/div/input',
            "code_image": '//*[@id="app"]/div/div/div[2]/div/div[2]/div[1]/form/div[3]/div/img',
            "success_ele": '//*[@id="app"]/div/div[1]/div[3]/div/ul/li[2]/div'
        }
        # 获取cookie
        cookies = self.login(xpath_info, image_size=(1036, 377, 1107, 408), image_type="30400")
        # 设置参数
        args = {
            'page': '1',
            'agentid': "",
            'startTime': str(int(time.mktime(time.strptime(f"{self.today} 00:00:00", "%Y-%m-%d %H:%M:%S")))),
            'endTime': str(int(time.mktime(time.strptime(f"{self.tomorrow} 00:00:00", "%Y-%m-%d %H:%M:%S"))))
        }
        info = json.loads(
            self.request(
                url="http://mxjz.52jhxinxin.com/admin_agent/mySCustomerList",
                cookie_dict=cookies,
                method="post",
                args=args
            )
        )['body']
        # 最终结果
        result = {
            "注册人数": info['total'],
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
    "login_url": "http://mxjz.52jhxinxin.com/admin/mxjz.html#/sign-in",
    "product": "萌新记账",
    "username": "jie18",
    "password": "123456",
    "message_code": "",
    "channel": "",
    "requirements": "下款3%",
    "area": "0",
    "remark": ""
}

WD = {
    "login_url": "http://mxjz.52jhxinxin.com/admin/mxjz.html#/sign-in",
    "product": "萌新记账",
    "username": "meng30",
    "password": "123456",
    "message_code": "",
    "channel": "",
    "requirements": "下款3%",
    "area": "1",
    "remark": ""

}

account_info = [SH, WD]

while True:
    for i in account_info:
        product = Spider(i)
        product.get_info()
    sleep(1200)

























