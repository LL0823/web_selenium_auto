#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: liu
# time: 2024/6/20 11:42
import logging
import time

import allure
import pytest
from page.baidu_serch import BaiduPage

from util.datas_helper import DatasHelper

normal_search_text = DatasHelper.get_datas_by_path(__file__, "$.normal_search..search_text")
normal_ids = DatasHelper.get_datas_by_path(__file__, "$.normal_search..ids")
special_search_text = DatasHelper.get_datas_by_path(__file__, "$.special_search..search_text")
special_ids = DatasHelper.get_datas_by_path(__file__, "$.special_search..ids")


class TestBaidu:

    @pytest.mark.parametrize("search_text", normal_search_text, ids=normal_ids)
    @pytest.mark.smoke
    @allure.feature("普通查询成功功能验证")
    def test_search_normal(self, driver, env, search_text):
        # get方法会一直等到页面被完全加载，然后才会继续程序，通常测试会在这里选择
        # driver.get(env["base_url"])
        baidu_page = BaiduPage(driver)
        baidu_page.open_chrom(env.get('$.base_url'))
        baidu_page.search_input_and_click(search_text)
        assert baidu_page.find_baidu_icon(), "没找到baidu图标"
        # 不等待的情况下，title来不及变更
        time.sleep(2)
        assert baidu_page.title == f"{search_text}_百度搜索", f"title与预期不符，为{baidu_page.title}"

    @pytest.mark.parametrize("search_text", special_search_text, ids=special_ids)
    @pytest.mark.smoke
    @allure.feature("特殊查询成功功能验证")
    def test_search_special(self, driver, env, search_text):
        # get方法会一直等到页面被完全加载，然后才会继续程序，通常测试会在这里选择
        # driver.get(env["base_url"])
        baidu_page = BaiduPage(driver)
        baidu_page.open_chrom(env.get('$.base_url'))
        baidu_page.search_input_and_click(search_text)
        logging.info(baidu_page.find_baidu_icon())
        assert baidu_page.find_baidu_icon(), "没找到baidu图标"
        time.sleep(2)
        if search_text != " ":
            assert baidu_page.title == f"{search_text}_百度搜索", f"title与预期不符，为{baidu_page.title}"
