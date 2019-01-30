# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月27日 12:06
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : 现金串串.py
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
            "success_ele": '//*[@id="main"]/div/div/div/div[2]/div/form/div[5]/div/button'
        }
        # 获取token
        token = self.login(xpath_info, image_size=(1020, 460, 1137, 494), image_type="10400", token_field="bearerToken")
        # json的url
        json_url = f"http://timedata.dgliao.cn/api/Bussiness/GetPartyBAccountData?PartyBId=590&StartTime={self.today}&EndTime={self.today}&Limit=10&Offset=0&format=json"
        info = json.loads(
            self.request(json_url, method="get", token_info=("Authorization", f"""Bearer {token.replace('"', "")}"""))
        )['rows'][0]
        # 最终结果
        result = {
            "注册人数": info['uploadCount'],
            "实名人数": "null",
            "申请人数": 'null',
            "放款人数": 'null',
            "备注": ''
        }
        # print(result)
        self.write_sql(result)


SH = {
    "login_url": "http://cashcus.ninexinchain.cn/#/login",
    "product": "现金串串(上海and四平)",
    "username": "xianjin583",
    "password": "xianjin583",
    "message_code": "",
    "channel": ""
}
# Spider(SH).get_info()
while True:
    try:
        Spider(SH).get_info()
    except:
        continue
    else:
        sleep(1200)


























