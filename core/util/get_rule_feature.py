import re
import os
import json
from core.config import DATA_DIR

base_dir = os.path.dirname(os.path.abspath(__file__))
stock_info_dict = json.load(
    open(os.path.join(DATA_DIR, "avaiable_stock_similar_name.json")))
industry_stock_dict = json.load(open(os.path.join(DATA_DIR, "industry_stock_dict.json")))

def get_stock_feature(title, content):
    pattern = re.compile(r'\$(.*?)\$')
    clean_text = re.sub(pattern, "", content)
    stock_max_count = {}
    stock_feature = {}
    for stock_key in self.stock_info_dict.keys():
        for stock, stock_other_list in self.stock_info_dict.items():
            stock_other_name_count = {}
            stock_title_count = 0
            for stock_other_name in stock_other_list:
                if stock_other_name in title:
                    stock_title_count = 2
                stock_other_name_count[stock_other_name] = clean_text.count(stock_other_name)
            max_count = stock_other_name_count[
                            max(stock_other_name_count, key=stock_other_name_count.get)] + stock_title_count
            result_text = pattern.findall(text)
            if max_count > 0:
                stock_max_count[stock] = max_count
        other_stock_count = len(stock_max_count.keys()) - 1
        for industry, stock_list in self.industry_stock_dict.items():
            if stock_key in stock_max_count.keys() and stock_key in stock_list:
                union_stock = list(set(stock_max_count.keys()).intersection(set(stock_list)))
                if len(union_stock) >= 2:
                    status_industry = True
                    break
                else:
                    status_industry = False
        if stock_key in stock_max_count.keys():
            if stock_max_count[stock_key] > 0:
                stock_all_count_rate = (sum(stock_max_count.values()) -
                                        stock_max_count[stock_key]) / stock_max_count[stock_key]
                stock_feature = "$$个数:" + len(match_stock) + "|" + "max_count:" + stock_max_count[stock_key] + "|" + "other_stock_count:" + other_stock_count + "|" + "stock_all_count_rate:" + stock_all_count_rate + "|" + "status_industry:" + status_industry
                stock_feature[stock_key] = stock_feature
    return stock_feature


if __name__ == '__main__':
    print ("hello get_stock_feature !")
    title = "成本持续下降+渠道快速扩张”，中顺洁柔悄然穿越牛熊，  "
    content = "b站自己造的星$Facebook$$中顺洁柔(SZ002511)$中顺洁柔(sz002511)发布2019年一季报，符合预期，近期木浆价格下行弹性显现，盈利水平环比显著回暖。产品结构不断优化，渠道布局持续扩张，全国性产能布局持续进行，业绩高增长可期。广发轻工赵中平认为产品渠道双轮驱动构筑公司核心竞争力，高毛利产品占比提升调整产品结构，各生产基地产能投产计划打开增长瓶颈。公司未来渠道扩张优势及新品研发核心壁垒有望持续助力公司业绩增长"
    get_stock_feature(title,content)