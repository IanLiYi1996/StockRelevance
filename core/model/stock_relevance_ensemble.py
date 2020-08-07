# -*- coding: utf-8 -*-
# @Time    : 2020/7/9 19:47
# @Author  : supinyu
# @File    : stock_relevance_ensemble.py
import json
import time
import os
import math
from multiprocessing import Process
from core.config import RESULT_DIR
from core.model.stock_relevance_1 import scores_v1
from core.model.stock_relevance_2 import scores_v2
from core.util.get_log_data import get_recall_online_log, chunks


class MultiStockRelevance(Process):
    """
    多进程处理文件
    """

    def __init__(self, data_list):
        super(MultiStockRelevance, self).__init__()
        self.data_list = data_list
        self.now_time = time.strftime("%Y-%m-%d", time.localtime())
        self.result_file = os.path.join(RESULT_DIR, self.now_time)

    def run(self):
        with open(self.result_file, "a+") as f:
            for item in self.data_list:
                line_dict = {}
                title = item["title"]
                text = item["text"]
                result_v1 = scores_v1(title, text)
                result_v2 = scores_v2(title, text)
                line_dict["title"] = item["title"]
                line_dict["text"] = item["text"]
                line_dict["status_id"] = item["status_id"]
                line_dict["url"] = item['url']
                line_dict["result_v1"] = result_v1
                line_dict["result_v2"] = result_v2
                f.write(json.dumps(line_dict, ensure_ascii=False) + "\n")


def multi_voter(result_file, voter_file):
    voter_file_data = open(voter_file, "w")
    with open(result_file, "r") as f:
        for line in f:
            line_data = json.loads(line)
            result_v1 = line_data["result_v1"]
            result_v2 = line_data["result_v2"]
            total_symbol = []
            total_symbol.extend(result_v1.keys())
            total_symbol.extend(result_v2.keys())
            volter_restlt = {}

            for each_symbol in set(total_symbol):
                volter_restlt[each_symbol] = {}
                voter1 = result_v1.get(each_symbol, 0)
                voter2 = result_v2.get(each_symbol, 0)
                volter_restlt[each_symbol]["voter_score"] = []
                volter_restlt[each_symbol]["voter_score"].append(voter1)
                volter_restlt[each_symbol]["voter_score"].append(voter2)
                if voter1 == voter2:
                    volter_restlt[each_symbol]["flag"] = True
                else:
                    volter_restlt[each_symbol]["flag"] = False
            line_data["voter_result"] = volter_restlt
            voter_file_data.write(json.dumps(line_data, ensure_ascii=False) + "\n")
    voter_file_data.close()


def run_ensemble(moment, day, symbo_list, log_file, core_num, type):
    stock_recall_log = get_recall_online_log(moment, day, symbo_list, log_file, type)
    multi_num = core_num
    for item in symbo_list:
        process_list = []
        item_data = stock_recall_log[item]
        data_len = len(item_data)
        if data_len > multi_num:
            split_data_list = chunks(item_data, multi_num)
            for i in range(len(split_data_list)):
                p = MultiStockRelevance(split_data_list[i])  # 实例化进程对象
                p.start()
                process_list.append(p)
        else:
            p = MultiStockRelevance(item_data)
            p.start()
            process_list.append(p)
        for j in process_list:
            j.join()
    result_file_path = os.path.join(RESULT_DIR, time.strftime("%Y-%m-%d", time.localtime()))
    voter_file_path = os.path.join(RESULT_DIR, time.strftime("%Y-%m-%d", time.localtime()) + ".voter")
    multi_voter(result_file_path, voter_file_path)


if __name__ == "__main__":
    moment = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    day = 30
    symbol_list = ["01810", '00700']
    task_log = "task_log"
    run_ensemble(moment, day, symbol_list, task_log, 3, "long")