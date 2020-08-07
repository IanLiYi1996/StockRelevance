# -*- coding: utf-8 -*-
# @Time    : 2020/7/9 10:44
# @Author  : supinyu
# @File    : word_segment.py

# -*- coding:utf-8 -*-
import re

import jieba
import os
from jieba import analyse as jieba_analyse
import jieba.posseg as pseg

from core.util.word import word
from core.config import DATA_DIR as dict_dir

AFTER_NUM = """%KWw万世个买亿以价位余倍億元克再几刀分到千卖只台号名后吨周块增多天套季家寸层岁平年度座开张强成或手才折指支斤日月条板楼次毛派清点瓶百秒米级线美股至萬补辆进连送页项％"""

TEXT_CLEAN_PIPLINE = [
    {
        "pattern": re.compile(r"&nbsp;"),
        "replace": "SPACE",
        "enable": True
    },
    {
        # HTML 标签正则
        "pattern": re.compile(r'&[a-z0-9]+;|'
                              r'<[a-z/][^>]*>|'
                              r'http[^ <>]+|'
                              r'<.*?>'),
        "replace": "_HTML_",
        "enable": True
    },
    {
        "pattern": re.compile(r'(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|'
                              r'[a-z0-9.\-]+[.](?:com|net|org|edu|gov|'
                              r'mil|aero|asia|biz|cat|coop|info|int|jobs|'
                              r'mobi|museum|name|post|pro|tel|travel|xxx|'
                              r'ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|'
                              r'at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|'
                              r'bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|'
                              r'cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|'
                              r'cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|'
                              r'eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|'
                              r'gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|'
                              r'gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|'
                              r'il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|'
                              r'kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|'
                              r'li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|'
                              r'mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|'
                              r'mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|'
                              r'nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|'
                              r'pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|'
                              r'sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|'
                              r'sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|'
                              r'tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|'
                              r'ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|'
                              r'ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\['
                              r'\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|'
                              r'\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)'
                              r'[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};'
                              r':\'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:'
                              r'[.\-][a-z0-9]+)*[.](?:com|net|org|edu|'
                              r'gov|mil|aero|asia|biz|cat|coop|info|int|'
                              r'jobs|mobi|museum|name|post|pro|tel|'
                              r'travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|'
                              r'ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|'
                              r'bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|'
                              r'by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|'
                              r'co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|'
                              r'do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|'
                              r'fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|'
                              r'gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|'
                              r'ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|'
                              r'jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|'
                              r'kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|'
                              r'mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|'
                              r'ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|'
                              r'ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|'
                              r'pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|'
                              r'ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|'
                              r'sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|'
                              r'td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|'
                              r'tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|'
                              r'vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?'
                              r'!@)))'),
        "replace": "_URL_",
        "enable": True
    },
    {
        # 金@钱的部分正则
        "pattern": re.compile(r"\[¥([.0-9]+)\]"),
        "replace": "_MONEY_",
        "enable": True
    },
    {
        # 表情
        "pattern": re.compile(r"(?:\[仰慕\]|\[韭菜\]|\[捂脸\]|\[减\]|"
                              r"\[生气\]|\[困\]|\[难过\]|\[秘密\]|"
                              r"\[能力圈\]|\[中签\]|\[无语\]|\[不赞\]|"
                              r"\[多\]|\[围观\]|\[诅咒\]|\[笑\]|"
                              r"\[抄底\]|\[停\]|\[困惑\]|\[干杯\]|"
                              r"\[大笑\]|\[好逊\]|\[俏皮\]|\[尴尬\]|"
                              r"\[凋谢\]|\[加仓\]|\[可爱\]|\[调皮\]|"
                              r"\[哭泣\]|\[主力\]|\[鼓鼓掌\]|\[护城河\]|"
                              r"\[毛估估\]|\[加油\]|\[赞\]|\[滴汗\]|"
                              r"\[抠鼻\]|\[晕\]|\[关灯吃面\]|\[卖出\]|"
                              r"\[哈哈\]|\[加\]|\[傲慢\]|\[空仓\]|"
                              r"\[贬\]|\[挣扎\]|\[心心\]|\[涨\]|"
                              r"\[看多\]|\[屎\]|\[卖\]|\[献花花\]|"
                              r"\[握手\]|\[怒了\]|\[梭哈\]|\[闭嘴\]|"
                              r"\[讨厌\]|\[跪了\]|\[买\]|\[满仓\]|"
                              r"\[心碎了\]|\[吐血\]|\[傲\]|\[汗\]|"
                              r"\[复盘\]|\[买入\]|\[呵呵傻逼\]|\[哭\]|"
                              r"\[赚大了\]|\[贪财\]|\[害羞\]|\[笑哭\]|"
                              r"\[摊手\]|\[很赞\]|\[成交\]|\[不说了\]|"
                              r"\[空\]|\[疑问\]|\[赞成\]|\[亲亲\]|"
                              r"\[跌\]|\[微笑\]|\[看空\]|\[割肉\]|"
                              r"\[可怜\]|\[心碎\]|\[吐舌\]|\[献花\]|"
                              r"\[色\]|\[减仓\]|\[一坨屎\]|\[好困惑\]|"
                              r"\[好失望\]|\[失望\]|\[卖身\]|\[胜利\]|"
                              r"\[鼓掌\]|\[国家队\]|\[不屑\]|\[爱\]|"
                              r"\[跳水\]|\[不知道\]|\[困顿\]|\[呵呵\]|"
                              r"\[牛\]|\[为什么\]|\[想一下\]|\[亏大了\]|"
                              r"\[囧\]|\[思考\])"),
        "replace": "_EXPRESSION_",
        "enable": True
    },
    {
        # @用户正则
        "pattern": re.compile(r"[@＠]([\u4E00-\u9FFFa-zA-Z0-9_-]{2,})"),
        "replace": "_USER_",
        "enable": True
    },
    {
        # 匹配时间格式问题
        "pattern": re.compile(
            r"[0-9]{4}[0-9]{2}[0-9]{2}[0-9]{2}[0-9]{2}[0-9]{2}|"
            r"[0-9]{4}[0-9]{2}[0-9]{2}|"
            r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}|"
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}|"
            r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}"
            r"(([0-9]|一|二|三|四|五|六|七|八|九|十)+[ ]*(年|月|日|季度|年度|月份|小时|分钟|刻钟|刻|秒)+)+|"
            r"[0-9]+(:|：)[0-9]+|"
            r"[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}|"
            r"(本|上|下)?(周|星期)(一|二|三|四|五|六|日|末)"
            ),
        "replace": "_TIME_",
        "enable": True
    },
    {
        "pattern": re.compile(r"(\d+)%|(\-|\+)\d+(\.\d+)%?"),
        "replace": "_PERCENT_",
        "enable": True
    },
    {
        "pattern": re.compile(r"[\+\-]?[0-9]+\.[0-9]+|"  # 小数
                              r"[\+\-]?[0-9]+%|"  # 百分数
                              r"[\+\-]?[0-9]+|"  # 整数
                              r"[0-9]{7,}|"  # 啥？
                              r"[,0-9\.]+(百|千|万|亿|元|块)|"  # 钱
                              # 中文百分数
                              r"(百分之|千分之|万分之)([0-9]|一|二|三|四|五|六|七|八|九|十)+|"
                              r"￥[0-9\.]+",  # 人民币
                              re.X | re.M),
        "replace": "_NUMBER_",
        "enable": False
    }
]


