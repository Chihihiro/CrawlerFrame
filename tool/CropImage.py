# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月23日 9:44
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : CropImage.py
# @Software: PyCharm
# @Describe: 
from PIL import Image


def cut_img(filename, size):
    # 打开图片
    old_image = Image.open(filename)
    # 转为灰度图像
    # old_image = old_image.convert("L")
    # 裁剪图片
    new_image = old_image.crop(size)
    # 保存图片
    new_image.save(filename)


























