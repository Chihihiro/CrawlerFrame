# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月25日 13:55
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : Request.py
# @Software: PyCharm
# @Describe: 

from chardet import detect
from requests import Session
from Error import CrawlError


class Request:
    @staticmethod
    def request(url, method="post", cookie_dict=None, token_info=None, args=None, payload=False, custom_header=None):
        """
        :param url: 请求url -- str
        :param method: get或者post  -- str
        :param cookie_dict: cookie值 -- dict
        :param token_info: 列表或者元组 (0:token字段  1:token值)  (字段, 值)
        :param args: 请求参数 -- dict
        :param payload: 是否是PayLoad形式的参数 -- bool
        :param custom_header: 自定义头部信息 -- dict
        """
        session = Session()  # 会话框
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        # 如果已经传入自定义头部
        if custom_header:
            custom_header.update(headers)

        # 如果有Cookie字典
        if cookie_dict:
            # 给session设置cookie
            session.cookies.update(cookie_dict)
        # 如果是token
        elif token_info:
            # 添加token信息
            headers[token_info[0]] = token_info[1]
        # 请求url, 设置浏览器头部与代理ip
        if method == "post":
            if payload:
                response = session.post(url, headers=custom_header if custom_header else headers, json=args)
            else:
                response = session.post(url, headers=custom_header if custom_header else headers, data=args)
        elif method == "get":
            response = session.get(url, headers=custom_header if custom_header else headers)
        else:
            raise CrawlError.MethodError()
        # 指定编码
        code = detect(response.content)["encoding"]
        response.encoding = code
        # 获取结果
        return response.text



