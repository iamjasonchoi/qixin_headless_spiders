# encoding=UTF-8
from qixin_rules import *


def parse_list(req):
    result = []
    for element in req.xpath(LIST_XPATH['list']):
        result.append({
            'title': element.xpath(LIST_XPATH['title']).extract_first().strip(),
            'legal_owner': element.xpath(LIST_XPATH['legal_owner']).re_first(r'法定代表人：(\w*)').strip(),
            'status': element.xpath(LIST_XPATH['status']).extract_first().strip(),
            'capital': element.xpath(LIST_XPATH['capital']).extract_first().strip(),
            'date': element.xpath(LIST_XPATH['date']).extract_first().strip(),
            'url': element.xpath(LIST_XPATH['url']).extract_first().strip()
        })
    return result


def process_search_condition(self):
        """
        构建搜索条件
        * URL: http://www.qixin.com/search?
        * param 地区: area.province=12, area.district=120101-120119
        * param 搜索范围: scope[]=1
        * param 排序: sorter=3 | 4
        * param 注册资本: capital: 1-5
        * param 所属行业: industry.l1 一级行业, industry.l2 二级行业
        * param 注册年份: year: 1-5
        * param page: 页码,最大不超过500, 只能看5000条搜索结果
        http://www.qixin.com/search?area.district=120101&area.province=12&capital=2&industry.l1=%E5%86%9C%E3%80%81%E6%9E%97%E3%80%81%E7%89%A7%E3%80%81%E6%B8%94%E4%B8%9A&industry.l2=%E5%86%9C%E4%B8%9A&page=1&scope[]=1&sorter=4&year=5
        """
        pass
