#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: liu
# time: 2024/6/19 20:38
import logging
import os

import pytest
import typer

from util.file_helper import FileHelper

app = typer.Typer()


def create_allure_report(allure_result_dir, allure_report_dir):
    shell = f'allure generate {allure_result_dir} -o {allure_report_dir} --clean'
    logging.info('执行命令生成报告：%s', shell)
    os.system(shell)
    logging.info('报告生成完毕，报告路径：%s', allure_result_dir)


@app.command()
def run(env=None, allure_result_dir=None, test_cases="test_cases", pytest_marker=None, reruns=None, reruns_delay=None):
    logging.info('正在执行pytest')
    # allure报告相关路径
    allure_result_dir = FileHelper.get_path('allure-results')
    allure_report_dir = FileHelper.get_path('allure-report')
    if env:
        os.environ['config-env'] = env
    pytest_params = [
        "--alluredir", allure_result_dir,
        "-vs", *test_cases.split(','),
    ]
    if pytest_marker:
        pytest_params.append(f"-m {pytest_marker}")
    if reruns and reruns_delay:
        pytest_params.append(f"--reruns={reruns}")
        pytest_params.append(f"--reruns-delay={reruns_delay}")
    logging.info("pytest参数: %s", pytest_params)
    pytest.main(pytest_params)
    create_allure_report(allure_result_dir, allure_report_dir)


if __name__ == '__main__':
    app()
