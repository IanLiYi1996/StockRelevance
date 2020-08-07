# -*- coding: utf-8 -*-
# @Time    : 2020/7/9 15:09
# @Author  : supinyu
# @File    : stock_relevance_2.py

"""
股票相关性V2版本---基于行情的具体需求
"""
import re
import os
import core.model.stock_relevance_1 as stock_v1
from core.util.word_segment import analyse
from collections import defaultdict
from core.config import DATA_DIR


def get_special_symbol(text):
    """
    获取带$的符号标签
    :param text:
    :return:
    """
    symbol_list = []
    symbol_regex = r'\$(.*?)\$'
    id_regex = "\((.*?)\)"
    symbol_pattern = re.compile(symbol_regex, re.S)
    id_pattern = re.compile(id_regex, re.S)
    symbol_result = symbol_pattern.findall(text)
    if symbol_result is not None:
        for item in symbol_result:
            id_result = id_pattern.findall(item)
            if id_result is not None:
                symbol_list.append(id_result[0].upper())
    return symbol_list


def get_text_symbol(text):
    """
    获取普通的股票文本中的股票，输入之前，去掉$$符号
    :param text:
    :return:
    """

    word_seg = analyse(text)
    word_list = [x.value.lower() for x in word_seg]
    word_count = defaultdict(int)
    symbol_count = defaultdict(int)
    for item in word_list:
        word_count[item] = word_count[item] + 1

    uniq_word = set(word_list)

    meanfull_words = stock_v1.HITWORDS.keys() & uniq_word
    if meanfull_words:
        stock_candidates = []
        for word in meanfull_words:
            stock_candidates.extend(stock_v1.HITWORDS[word])
        for stock in set(stock_candidates):
            key_word = stock_v1.query_expansion_dict.get(stock)
            # 将股票symbol也加入到关键词中，同时将symbol设置为小写
            key_word.add(stock.lower())
            key_word = [x.lower() for x in key_word]
            count = 0
            for each in key_word:
                if each in word_count:
                    count = count + word_count.get(each, 0)
            if count > 0:
                symbol_count[stock] = count
    return dict(symbol_count)


def rule_score(title, content):
    symbol_regex = r'\$(.*?)\$'
    symbol_pattern = re.compile(symbol_regex, re.S)
    replace_title = re.sub(symbol_pattern, "", title)
    replace_content = re.sub(symbol_pattern, "", content)
    special_stock = get_special_symbol(content)
    title_stock = {}
    content_stock = {}
    total_stock = defaultdict(int)
    if len(replace_title) > 0:
        title_stock = get_text_symbol(replace_title)
    if len(replace_content) > 0:
        content_stock = get_text_symbol(replace_content)
    if len(title_stock) > 0:
        for item in title_stock:
            total_stock[item] = total_stock[item] + 3
    if len(content_stock) > 0:
        for item in content_stock:
            total_stock[item] = total_stock[item] + content_stock[item]
    if len(special_stock) > 0:
        for item in special_stock:
            total_stock[item] = total_stock[item] + 2
    return total_stock


def scores_v2(title, text):
    result_score_map = {}
    count_score = rule_score(title, text)
    for key, value in count_score.items():
        if value >= 6:
            result_score_map[key.upper()] = 4
        elif 4 <= value < 6:
            result_score_map[key.upper()] = 3
        elif 2 <= value < 4:
            result_score_map[key.upper()] = 2
        else:
            result_score_map[key.upper()] = 1
    return result_score_map


if __name__ == "__main__":
    print("hello")
    text = "我刚刚关注了股票$新北洋(SZ002376)$ 我刚刚关注了股票$中证全指(SH000985)$b站"
    symbol_list = get_special_symbol(text)
    print(symbol_list)
    get_text_symbol(text)
    rule_score(text, text)
    res = scores_v2(text, text)
    print(res)
