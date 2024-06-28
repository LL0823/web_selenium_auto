#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: liu
# time: 2024/6/20 13:22
import json
import logging
import os

import yaml  # 需要pip install pyyaml安装


class FileHelper:
    """
    文件帮助类
    """

    @classmethod
    def get_root_path(cls) -> str:
        """
        获取本项目的根目录
        :return: 项目根目录路径
        """
        current_path = __file__
        split_path = current_path.split(os.path.sep)
        return os.path.sep.join(split_path[:-2])

    @classmethod
    def get_path(cls, *paths) -> str:
        """
        拼接项目根目录，获取指定路径
        示例：Common.get_path("api","haha.txt")
        :param paths: 从根目录开始拼接路径
        :return: 获取指定路径
        """
        return os.path.join(cls.get_root_path(), *paths)

    def load_yaml(yml_path: str, raise_if_not_exists: bool = True):
        logging.info(f"正在读取配置文件: {yml_path}")
        if not os.path.isfile(yml_path):
            if raise_if_not_exists:
                raise AssertionError(f"配置文件不存在：{yml_path}")
            else:
                return None
        with open(yml_path, encoding='utf-8') as f:
            content = yaml.load(f.read(), Loader=yaml.SafeLoader)
        logging.info(f"配置内容：{content}")
        return content