def read_words(names):
    """
    read data from file
    Args:
        names: file names

    Returns:
        words:
    """
    words = set()
    for name in names:
        with open(os.path.join(dict_dir, name), 'r', encoding='utf-8') as f:
            words.update(set(filter(lambda line: line != '', map(
                lambda line: line.strip(), f.readlines()))))
    return words


# 停用词
stop_words = read_words(['stopwords.txt'])

USER_DICT_VERSION = "20180418"


def init_jieba(user_dict_version):
    """
    初始化jieba分词
    Args:
        user_dict_version: 结巴分词的字典版本

    Returns:

    """
    user_dict_path = "{}/user.dict.utf8.{}".format(
        dict_dir, USER_DICT_VERSION)
    jieba.load_userdict(user_dict_path)
    print('Load dict: %s.' % user_dict_version)


init_jieba(USER_DICT_VERSION)

COMBINE_TH = 3


def load_stock(filename):
    d = set()
    for line in open(filename, encoding='utf-8'):
        d.add(line.strip())
    return d


stock_set = load_stock('{}/stock'.format(dict_dir))


def check_ner(word_value):
    """
    根据实体词典做实体标注
    Args:
        词的文本值
    return:
        实体标注结果
    """
    if word_value in stock_set:
        return "_STOCK_"
    elif re.match("\d*\.?\d+$", word_value):
        return "_NUMBER_"
    # elif word_value in zuhe_words:
    #     return "_ZUHE_"
    else:
        return


def combine_words(list_of_words):
    """
    根据自定义词典合并多个词
    Args:
        list_of_words: 连续的多个词

    Returns:
        如果能合并则返回合并的词，否则返回None
    """
    list_of_words = list_of_words[::-1]
    s = "".join([x.value for x in list_of_words])
    c = check_ner(s)
    if c:
        w = word(s, list_of_words[0].start, list_of_words[-1].end)
        w.ner = c
        w.part_of_speech = "n"
        return w
    else:
        return


