#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: liu
# time: 2024/6/20 11:43
import logging

from selenium.webdriver.common.by import By

from util.base_page import BasePage


class BaiduHomepage(BasePage):
    baidu_input_element = (By.ID, 'kw')
    baidu_search_button_element = (By.ID, 'su')
    baidu_icon = (By.ID, 'lg')
    baidu_index_login_button = (By.ID, 's-top-loginbtn')

    baidu_login_username_input = (By.XPATH, '//*[@id="TANGRAM__PSP_11__userName"]')
    baidu_login_password_input = (By.XPATH, '//*[@id="TANGRAM__PSP_11__password"]')
    baidu_login_checkbox = (By.XPATH, '//*[@id="TANGRAM__PSP_11__isAgree"]')
    baidu_login_button = (By.XPATH, '//*[@id="TANGRAM__PSP_11__submit"]')
    baidu_login_error_wrapper = (By.XPATH, '//*[@id="TANGRAM__PSP_11__error"]')

    def open_chrom(self, url):
        self.open(url)

    def find_baidu_icon(self) -> bool:
        return self.is_element_exit(*self.baidu_icon)

    def search_input_text(self, text):
        self.input_text(*self.baidu_input_element, text)
        return self

    def click_search_button(self):
        self.click_element(*self.baidu_search_button_element)

    def click_login_button(self):
        self.click_element(*self.baidu_login_button)

    def click_login_checkbox(self):
        self.click_element(*self.baidu_login_checkbox)

    # 组合操作
    def search_input_and_click(self, text):
        self.search_input_text(text).click_search_button()

    def login_input_and_click(self, username='', password=''):
        self.click_element(*self.baidu_index_login_button)
        self.input_text(*self.baidu_login_username_input, username)
        self.input_text(*self.baidu_login_password_input, password)
        self.click_login_checkbox()
        self.click_login_button()
