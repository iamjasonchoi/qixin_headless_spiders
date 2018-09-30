# encoding=UTF-8
import time
import random
import ujson
import os
import hashlib
from pprint import pprint

from requestium import Session, Keys
# from pprint import pprint


#USERNAME = '17695586823'
#PASSWORD = '900523'
USERNAME = '18622185985'
PASSWORD = 'jazz007'
FILENAME = 'category_mapping.json'
# 搜索条件常量
AREA_DISTRICTS = [str(x) for x in range(120101, 120120)]
CAPITALS = [str(x) for x in range(1, 6)]
YEARS = [str(x) for x in range(1, 6)]


def sign():
    secret = '1d3a17f969724c978a36115ed39bce06'
    order_no = 'ZF201710145848mpry3V'
    timestamp = int(time.time())
    plan_text = 'orderno=%s,secret=%s,timestamp=%s' % (order_no, secret, timestamp)
    md5_string = hashlib.md5(plan_text.encode()).hexdigest().upper()
    sign = 'sign=%s&orderno=%s&timestamp=%s' % (md5_string, order_no, timestamp)
    return sign


class Driver(object):
    def __init__(self):
        # 使用requestium的Session, 使用requests和Selenium, 设置为headless模式
        self.s = Session(
            webdriver_path='./chromedriver',
            browser='chrome',
            default_timeout=15,
            #webdriver_options={'arguments': ['headless']}
        )
        self.category_mapping = None

        path = os.path.join(os.getcwd(), FILENAME)
        if os.path.exists(path):
            self.category_mapping = ujson.load(open(path))
            #pprint(self.category_mapping)

    def close(self):
        if self.s.driver is not None:
            self.s.driver.quit()
        if self.s is not None:
            self.s.close()

    def login(self):
        """
        使用driver登录到启信宝
        """
        login_url = 'http://www.qixin.com/auth/login?return_url=%2F'
        self.s.driver.get(login_url)

        # 使用requestium中的ensure_*方法定位元素
        username_xpath = '//input[@class="form-control input-lg input-flat input-flat-user"]'
        user_element = self.s.driver.ensure_element_by_xpath(username_xpath)
        for c in USERNAME:
            # 间歇输入Username和Password
            user_element.send_keys(c)
            time.sleep(random.randint(0, 2))

        password_xpath = '//input[@class="form-control input-lg input-flat input-flat-lock"]'
        password_element = self.s.driver.ensure_element_by_xpath(password_xpath)
        for c in PASSWORD:
            password_element.send_keys(c)
            time.sleep(random.random())
        password_element.send_keys(Keys.ENTER)
        self.s.driver.implicitly_wait(10)

    def process_cookies(self):
        """
        使用requests抓取页面
        """
        # 将driver的cookies转给requests的session
        tmp_url = 'http://www.qixin.com/search?area.province=12&page=1&scope[]=1'
        self.s.driver.get(tmp_url)
        self.s.transfer_driver_cookies_to_session()
        self.s.copy_user_agent_from_driver()

        # 判断category mapping是否存在
        if self.category_mapping is None:
            req = self.s.get('http://www.qixin.com')
            self.category_mapping = {}
            for element in req.xpath('//div[@class="grid-item"]'):
                category_l1 = element.xpath('./div/text()').extract_first().strip()
                category_l2 = element.xpath('./a/text()').extract()
                self.category_mapping[category_l1] = category_l2
                ujson.dump(self.category_mapping, open(os.path.join(os.getcwd(), FILENAME), 'w'))

    def fetch_page(self):
        # 获取cookies之后,使用requests的session开始抓取数据
        result = []
        self.s.proxies.update({'http': 'http://forward.xdaili.cn:80', 'https': 'https://forward.xdaili.cn:80'})
        for page in range(1, 11):
            url = 'http://www.qixin.com/search?area.province=12&page=%s&scope[]=1&sorter=4' % page
            self.s.headers.update({'Proxy-Authorization': sign()})
            req = self.s.get(url)
            for element in req.xpath("//div[contains(@class, 'company-item')]"):
                result.append({
                    'title': element.xpath(".//div[@class='company-title']/a/text()").extract_first().strip(),
                    'legal_owner': element.xpath(".//div[@class='legal-person'][1]/text()").re_first(r'法定代表人：(\w*)').strip(),
                    'status': element.xpath(".//div[@class='company-tags']/span[1]/text()").extract_first().strip(),
                    'capital': element.xpath(".//div[contains(@class, 'col-3-1')]/text()").extract_first().strip(),
                    'date': element.xpath(".//div[contains(@class, 'col-3-2')]/text()").extract_first().strip(),
                    'url': element.xpath(".//div[@class='company-title']/a/@href").extract_first().strip()
                })
            time.sleep(10)
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


if __name__ == "__main__":
    driver = Driver()
    driver.login()
    driver.process_cookies()
    result = driver.fetch_page()
    #pprint(result)
    ujson.dump(result, open('result.json', 'w'))

    driver.close()