def cut_sub_string(substring, last_pos):
    """
    对分段后的文本数据进行分词
    Args:
        substring: 文本，该文本中已不包含TEXT_CLEAN_PIPLINE模式可匹配的串

    Returns:
        last_pos: 该文本在原文本中的起始地址
    """
    main_stack = []
    for w, p in pseg.cut(substring):
        this_word = word(w, last_pos, last_pos + len(w))
        this_word.part_of_speech = p
        if this_word.value in stop_words:
            this_word.is_stop_word = True
        last_pos = last_pos + len(w)
        ner = check_ner(w)
        if ner:
            this_word.ner = ner
            this_word.part_of_speech = "n"
            this_word.is_stop_word = False
            main_stack.append(this_word)
        elif main_stack:  # 向后查找
            t = main_stack.pop()
            list_of_words = [this_word, t]
            c = combine_words(list_of_words)
            if c:
                main_stack.append(c)
            else:
                i = 0
                while i < COMBINE_TH and main_stack:
                    t = main_stack.pop()
                    list_of_words.append(t)
                    c = combine_words(list_of_words)
                    if c:
                        main_stack.append(c)
                        break
                    i += 1
                else:
                    main_stack.extend(list_of_words[::-1])

        else:
            main_stack.append(this_word)
    return main_stack


def analyse(text):
    """
        词级别数据分析:
            0. 匹配奇异值
            1. 去除停用词
            2. 组合发现
            3. 股票发现

        Args:
            text: 文本，

        Returns:
            final: 分析结果
    """
    text = text.strip().lower()
    tags = []
    for p in TEXT_CLEAN_PIPLINE:
        if not p["enable"]:
            continue
        for t in p["pattern"].finditer(text):
            pattern_start, pattern_end = t.span()
            for substring in tags:
                left, right = substring.start, substring.end
                if (pattern_start < left and pattern_end >= left) or \
                        (pattern_start >= left and pattern_start < right):
                    break
            else:
                w = word(text[pattern_start: pattern_end],
                         pattern_start, pattern_end)
                w.ner = p["replace"]
                tags.append(w)
    tags_sorted = sorted(tags, key=lambda x: x.start)
    last_pos = 0
    words = []
    if tags_sorted:
        for r in tags_sorted:
            if (r.start - last_pos < 1):
                last_pos = r.end
                continue
            ws = cut_sub_string(text[last_pos:r.start], last_pos)
            words.extend(ws)
            last_pos = r.end
        ws = cut_sub_string(text[last_pos:], last_pos)
        words.extend(ws)
    else:
        ws = cut_sub_string(text, last_pos)
        words.extend(ws)
    final = sorted(tags_sorted + words, key=lambda x: x.start)
    # final = remerge(final)
    return final


def remerge(words):
    final = []
    i = 0
    while i < len(words) - 1:
        if words[i].ner == "_NUMBER_":
            if words[i + 1].value in AFTER_NUM:
                w = word(words[i].value + words[i + 1].value,
                         words[i].start, words[i + 1].end)
                w.ner = "_NUMBER_"
                w.part_of_speech = "n"
                final.append(w)
                i += 1
            else:
                final.append(words[i])
        else:
            final.append(words[i])
        i += 1
    return final


def cut(text):
    """
        Args:
            text: 文本，

        Returns:
            final: 分词结果, List
    """
    return [w.value for w in analyse(text) if w.is_stop_word is False]


def extract_keywords(text, topk=5, method="tf-idf"):
    """
    关键词提取
    Args:
        text:
        topk:
        method:

    Returns:

    """
    # sentence = "".join([w.value for w in text])
    if method == "textrank":
        return jieba_analyse.textrank(sentence=text, topK=topk, withWeight=True)
    else:
        return jieba_analyse.tfidf(sentence=text, topK=topk, withWeight=True)


if __name__ == "__main__":
    t = r"""$中顺洁柔(SZ002511)$ 中顺洁柔(sz002511)发布2019年一季报，符合预期，近期木浆价格下行弹性显现，盈利水平环比显著回暖。产品结构不断优化，渠道布局持续扩张，全国性产能布局持续进行，业绩高增长可期。广发轻工赵中平认为产品渠道双轮驱动构筑公司核心竞争力，高毛利产品占比提升调整产品结构，各生产基地产能投产计划打开增长瓶颈。公司未来渠道扩张优势及新品研发核心壁垒有望持续助力公司业绩增长"""
    # d = analyse(t)
    # from IPython import embed
    # embed()
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--text",
        type=str,
        default=t,
    )
    # parser.add_argument(
    #     "--filter",
    #     type=list,
    #     default=[],
    # )
    # parser.add_argument(
    #     "--stopword",
    #     type=bool,
    #     default=True,
    # )
    TEXT, unparsed = parser.parse_known_args()
    result = analyse(TEXT.text)
    # print([ for x in result ])
    print([(x.value, x.is_stop_word, x.part_of_speech) for x in result])

