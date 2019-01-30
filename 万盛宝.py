#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/29 0029 13:49 
# @Author : Chihiro 
# @Site :  
# @File : 万盛宝.py 
# @Software: PyCharm



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
            "username": '//*[@id="userName"]',
            "password": '//*[@id="password"]',
            "login_button": '//*[@id="doLogin"]',
            "message_code": '',
            "check_code": '',
            "code_image": '',
            "success_ele": '//*[@id="leftNav"]/li/a'
        }
        cookie = self.login(xpath_info)  # 获取cookie
        # json的url地址
        json_url = f"http://ws.29n0ym.cn/customer/channelUser/getData?page=1&limit=3000&channelId=&customerProvince=&createTimeStart={self.today}&createTimeEnd={self.tomorrow}&infoLevel="
        info = json.loads(
            self.request(json_url, method="get", cookie_dict=cookie)
        )
        print(info)
        # # 最终结果
        result = {
            "注册人数": info['count'],
            "实名人数": 0,
            "申请人数": "null",
            "放款人数": "null",
            "备注": "",
            "地区": self.area,
            "产品要求": self.requirements
        }
        for each_user in info['data']:
            if each_user["infoLevelStr"] != "未填写":
                result["实名人数"] += 1
        # print(result)
        self.write_sql(result)


SH = {
    "login_url": "http://ws.29n0ym.cn/login",
    "area": 1,
    "product": "万盛宝",
    "username": "小牛",
    "password": "Aa123456",
    "message_code": "",
    "channel": "",
    "requirements": "下款3",
    "remark": ""
}



account_info = [SH]

while True:
    for i in account_info:
        product = Spider(i)
        product.get_info()
    sleep(600)



























