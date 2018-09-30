# encoding=UTF-8
"""
启信宝REQUESTIUM的DRIVER
"""
import time
import random
import ujson
import os
import hashlib
from requestium import Session, Keys
from qixin_rules import *
from qixin_parser import *


USERNAME = ''
PASSWORD = ''
FILENAME = 'category_mapping.json'
# 搜索条件常量
AREA_DISTRICTS = [str(x) for x in range(120101, 120120)]
CAPITALS = [str(x) for x in range(1, 6)]
YEARS = [str(x) for x in range(1, 6)]


def sign():
    secret = ''
    order_no = ''
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
        # self.category_mapping = None

        # path = os.path.join(os.getcwd(), FILENAME)
        # if os.path.exists(path):
        #     self.category_mapping = ujson.load(open(path))
        #     pprint(self.category_mapping)

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
        user_element = self.s.driver.ensure_element_by_xpath(LOGIN_XPATH['username'])
        for c in USERNAME:
            # 间歇输入Username和Password
            user_element.send_keys(c)
            time.sleep(random.randint(0, 2))

        password_element = self.s.driver.ensure_element_by_xpath(LOGIN_XPATH['password'])
        for c in PASSWORD:
            password_element.send_keys(c)
            time.sleep(random.random())
        password_element.send_keys(Keys.ENTER)
        self.s.driver.implicitly_wait(20)

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
            for element in req.xpath(CATEGORY_XPATH['info']):
                category_l1 = element.xpath(CATEGORY_XPATH['l1']).extract_first().strip()
                category_l2 = element.xpath(CATEGORY_XPATH['l2']).extract()
                self.category_mapping[category_l1] = category_l2
                ujson.dump(self.category_mapping, open(os.path.join(os.getcwd(), FILENAME), 'w'))

    def fetch_page_with_chrome(self, url):
        self.s.transfer_session_cookies_to_driver()
        self.s.driver.get(url)

    def fetch_page_with_requests(self, url):
        """
        url = 'http://www.qixin.com/search?area.province=12&page=%s&scope[]=1&sorter=4' % page
        :param url:请求的URL
        :param return: 返回list
        """
        # 获取cookies之后,使用requests的session开始抓取数据
        self.s.proxies.update({
            'http': 'http://forward.xdaili.cn:80',
            'https': 'https://forward.xdaili.cn:80'
        })
        self.s.headers.update({'Proxy-Authorization': sign()})
        req = self.s.get(url)
        result = parse_list(req)
        return result


if __name__ == "__main__":
    driver = Driver()
    driver.login()
    driver.process_cookies()
    result = driver.fetch_page()
    # # pprint(result)
    ujson.dump(result, open('result.json', 'w'))

    driver.close()
