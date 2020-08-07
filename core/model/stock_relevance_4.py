import os

from core.util.get_rule_feature import get_stock_feature

base_dir = os.path.dirname(os.path.abspath(__file__))

def rule_score(title, content):
    stock_feature = get_stock_feature(title,content)
    for stock, feature in stock_feature.items():
        symbol_number = feature.split("|")[0].split(":")[1]
        stock_number_count = feature.split("|")[1].split(":")[1]
        other_stock_count = feature.split("|")[2].split(":")[1]
        stock_all_count_rate = feature.split("|")[3].split(":")[1]
        status_industry = feature.split("|")[4].split(":")[1]
        # if symbol_number == 3 and
        pass



    print (stock_feature)



if __name__ == '__main__':
    print ("hello get_stock_feature !")
    title = "成本持续下降+渠道快速扩张”，中顺洁柔悄然穿越牛熊，  "
    content = "b站自己造的星$Facebook$$中顺洁柔(SZ002511)$中顺洁柔(sz002511)发布2019年一季报，符合预期，近期木浆价格下行弹性显现，盈利水平环比显著回暖。产品结构不断优化，渠道布局持续扩张，全国性产能布局持续进行，业绩高增长可期。广发轻工赵中平认为产品渠道双轮驱动构筑公司核心竞争力，高毛利产品占比提升调整产品结构，各生产基地产能投产计划打开增长瓶颈。公司未来渠道扩张优势及新品研发核心壁垒有望持续助力公司业绩增长"
    rule_score(title,content)
