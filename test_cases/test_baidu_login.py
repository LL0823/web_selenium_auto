#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: liu
# time: 2024/6/20 11:42
import logging
import time

import allure
import pytest
from page.baidu_homepage import BaiduHomepage

from util.datas_helper import DatasHelper

error_login_data = DatasHelper.get_datas_by_path(__file__, "$.error_login..testcase")
normal_ids = DatasHelper.get_datas_by_path(__file__, "$.error_login..ids")


class TestBaiduLogin:

    @pytest.mark.parametrize("username,password", error_login_data, ids=normal_ids)
    @pytest.mark.smoke
    @allure.feature("登录-账号或密码错误")
    def test_login_fail(self, driver, env, username, password):
        baidu_page = BaiduHomepage(driver)
        baidu_page.open_chrom(env.get('$.base_url'))
        baidu_page.login_input_and_click(username, password)
        assert baidu_page.is_element_exit(*baidu_page.baidu_login_error_wrapper, timeout=2), "没有出现登录失败提示"
