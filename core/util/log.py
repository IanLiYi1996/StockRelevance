# -*- coding: utf-8 -*-
# @Time    : 2020/7/9 14:47
# @Author  : supinyu
# @File    : log.py

import logging
import time
import os
from core.config import LOG_DIR


class Log(object):
    """
    封装后的logging
    """

    def __init__(self, logger=None, log_cate='nlp-stock-relevance'):
        """
        指定保存日志的文件路径，日志级别，以及调用文件，将日志存入到指定的文件中

        Args:
            logger:  logging 对象
            log_cate: 日志名称前缀
        """

        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        # 创建一个handler，用于写入日志文件
        self.log_time = time.strftime("%Y_%m_%d")
        file_dir = LOG_DIR
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)
        self.log_path = file_dir
        self.log_name = self.log_path + "/" + log_cate + "." + self.log_time + '.log'

        fh = logging.FileHandler(self.log_name, 'a', encoding='utf-8')
        fh.setLevel(logging.INFO)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # 定义handler的输出格式
        formatter = logging.Formatter(
            '[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s]%(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        #  添加下面一句，在记录日志之后移除句柄
        # self.logger.removeHandler(ch)
        # self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()
        ch.close()

    def getlog(self):
        """
        生成一个logger对象

        Returns: 返回生成的logger对象

        """
        return self.logger


logger = Log("nlp-stock").getlog()