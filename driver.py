# encoding=UTF-8
import time
import random
import ujson
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from parser import parse_list
import hashlib
from lxml import etree


#USERNAME = '13702146441'
#PASSWORD = 'abcd1234'

USERNAME = '18622185985'
PASSWORD = 'jazz007'
def sign():
    secret = '1d3a17f969724c978a36115ed39bce06'
    order_no = 'ZF201710145848mpry3V'
    timestamp = int(time.time())
    plan_text = 'orderno=%s,secret=%s,timestamp=%s' % (order_no, secret, timestamp)
    md5_string = hashlib.md5(plan_text.encode()).hexdigest().upper()
    sign = 'sign=%s&orderno=%s&timestamp=%s' % (md5_string, order_no, timestamp)
    return sign

class Fetcher(object):
    def __init__(self):
        self.driver = None
        self.wait = None

    def __init__driver__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"')
        options.add_argument('accept-language="zh-CN,zh;q=0.9"')
        self.driver = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.driver, 20)

    def close_driver(self):
        if self.driver is not None:
            self.driver.close()

    def open(self, url):
        if self.driver is None:
            self.__init__driver__()
        self.driver.get(url)

    def login(self):
        login_url = 'http://www.qixin.com/auth/login?return_url=%2F'
        self.open(login_url)
        user_element = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@class="form-control input-lg input-flat input-flat-user"]')))
        for c in USERNAME:
            user_element.send_keys(c)
            time.sleep(random.randint(0,2))
        password_element = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@class="form-control input-lg input-flat input-flat-lock"]')))
        for c in PASSWORD:
            password_element.send_keys(c)
            time.sleep(random.random())
        password_element.send_keys(Keys.ENTER)

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


    def get_page(self):
        # 获取cookies之后,使用requests的session开始抓取数据
        result = []

        for page in range(1, 100):
            url = 'http://www.qixin.com/search-prov?area.province=45&area.city=4501&page=%s&sorter=4' % page
            #self.driver.headers.update({'Proxy-Authorization': sign()})
            #req = self.driver.get(url)
            self.driver.get(url)
            source = self.driver.page_source
            html = etree.HTML(source)

            for element in html.xpath("//div[contains(@class, 'company-item')]"):
                result.append({
                    'company': element.xpath(".//div[@class='company-title']/a/text()")[0].strip(),
                    #'tel': element.xpath(".//div[@class='legal-person']/span[@class='margin-r-1x']/text()")[0].strip(),
                    'legal_owner': element.xpath(".//div[@class='legal-person']/text()")[0].strip(),
                    #'address': element.xpath(".//div[@class='legal-person'][1]/span/text()")[0].strip(),
                    'status': element.xpath(".//div[@class='company-tags']/span/text()")[0].strip(),
                    'capital': element.xpath(".//div[contains(@class, 'col-3-1')]/text()")[0].strip(),
                    'date': element.xpath(".//div[contains(@class, 'col-3-2')]/text()")[0].strip()
                    #'url': element.xpath(".//div[@class='company-title']/a/@href")[0].strip()
                })
            time.sleep(10)
        return result


if __name__ == "__main__":
    fetcher = Fetcher()
    fetcher.login()
    time.sleep(5)
    html = fetcher.get_page()

    ujson.dump(html, open('result.json', 'w'))
    fetcher.close_driver()
