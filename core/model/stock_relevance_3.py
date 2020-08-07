import re
import os
import json
from core.config import DATA_DIR

base_dir = os.path.dirname(os.path.abspath(__file__))
stock_info_dict = json.load(
    open(os.path.join(DATA_DIR, "a_stock_info_dict.json")))
def rule_score_v3(title, content):
    pattern = re.compile(r'\$(.*?)\$')
    clean_text = re.sub(pattern, "", content)
    match_stock_list = pattern.findall(content)
    stock_score = {}
    stock_rule = {}
    for stock, stock_other_list in stock_info_dict.items():
        stock_score[stock] = 0
        stock_other_name_count = {}
        for stock_other_name in stock_other_list:
            if stock_other_name in title:
                stock_score[stock] = stock_score[stock] + 5
            for match_stock in match_stock_list:
                if stock_other_name in match_stock:
                    stock_score[stock] = stock_score[stock] + 1
            stock_other_name_count[stock_other_name] = clean_text.count(stock_other_name)
        max_count = stock_other_name_count[max(stock_other_name_count, key=stock_other_name_count.get)]
        stock_score[stock] = stock_score[stock] + 2 * max_count
    stock_score_v1 = {}
    for stock,score in stock_score.items():
        if score > 0:
            stock_score_v1[stock] = score
    stock_score_sort = sorted(stock_score_v1.items(), key=lambda item:item[1],reverse=True)
    return stock_score_v1



if __name__ == '__main__':
    print ("hello stock_relevance_3")
    title = "成本持续下降+渠道快速扩张”，中顺洁柔悄然穿越牛熊，  "
    content = "b站自己造的星$Facebook$$中顺洁柔(SZ002511)$中顺洁柔(sz002511)发布2019年一季报，符合预期，近期木浆价格下行弹性显现，盈利水平环比显著回暖。产品结构不断优化，渠道布局持续扩张，全国性产能布局持续进行，业绩高增长可期。广发轻工赵中平认为产品渠道双轮驱动构筑公司核心竞争力，高毛利产品占比提升调整产品结构，各生产基地产能投产计划打开增长瓶颈。公司未来渠道扩张优势及新品研发核心壁垒有望持续助力公司业绩增长"
    rule_score(title,content)
