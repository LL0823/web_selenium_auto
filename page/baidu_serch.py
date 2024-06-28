#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: liu
# time: 2024/6/20 11:43
import logging

from selenium.webdriver.common.by import By

from util.base_page import BasePage


class BaiduPage(BasePage):
    baidu_input_element = (By.ID, 'kw')
    baidu_search_button_element = (By.ID, 'su')
    baidu_icon = (By.ID, 'lg')

    def open_chrom(self, url):
        self.open(url)

    def find_baidu_icon(self) -> bool:
        return self.is_element_exit(*self.baidu_icon)

    def search_input_text(self, text):
        self.input_text(*self.baidu_input_element, text)
        return self

    def click_search_button(self):
        self.click_element(*self.baidu_search_button_element)

    # 组合操作
    def search_input_and_click(self, text):
        self.search_input_text(text).click_search_button()
