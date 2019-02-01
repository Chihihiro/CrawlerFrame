# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月25日 23:15
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : 闲鱼贷.py
# @Software: PyCharm
# @Describe: 

from scrapy import Selector
from Frame.Crawler import BaseSpider
from Frame.Request import Request
from time import sleep
import time
import json


class Spider(BaseSpider, Request):
    def __init__(self, account):
        super(Spider, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="app"]/div/form/div[1]/div/div/input',
            "password": '//*[@id="app"]/div/form/div[2]/div/div[1]/input',
            "login_button": '//*[@id="app"]/div/form/div[3]/div/button',
            "message_code": '',
            "check_code": '',
            "code_image": '',
            "success_ele": '//*[@id="app"]/div/div[2]/ul/div[3]/div/span'
        }
        # 获取Cookie值
        cookie = self.login(xpath_info)
        # cookie = self.login(x)
        # page的url
        page_url = "https://ohmyadmin.happycheer.com/api.php?route=Admin/getTableList&schemaKey=JGD_ADMIN_CHANNEL_JHI-USER_SELECT&page=1&count=10&sessionToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Ijg4MCIsIm5hbWUiOiJ4eWRfc3p5c19kYzAxIiwicmVhbF9uYW1lIjoiXHU3YzczXHU1MTU0XHU5MWQxXHU4NzhkIiwicm9sZV9pZCI6IjMifQ.TFp_NwO-mLhVYQXJ2D8jCbxZ9YMquOBLDiv_Sc37WS4"
        # 设置参数
        arg = {
            "condition": str({"`jhi_user`.`channel`":"xyd_szys_dc01","`jhi_user`.`ctime`": f"{self.today} 00:00:00|{self.tomorrow} 00:00:00"})
        }
        info = json.loads(self.request(page_url, cookie_dict=cookie, method="post", args=arg))['result']['totalCount']

        # 获取结果
        result = {
            "注册人数": info,
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": "",
            "地区": self.area,
            "产品要求": self.requirements
        }
        self.write_sql(result)


SH = {
    "login_url": "https://ohmyadmin.happycheer.com/login",
    "area": 1,
    "product": "闲鱼贷",
    "username": "xyd_szys_dc01",
    "password": "123456",
    "message_code": "",
    "channel": "",
    "requirements": "",
    "remark": ""
}


account_info = [SH]

while True:
    for i in account_info:
        product = Spider(i)
        product.get_info()
    time.sleep(1200)

























