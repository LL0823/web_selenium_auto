#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: liu
# time: 2024/6/25 16:44
from selenium import webdriver


class DriverUtil:
    __WebDriver = None

    @classmethod
    def get_web_driver(cls):
        if cls.__WebDriver is None:
            cls.__WebDriver = webdriver.Chrome()
        return cls.__WebDriver
