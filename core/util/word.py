# -*- coding: utf-8 -*-
# @Time    : 2020/7/9 10:36
# @Author  : supinyu
# @File    : word.py

class word(object):
    value = ""
    start = 0
    end = 0
    is_stop_word = False
    part_of_speech = ""
    ner = ""
    keyword_score = 0

    def __init__(self, value, start, end):
        self.value = value
        self.start = start
        self.end = end

    def to_json(self):
        return {
            "value": self.value,
            "start": self.start,
            "end": self.end,
            "is_stop_word": self.is_stop_word,
            "part_of_speech": self.part_of_speech,
            "ner": self.ner,
            "keyword_score": self.keyword_score
        }
