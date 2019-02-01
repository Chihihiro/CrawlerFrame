# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月25日 20:48
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : 金来购.py
# @Software: PyCharm
# @Describe: 

import json
import time
from Frame.Crawler import BaseSpider
from Frame.Request import Request


class Spider(BaseSpider, Request):
    def __init__(self, account):
        super(Spider, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="app"]/div/div/div[2]/div[2]/div[2]/div[1]/form/div[1]/div/div/input',
            "password": '//*[@id="app"]/div/div/div[2]/div[2]/div[2]/div[1]/form/div[2]/div/div[1]/input',
            "login_button": '//*[@id="app"]/div/div/div[2]/div[2]/div[2]/div[1]/div',
            "message_code": '',
            "check_code": '//*[@id="app"]/div/div/div[2]/div[2]/div[2]/div[1]/form/div[3]/div/div[1]/input',
            "code_image": '//*[@id="app"]/div/div/div[2]/div[2]/div[2]/div[1]/form/div[3]/div/img',
            "success_ele": '//*[@id="app"]/div/div[1]/div[1]'
        }
        # 获取Cookie值
        cookie = self.login(
            xpath_info,
            image_size=(1035, 377, 1110, 411),
            image_type="30400"
        )
        # json的url
        json_url = "http://jlg.lkdjhls.cn/admin_agent/mySCustomerList"
        # 设置参数
        args = {
            'page': '1',
            'agentid': "",
            "startTime": str(int(time.mktime(time.strptime(f"{self.today} 00:00:00", "%Y-%m-%d %H:%M:%S")))),
            "endTime": str(int(time.mktime(time.strptime(f"{self.tomorrow} 00:00:00", "%Y-%m-%d %H:%M:%S"))))
        }
        # 获取数据
        info = json.loads(
            self.request(json_url, method="post", args=args, cookie_dict=cookie)
        )['body']
        # 最终结果
        result = {
            "注册人数": info['total'],
            "实名人数": "null",
            "申请人数": 'null',
            "放款人数": 'null',
            "备注": '',
            "地区": self.area,
            "产品要求": self.requirements
        }
        self.write_sql(result)


SH = {
    "login_url": "http://jlg.lkdjhls.cn/admin/jlg.html#/sign-in",
    "area": 0,
    "product": "金来购",
    "username": "奂4",
    "password": "123456",
    "message_code": "",
    "channel": "",
    "requirements": "下款5 认证50",
    "remark": ""
}

WD = {
    "login_url": "http://jlg.lkdjhls.cn/admin/jlg.html#/sign-in",
    "area": 1,
    "product": "金来购",
    "username": "奂16",
    "password": "123456",
    "message_code": "",
    "channel": "",
    "requirements": "下款3",
    "remark": ""
}

account_info = [WD]

while True:
    for i in account_info:
        product = Spider(i)
        product.get_info()
    time.sleep(1200)



