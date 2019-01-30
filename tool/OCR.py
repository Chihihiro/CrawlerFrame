# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月23日 9:48
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : OCR.py
# @Software: PyCharm
# @Describe: 

from OCR.fateadm_api import TestFunc


def ocr(api_type, file_name):
    # 识别验证码
    code = TestFunc(api_type, file_name)
    return code


























