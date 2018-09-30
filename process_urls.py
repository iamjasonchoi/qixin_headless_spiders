# encoding=UTF-8
import ujson
import urllib.parse
from pprint import pprint


AREA_DISTRICTS = [str(x) for x in range(120101, 120120)]
CAPITALS = [str(x) for x in range(1, 6)]
YEARS = [str(x) for x in range(1, 6)]
SORTERS = [3, 4]
VARIABLE = {
    'area.district': 'AREA_DISTRICTS',
    'capital': 'CAPITALS',
    'year': 'YEARS',
    'sorter': 'SORTERS'
}
BASE = 'http://www.qixin.com/search?'


def process(url):
    query_tuple = parse_qsl(url.split('?')[1])
    query_dict = {}
    variable_key = None
    result = []
    for key, value in query_tuple:
        if '-' not in value:
            query_dict[key] = value
        else:
            variable_key = key
            query_dict[key] = value

    for d in eval(VARIABLE[variable_key]):
        query_dict[variable_key] = d
        result.append(BASE + urlencode(query_dict))
    return result


if __name__ == '__main__':
    result = []
    urls = open('concat_urls.txt').readlines()
    to_process_urls = open('urls.txt').readlines()
    for url in to_process_urls:
        tmp = process(url)
        for u in tmp:
            urls.append(u)
    print(len(urls))
    ujson.dump(urls, open('urls.json', 'w'))
    
    urls = [
        'http://www.qixin.com/search?area.district=120101-120119&area.province=12&capital=1-5&industry.l1=%E4%BD%8F%E5%AE%BF%E5%92%8C%E9%A4%90%E9%A5%AE%E4%B8%9A&industry.l2=%E9%A4%90%E9%A5%AE%E4%B8%9A&page=1&scope%5B%5D=1&sorter=3-4&year=1-5',
        'http://www.qixin.com/search?area.district=120101-120119&area.province=12&capital=1-5&industry.l1=%E6%89%B9%E5%8F%91%E5%92%8C%E9%9B%B6%E5%94%AE%E4%B8%9A&industry.l2=%E6%89%B9%E5%8F%91%E4%B8%9A&page=1&scope%5B%5D=1&sorter=3-4&year=1-5',
        'http://www.qixin.com/search?area.district=120101-120119&area.province=12&capital=1-5&industry.l1=%E6%89%B9%E5%8F%91%E5%92%8C%E9%9B%B6%E5%94%AE%E4%B8%9A&industry.l2=%E9%9B%B6%E5%94%AE%E4%B8%9A&page=1&scope%5B%5D=1&sorter=3-4&year=1-5'
    ]
    result = []
    for url in urls:
        tmp1 = process(url)
        for u1 in tmp1:
            tmp2 = process(u1)
            for u2 in tmp2:
                tmp3 = process(u2)
                for u3 in tmp3:
                    tmp4 = process(u3)
                    for u4 in tmp4:
                        result.append(u4)
    pprint(len(result))
    original = ujson.load(open('urls.json'))
    for url in result:
        original.append(url)
    ujson.dump(original, open('urls.json', 'w'))
