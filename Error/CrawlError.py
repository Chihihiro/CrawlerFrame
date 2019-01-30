# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月25日 14:14
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : CrawlError.py
# @Software: PyCharm
# @Describe: 


class MethodError(BaseException):
    def __init__(self, content="method参数只能传入get或者post!"):
        self.content = content

    def __str__(self):
        return self.content


if __name__ == '__main__':
    raise MethodError()


