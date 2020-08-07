# -*- coding: utf-8 -*-
# @Time    : 2020/7/9 11:17
# @Author  : supinyu
# @File    : get_log_data.py
import math
import re
import time
import json
import os

from core.util.data_clean import DataClean
from core.config import DATA_DIR

cleaner = DataClean()


def trans_time(now_time):
    temp = now_time
    time_array = time.localtime(int(temp) / 1000)
    return time.strftime("%Y-%m-%d %H:%M:%S", time_array)


def get_recall_online_log(moment, recall_range, symbol_list, log_file, type):
    """
    召回离线的数据，
    :param moment: str, 具体的时间，"%Y-%m-%d %H:%M:%S"
    :param recall_range: int, 回溯的天数，5
    :param symbol_list: list, 股票的list
    :param log_file: str, log文件的名称
    :return:
    """

    online_data_path = os.path.join(DATA_DIR, log_file)

    def trans_format(
            time_string,
            from_format,
            to_format='%Y-%m-%d %H:%M:%S'):
        time_struct = time.strptime(time_string, from_format)
        times = time.strftime(to_format, time_struct)
        times = time.mktime(
            time.strptime(
                times,
                "%Y-%m-%d %H:%M:%S")) * 1000
        return times

    reflact = {
        "公告": "公告",
        "研报": "公告",
        "新闻": "自选股新闻",
        "自选股": "自选股新闻",
        "雪球": "股票微博",
        "Android": "股票微博",
        "iPad": "股票微博",
        "iPhone": "股票微博"
    }

    res = {}
    for symbol in symbol_list:
        res[symbol] = []

    end_moment = time.mktime(
        time.strptime(
            moment,
            "%Y-%m-%d %H:%M:%S")) * 1000
    start_moment = end_moment - recall_range * 24 * 3600 * 1000
    fr = open(online_data_path)
    #    next(fr)
    for line in fr:
        line = line.strip()
        if len(line) == 0:
            continue
        json_data = json.loads(line)
        status_id = json_data["id"]
        created_at = trans_format(
            json_data["created_at"],
            "%a %b %d %H:%M:%S +0800 %Y")
        source = json_data["source"]
        if source in reflact:
            source = reflact[source]

        symbol_set = set()
        if json_data["symbol_id"]:
            symbol_set.add(json_data["symbol_id"])

        for sb in json_data["stockCorrelation"].strip().split("_"):
            its = sb.strip().split(":")
            if len(its) == 2:
                if float(sb.split(":")[1]) > 0:
                    symbol_set.add(sb.split(":")[0])
        title = json_data["title"]
        text = json_data["text"]
        url = json_data["target"]
        description = json_data["description"]

        if start_moment < created_at < end_moment:
            text = cleaner.clean_text(text)
            title = cleaner.clean_text(title)
            symbol_regex = r'\$(.*?)\$'
            symbol_pattern = re.compile(symbol_regex, re.S)
            replace_text = re.sub(symbol_pattern, "", text)
            if type == "short":
                if 50 > len(replace_text) or len(replace_text) > 200:
                    continue
            elif type == "long":
                if len(replace_text) <= 200:
                    continue
            elif type == "supershort":
                if len(replace_text) > 50:
                    continue
            #            description = cleaner.clean_text(description)
            #            keyword_nlp = json_data["keyword"]
            temp_data = {
                "status_id": status_id,
                "created_at": trans_time(created_at),
                "source": source,
                "symbol_set": symbol_set,
                "symbol_id": json_data["symbol_id"],
                #                "keyword_nlp": keyword_nlp,
                "title": title,
                "text": text,
                #                "description": description,
                "url": url}
            for symbol in symbol_set:
                if symbol in res:
                    res[symbol].append(temp_data)
    return res


def chunks(arr, m):
    """
    将arr list 数据等分成m份
    :param arr:
    :param m:
    :return:
    """
    n = int(math.ceil(len(arr) / float(m)))
    return [arr[i:i + n] for i in range(0, len(arr), n)]


if __name__ == "__main__":
    moment = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # moment = "2020-02-26 00:00:00"
    stock_recall_now = get_recall_online_log(moment, 30, ["01810", '00700'], "task_log", "short")
    print(stock_recall_now)
    print(len(stock_recall_now["01810"]))
    print(len(stock_recall_now["00700"]))
