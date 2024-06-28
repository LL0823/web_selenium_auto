#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: liu
# time: 2024/6/20 16:13
import logging
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException


class BasePage:
    url = None

    def __init__(self, driver):  # 初始化传入driver
        self.driver = driver  # 绑定页面对象

    @property
    def title(self):
        return self.driver.title

    @property
    def page_source(self):
        return self.driver.page_source

    def open(self, url=None):
        url = url or self.url  # 如果没有指定url则打开页面url
        logging.info(f'打开 {url}')
        if url:
            self.driver.get(url)
        return self  # 返回self以支持链式操作如page.open('').click_element('')

    def wait(self, secs=1):
        logging.info(f"等待 {secs}s")
        sleep(secs)
        return self

    def find_element(self, by, value, timeout=None, ignore_error=False):
        """元素定位方法增加显式等待和忽略异常选项（处理偶现元素）"""
        try:
            if timeout is None:
                return self.driver.find_element(by, value)
            else:
                return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))
        except NoSuchElementException:
            if ignore_error is False:  # 不忽略错误则抛出异常
                raise

    def click_element(self, by, value, timeout=None, ignore_error=False):
        logging.info(f'点击元素 {by}={value} 超时 {timeout} 忽略异常 {ignore_error}')
        self.find_element(by, value, timeout, ignore_error).click()
        return self

    def input_text(self, by, value, text, timeout=None):
        logging.info(f'向元素 {by}={value} 输入文本 {text} 超时 {timeout}')
        elm = self.find_element(by, value, timeout)
        elm.clear()
        elm.send_keys(text)
        return self

    def move_to_element(self, by, value):
        logging.info('移动到元素 {by}={value}')
        elm = self.find_element(by, value)
        ActionChains(self.driver).move_to_element(elm).perform()
        return self

    def switch_to_frame(self, *frames):
        logging.info(f'切换到框架 {" > ".join(frames)}')
        for frame in frames:
            self.driver.switch_to.frame(frame)

    def switch_to_window(self, index):
        logging.info(f'切换到第{index + 1}个窗口')
        window_list = self.driver.window_handles
        self.driver.switch_to.window(window_list[index])
        return self

    def dismiss_alert(self, ignore_error=False):
        logging.info("关闭警告弹框")
        try:
            self.driver.switch_to.alert().dissmiss()
        except NoAlertPresentException:
            if ignore_error is False:
                raise
        return self

    def remove_attr(self, by, value, attr):
        logging.info(f'移除元素 {by}={value} {attr}属性')
        elm = self.find_element(by, value)
        js_script = f'arguments[0].removeAttribute("{attr}");'
        self.driver.execute_script(js_script, elm)
        return self

    def is_element_exit(self, by, value, timeout=None, ignore_error=False):
        try:
            self.find_element(by, value, timeout, ignore_error)
        except NoSuchElementException:
            logging.error("元素在页面不存在，请排查。")
            return False
        return True
