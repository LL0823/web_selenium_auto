#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: liu
# time: 2024/6/27 10:34
import logging
import os

from util.file_helper import FileHelper
from util.config import Config


class DatasHelper:
    @classmethod
    def py_to_yaml(cls, file):
        """
        根据传入的py文件，直接转换成yaml结尾的同名配置文件
        :param file: 文件路径
        :return:
        """
        return os.path.basename(file).replace('py', 'yaml')

    @classmethod
    def get_datas_by_path(cls, file_path, json_path="$"):
        """
        读取对应file_path相同文件名的yaml文件中，jsonpath取出的值
        :param file_path:
        :param json_path: 不传默认取出所有数据
        :return:
        """
        case_yaml = cls.py_to_yaml(file_path)
        file_path = FileHelper.get_path("test_data", case_yaml)
        test_datas = Config(FileHelper.load_yaml(file_path))
        yaml_datas = test_datas.get_multi(json_path)
        return yaml_datas
