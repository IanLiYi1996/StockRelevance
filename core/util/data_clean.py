# -*- coding: utf-8 -*-
# @Time    : 2020/7/9 11:06
# @Author  : supinyu
# @File    : data_clean.py

# -*- coding: utf-8 -*-
# @Time    : 2019-11-19 19:47
# @Author  : wangjianfeng
# @File    : data_clean.py

"""
数据的清洗流程，包括去除html标签，繁体转简体，全角转半角, 大写转小写等
"""

from zhconv import convert

from lxml import etree


class DataClean(object):
    """
    来的原始数据都要经过这里进行处理
    """

    @staticmethod
    def fullwidth_to_halfwidth(ustring):
        """
        全角转半角
        :param ustring: string
        :return: string
        """
        rstring = ""
        for uchar in ustring:
            inside_code = ord(uchar)
            if inside_code == 12288:  # 全角空格直接转换
                inside_code = 32
            elif 65281 <= inside_code <= 65374:  # 全角字符（除空格）根据关系转化
                inside_code -= 65248
            rstring += chr(inside_code)
        return rstring

    def clean_text(self, text):
        """
        清洗入口
        :param text: string
        :return: string
        """
        if not text:
            return ""
        if not isinstance(text, str):
            text = str(text)
        if not text.strip():
            return ""
        clean_html = etree.HTML(text=text).xpath('string(.)')
        simplified_text = convert(clean_html, "zh-cn")
        return self.fullwidth_to_halfwidth(simplified_text).lower()


if __name__ == '__main__':
    cleaner = DataClean()
    a = """
    <p>$IGG(00799)$&nbsp;新力金融《王国纪元》手游近日在美国市场畅销排名已经大幅回升！</p><img src="#{yu.upload.image.domain}/16dd34e23aa27cdb3fda6095.png!custom.jpg" class="ke_img" ><p><br/></p><img src="#{yu.upload.image.domain}/16dd34e5f7027d803fd49f8c.jpg!custom.jpg" class="ke_img" ><p>$IGG(00799)$&nbsp;</p>
    """
    b = """
    <p><b>大公報</b><b></b></p><p>B05  -     經濟  -     板塊尋寶  -     By 贊華  -   2019-10-16</p><p><b><i>華人策略</i></b><b>轉攻</b><b>AI</b><b>業務</b></p><p>華 人 策 略 （08089）近年業績乏善可陳，必須轉型尋求生機，早前公布擬引入北京專注人工智能（AI）業務的科技公司，透過大數據為企業提供質優價廉的信用服務，擴大收益來源，現價值得收集。</p><p><b><i>華人策略</i></b>全資附屬必進投資及承教投資諮詢（深圳）與北京華鼎匯金投資訂立戰略合作框架協定，在全球戰略性發展及推廣現時由北京藍海科技所經營的AI業務。</p><p>根據協議，在必進能於今年第四季度確保取得7800名收費用戶及於明年取得7.3萬名收費用戶為前提下，華鼎匯金將促使藍海科技與必進訂立獨家代理協定，以換取必進25%股權。</p><p>華鼎匯金旗下藍海科技主要從事設計、開發、轉讓、創新及管理AI科技和提供AI諮詢服務，華鼎匯金是其主要股東。而根據網站資料，藍海科技是透過金准數據的平台進行相關業務。</p><p>目前，金准擁有數百項專利，包括 「基於AI的企業匹配方法」 、 「基於AI的企業搜索系統」 ，以及 「企業動態大數據深度學習和智能評估」 ，因此可利用強大的搜索能力，將企業的 「信用和信譽」 數量化、價值化，從而提供信用服務。</p><p>在金准的商業模式下，搜尋引擎的價值將從篩選資訊變成直接獲取最有價值的商業資訊，企業的行銷推廣商業成本將因此大大降低，從而贏得更多的商業發展機會。目前金准數據已完成79萬企業註冊、18萬企業付費。</p><p>                                                                              </p><p><b><i>華人策略</i></b>能透過利用藍海科技的現有資源及專業知識，以最小的風險高效且具成本效益地涉足AI業務，潛力不容忽視。</p><img src="#{yu.upload.image.domain}/16dd266fda0276b13fbe0585.jpg!custom.jpg" class="ke_img" >"""
    print(cleaner.clean_text(a))