# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月23日 9:39
# @Author  : Joyce
# @Project : CrawlerFrame
# @File    : Crawler.py
# @Software: PyCharm
# @Describe: 爬虫框架

import pymysql
from time import sleep
from tool.OCR import ocr
from tool.CropImage import cut_img
from tool.DealWithCookie import cookie_to_dict
from datetime import datetime, date, timedelta
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException, NoAlertPresentException


class BaseSpider:
    """
    主要功能:
    1)动态获取cookie/token信息
    2)识别图形验证码
    3)将数据写入MySQL数据库中
    """
    def __init__(self, account):
        self.driver = Chrome()  # 模拟浏览器
        self.wait = WebDriverWait(self.driver, 10)
        self.login_url = account["login_url"]  # 登录地址
        self.product = account["product"]  # 产品名称
        self.area = account["area"]  # 地区
        self.user_name = account["username"]  # 帐号
        self.password = account["password"]  # 密码
        self.remark = account["remark"]  # 备注
        self.requirements = account["requirements"]  # 产品要求
        self.message_code = account["message_code"]  # 短信验证码
        self.channel = account["channel"]  # 渠道
        self.now = datetime.now()  # 当前时间
        self.today = date.today()  # 今天日期
        self.yesterday = self.today - timedelta(days=1)  # 昨天日期
        self.tomorrow = self.today + timedelta(days=1)  # 明天日期

    def login(self, xpath_dict, image_size=None, image_type=None, token_field=None, operation=None, switch=False, frame_index=0):
        """
        xpath_info  : 表单元素的xpath值(Dict)
        image_size  : 图像裁剪尺寸(Tuple)
        ocr_type    : 识别类型(String)
        token_field : Token字段名称(String)
        登录页面
        """
        self.driver.maximize_window()
        # 登录页面
        self.driver.get(self.login_url)
        # 设置等待时间
        # **************************** 查找所有表单元素 ****************************
        username = self.wait.until(  # 帐号输入框
            EC.presence_of_element_located((By.XPATH, xpath_dict["username"]))
        )
        password = self.wait.until(  # 密码输入框
            EC.presence_of_element_located((By.XPATH, xpath_dict["password"]))
        )
        login_button = self.wait.until(  # 登录按钮
            EC.presence_of_element_located((By.XPATH, xpath_dict["login_button"]))
        )
        # 如果有图形验证码
        if xpath_dict["check_code"] and xpath_dict["code_image"]:
            code_image = self.wait.until(  # 图形验证码
                EC.presence_of_element_located((By.XPATH, xpath_dict["login_button"]))
            )
            code_input = self.wait.until(  # 验证码输入框
                EC.presence_of_element_located((By.XPATH, xpath_dict["check_code"]))
            )
            sleep(1)
            code_image.click()  # 切换验证码
            sleep(5)
            image_name = f"{self.product}.png"  # 图片名称
            self.driver.save_screenshot("Image/"+image_name)  # 截屏
            print("截图完毕!")
            sleep(2)
            cut_img("Image/"+image_name, image_size)  # 裁剪图像
            print("切图完毕!")
            code = ocr(image_type, image_name)  # 图像转文字
            print(code)
            try:
                code_input.send_keys(code)  # 输入验证码
            except StaleElementReferenceException:
                self.driver.find_element_by_xpath(xpath_dict["check_code"]).send_keys(code)

        # 输入帐号、密码
        try:
            username.send_keys(self.user_name)
            password.send_keys(self.password)
        except StaleElementReferenceException:
            self.driver.find_element_by_xpath(xpath_dict["username"]).send_keys(self.user_name)
            self.driver.find_element_by_xpath(xpath_dict["password"]).send_keys(self.password)
        if self.message_code:
            message = self.wait.until(  # 短信验证码输入框
                EC.presence_of_element_located((By.XPATH, xpath_dict["message_code"]))
            )
            try:
                message.send_keys(self.message_code)
            except StaleElementReferenceException:
                self.driver.find_element_by_xpath(xpath_dict["message_code"]).send_keys(self.message_code)

        # 点击登录按钮
        try:
            login_button.click()
        except StaleElementReferenceException:
            self.driver.find_element_by_xpath(xpath_dict["login_button"]).click()

        try:
            self.wait.until(  # 图形验证码
                EC.presence_of_element_located((By.XPATH, xpath_dict["success_ele"]))
            )
        except TimeoutException:
            self.driver.refresh()
            self.login(xpath_dict, image_size=image_size, image_type=image_type)
        except NoAlertPresentException:
            self.driver.switch_to.alert.accept()
            self.login(xpath_dict, image_size=image_size, image_type=image_type)
        else:
            print("登陆成功...")
            sleep(5)

        if token_field:
            return self._get_token(token_field)
        elif operation:
            return self._get_html(operation, switch=switch, frame_index=frame_index)
        else:
            return self._get_cookie()

    def _get_cookie(self):
        """ 获取Cookie值 """
        cookie = self.driver.get_cookies()
        self.driver.quit()
        return cookie_to_dict(cookie)

    def _get_token(self, token_field):
        """ 通过js获取token值 """
        js = f"return window.localStorage.{token_field};"
        token = self.driver.execute_script(js)
        self.driver.quit()
        return token

    def _get_html(self, step=None, switch=False, frame_index=0):
        """
        step = [
            (步骤名称1, xpath, "click/input", "要输入的值"),
            (步骤名称2, xpath, "click/input", "要输入的值"),
            ......
            (步骤名称n, xpath, "click/input", "要输入的值")
        ]
        如果什么操作都没有, 而且希望获取html  step=[[]]
        """
        if step and step[0]:
            for each_step in step:
                element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, each_step[1]))
                )
                if each_step[2] == "click":
                    element.click()
                else:
                    element.send_keys(each_step[-1])
                sleep(3)  # 延迟三秒
        if switch:  # 是否要切换窗口 进入浮动框架
            """
            //获取页面所有浮动框架  -- js脚本
            document.getElementsByTagName("iframe");
            """
            frame = self.driver.find_elements_by_tag_name("iframe")[frame_index]  # 找到浮动框架
            src = frame.get_attribute("src")  # 提取src属性
            print('窗口切换..................')
            print(src)
            self.driver.switch_to.frame(frame)  # 切换窗口 进入浮动框架
            sleep(2)

        html = self.driver.page_source  # 获取html
        self.driver.quit()
        return html

    # 将数据写入MySQL数据库
    def write_sql(self, ht_info):
        # 连接数据库
        connect = pymysql.connect("192.168.10.180", "root1", "123456", "spider", 3306)
        # 获取游标
        cursor = connect.cursor()
        # 生成SQL语句
        info = {
            "产品名称": self.product,
            "注册人数": ht_info["注册人数"],
            "实名人数": ht_info["实名人数"],
            "申请人数": ht_info["申请人数"],
            "放款人数": ht_info["放款人数"],
            "当前时间": str(self.now),
            "备注": ht_info["备注"],
            "地区": ht_info["地区"],
            "产品要求": ht_info["产品要求"]
        }
        # 执行SQL语句
        sql = """
            insert into  ht_data (product_name,
            register_count,realname_count,apply_count,success_count,now,status,remark,area,requirements)
             VALUES ("{产品名称}",{注册人数},{实名人数},{申请人数},{放款人数},"{当前时间}", 1, "{备注}",{地区},"{产品要求}") 
            on DUPLICATE KEY UPDATE  product_name = VALUES(`product_name`),
            register_count = VALUES(`register_count`),
            apply_count = VALUES(`apply_count`),
            realname_count = VALUES(`realname_count`),
            success_count = VALUES(`success_count`),
            now = VALUES(`now`),
            status = VALUES(`status`), 
            remark = VALUES(`remark`),
            area = VALUES(`area`),
            requirements = VALUES(`requirements`)""".format_map(info)
        cursor.execute(sql)
        # 提交事务
        connect.commit()
        print(info)
        # 关闭连接
        cursor.close()
        connect.close()

    def get_info(self):
        pass






