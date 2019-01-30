# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月27日 11:40
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : 乐先花.py
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
            "username": '/html/body/div/div/div/div[2]/div[1]/input',
            "password": '/html/body/div/div/div/div[2]/div[2]/input',
            "login_button": '/html/body/div/div/div/div[2]/button',
            "message_code": '',
            "check_code": '',
            "code_image": '',
            "success_ele": '/html/body/div[1]/div/ul/li[1]'
        }
        cookie = self.login(xpath_info)  # 获取cookie
        # json的url地址
        json_url = f"https://saas.fin-tech.cn/admin/index.php/linkshare/index/share_count_ajax.html?page=1&limit=10&search_date_start={self.today}&search_date_end={self.today}"
        info = json.loads(
            self.request(json_url, method="get", cookie_dict=cookie)
        )["data"]["0"]
        # 最终结果
        result = {
            "注册人数": info["create_count"],
            "实名人数": "null",
            "申请人数": info["submit_count"],
            "放款人数": info["out_count"],
            "备注": "",
            "地区": self.area,
            "产品要求": self.requirements
        }
        self.write_sql(result)


SH = {
    "login_url": "https://saas.fin-tech.cn/admin/index.php?g=linkshare&m=index",
    "area": 0,
    "product": "乐先花",
    "username": "sz121",
    "password": "sz123",
    "message_code": "",
    "channel": "",
    "requirements": "实名40% 下款3%",
    "remark": ""
}

WD = {
    "login_url": "https://saas.fin-tech.cn/admin/index.php?g=linkshare&m=index",
    "area": 1,
    "product": "乐先花",
    "username": "sz115",
    "password": "sz123",
    "message_code": "",
    "channel": "",
    "requirements": "下款5 认证50",
    "remark": ""
}



account_info = [SH, WD]

while True:
    for i in account_info:
        product = Spider(i)
        product.get_info()
    sleep(600)


























