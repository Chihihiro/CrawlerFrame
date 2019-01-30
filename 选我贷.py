# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月27日 12:25
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : 选我贷.py
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
            "username": '//*[@id="main"]/div/div/div/div[2]/div/form/div[1]/div/div[1]/input',
            "password": '//*[@id="main"]/div/div/div/div[2]/div/form/div[2]/div/div[1]/input',
            "login_button": '//*[@id="main"]/div/div/div/div[2]/div/form/div[5]/div/button',
            "check_code": '//*[@id="main"]/div/div/div/div[2]/div/form/div[4]/div/div[1]/input',
            "code_image": '//*[@id="s-canvas"]',
            "success_ele": '//*[@id="main"]/div/div[2]/div/div/div/div[2]/div/div/div/div[3]/button'
        }
        # 获取token
        token = self.login(xpath_info, image_size=(1682, 457, 1857, 500), image_type="10400", token_field="bearerToken")
        # json的url
        json_url = f"http://timedata.dgliao.cn/api/Bussiness/GetPartyBAccountData?PartyBId=315&StartTime={self.today}&EndTime={self.today}&Limit=10&Offset=0&format=json"
        info = json.loads(
            self.request(json_url, method="get", token_info=("Authorization", f"""Bearer {token.replace('"', "")}"""))
        )['rows'][0]
        # 最终结果
        result = {
            "注册人数": info['uploadCount'],
            "实名人数": "null",
            "申请人数": 'null',
            "放款人数": 'null',
            "备注": '',
            "地区": self.area,
            "产品要求": self.requirements
        }
        # print(result)
        self.write_sql(result)


SH = {
    "login_url": "http://justc.qkjinrong.cn/#/login",
    "product": "选我贷",
    "username": "rong0407",
    "password": "rong0407",
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



























