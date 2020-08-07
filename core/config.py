# -*- coding: utf-8 -*-
# @Time    : 2020/7/9 10:37
# @Author  : supinyu
# @File    : config.py

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "../data")

DICT_DIR = os.path.join(DATA_DIR, "user.dict.utf8.20180418")

LOG_DIR = os.path.join(BASE_DIR, "../log")

RESULT_DIR = os.path.join(BASE_DIR, "../result")