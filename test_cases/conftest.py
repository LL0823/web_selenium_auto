#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: liu
# time: 2024/6/20 12:45
import logging
import os
import time

import allure
import pytest
from selenium import webdriver
from util.config import Config
from util.file_helper import FileHelper


@pytest.fixture(scope='session')
def driver(env, request):
    # dr = webdriver.Chrome()
    # dr.maximize_window()
    # # dr = DriverUtil.get_web_driver()
    # yield dr
    # dr.quit()
    global driver_global
    driver_global = webdriver.Chrome()
    driver_global.maximize_window()
    driver_global.implicitly_wait(5)

    def end():
        driver_global.quit()

    request.addfinalizer(end)  # 终结函数
    # 这里为什么不用yield呢因为yield不能return，addfinalizer这个功能可以实现饿yield功能一样
    # 而且可以return参数传给后面的用例
    return driver_global


@pytest.fixture(scope="session")
def env(request):
    config_file_name = "config.yaml"
    env_config = os.environ.get("config-env")
    if env_config:
        config_file_name = f"config-{env_config}.yaml"
    # config_path = os.path.join(FileHelper.get_root_path(), "config", config_file_name)
    config_path = FileHelper.get_path("config", config_file_name)
    config = FileHelper.load_yaml(config_path)
    logging.info(config)
    yield Config(config)


# 编写钩子函数,失败用例自动截图函数
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    获取每个用例的钩子函数
    :param item:
    :param call:
    :return:
    """
    # 获取钩子方法的调用结果
    outcome = yield
    rep = outcome.get_result()
    # 以下为实现异常截图的代码：
    # rep.when可选参数有call、setup、teardown，
    # call表示为用例执行环节、setup、teardown为环境初始化和清理环节
    # 这里只针对用例执行且失败的用例进行异常截图
    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode) as f:
            if "tmpdir" in item.fixturenames:
                extra = " (%s) " % item.funcargs["tmpdir"]
            else:
                extra = ""
            f.write(rep.nodeid + extra + "\n")
        item.name = item.name.encode("utf-8").decode("unicode-escape")
        file_name = '{}.png'.format(time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime()))
        path = FileHelper.get_path("screen", file_name)
        driver_global.save_screenshot(path)

        if hasattr(driver_global, "get_screenshot_as_png"):
            with allure.step("添加失败截图"):
                # get_screenshot_as_png实现截图并生成二进制数据
                # allure.attach直接将截图二进制数据附加到allure报告中
                allure.attach(driver_global.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)
                logging.info("错误页面截图成功，图表保存的路径:{}".format(path))
