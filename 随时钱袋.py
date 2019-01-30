# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月25日 11:03
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : 随时钱袋.py
# @Software: PyCharm
# @Describe:

import json
from Frame.Crawler import BaseSpider
from Frame.Request import Request
from time import sleep


class Spider(BaseSpider, Request):
    def __init__(self, account):
        super(Spider, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="main"]/div/div/div/div[2]/div/form/div[1]/div/div[1]/input',
            "password": '//*[@id="main"]/div/div/div/div[2]/div/form/div[4]/div/div[1]/input',
            "login_button": '//*[@id="main"]/div/div/div/div[2]/div/form/div[5]/div/button',
            "message_code": '',
            "check_code": '//*[@id="main"]/div/div/div/div[2]/div/form/div[3]/div/div[1]/input',
            "code_image": '//*[@id="s-canvas"]',
            "success_ele": '//*[@id="service_request_con"]/div[1]/canvas'
        }
        # 获取Cookie值
        token = self.login(
            xpath_info,
            image_size=(1004, 386, 1143, 428),
            image_type="10400",
            token_field="bearerToken"
        )
        # json的url
        json_url = f"http://timedata.dgliao.cn/api/Bussiness/GetPartyBAccountData?PartyBId=977&StartTime={self.today}&EndTime={self.today}&Limit=10&Offset=0&format=json"
        # 设置头部信息
        token_info = ["Authorization", "Bearer {0}".format(token.strip('"'))]
        # 获取数据
        info = json.loads(
            self.request(json_url, method="get", token_info=token_info)
        )["rows"][0]
        # 获取结果
        result = {
            "注册人数": info["uploadCount"],
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
    "login_url": "http://qdaid.wucblock.cn/#/login",
    "area": 0,
    "product": "随时钱贷",
    "username": "ss1967",
    "password": "ss1967",
    "message_code": "",
    "channel": "",
    "requirements": "下款3%",
    "remark": ""
}


account_info = [SH]

while True:
    for i in account_info:
        product = Spider(i)
        product.get_info()
    sleep(1200)



