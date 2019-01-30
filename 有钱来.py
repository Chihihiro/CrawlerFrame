# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月26日 10:35
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : 有钱来.py
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
            "username": '//*[@id="login"]/form/div/input[1]',
            "password": '//*[@id="login"]/form/div/input[2]',
            "login_button": '//*[@id="login"]/form/button',
            "message_code": '',
            "check_code": '',
            "code_image": '',
            "success_ele": '//*[@id="menu"]/div/a'
        }
        cookie = self.login(xpath_info)  # 获取cookie
        # json的url地址
        json_url = f"https://toupin.cn/qianbaoadm/channel/list"
        args = {
            'addtime_endtime': f'{self.today}',
            'addtime_starttime': f'{self.today}',
            'currentpage': "1"
        }
        info = json.loads(
            self.request(json_url, method="post", cookie_dict=cookie, args=json.dumps(args), payload=False)
        )["data"]
        # 最终结果
        result = {
            "注册人数": info["listnum"],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": ""
        }
        # print(result)
        self.write_sql(result)


account_info = {
    "login_url": "https://toupin.cn/web/channel/",
    "area": "上海",
    "product": "有钱来(安徽and河南)",
    "username": "yqddqb12",
    "password": "112233",
    "message_code": "",
    "channel": ""
}

while True:
    product = Spider(account_info)
    product.get_info()
    sleep(300)


























