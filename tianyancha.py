# encoding=UTF-8

import sys
print sys.getdefaultencoding()

import time

from requests import cookies
from selenium import webdriver
from selenium.webdriver import Firefox


class GetCompanyInfo(object):
    """
    爬取天眼查下的企业的信息
    """
    def __init__(self):
        """
        初始化爬虫执行代理，使用firefox访问
        """
        self.username = ''
        self.password = ''
        self.options = webdriver.FirefoxOptions()
        self.options.add_argument('-headless')  # 无头参数
        self.geckodriver = r'geckodriver'
        self.driver = Firefox(executable_path=self.geckodriver, firefox_options=self.options)

        self.start_url = 'https://www.tianyancha.com'

    def test(self):
        """
        调试专用
        :return:
        """
        start_url = ''
        self.driver.get(start_url)

        for k, v in cookies.items():
            self.driver.add_cookie({
                'name': k,
                'value': v
            })
        time.sleep(1)
        print(self.driver.page_source)
        self.driver.close()

    def login(self):
        """
        登录并检查状态
        :return:
        """
        try:
            self.driver.get(self.start_url)

            print(self.driver.get_cookies())

            username = self.index_login()
            username_pattern = username[:3] + ' **** ' + username[-4:]
            print(username_pattern)
            page = self.driver.page_source
            is_login = page.find(username_pattern)

            print(is_login)
            if is_login != -1:
                print('登录成功')
        except Exception as e:
            print(e)

    def index_login(self):
        """
        主页下的登录模式
        :return:
        """
        get_login = self.driver.find_elements_by_xpath('//a[@class="media_port"]')[0]   # 登录/注册
        print(get_login.text)
        # url为login的input
        get_login.click()
        login_by_pwd = self.driver.find_element_by_xpath('//div[@class="bgContent"]/div[2]/div[2]/div')     # 切换到手机登录
        print(login_by_pwd.text)
        login_by_pwd.click()
        input1 = self.driver.find_element_by_xpath('//div[@class="bgContent"]/div[2]/div/div[2]/input')     # 手机号码

        input2 = self.driver.find_element_by_xpath('//div[@class="bgContent"]/div[2]/div/div[3]/input')     # 密码
        print(input1.get_attribute('placeholder'))
        print(input2.get_attribute('placeholder'))

        username, password = self._check_user_pass()
        input1.send_keys(username)
        input2.send_keys(password)

        login_button = self.driver.find_element_by_xpath('//div[@class="bgContent"]/div[2]/div/div[5]')     # 点击登录
        print(login_button.text)
        time.sleep(1)   # 必须等待否则鉴别是爬虫
        login_button.click()
        return username

    def _check_user_pass(self):
        """
        检查是否有帐号密码
        :return:
        """
        if self.username and self.password:
            return self.username, self.password
        else:
            username = input('输入您的手机号码\n')
            password = input('输入您的密码\n')
            return username, password

    def login_page_login(self):
        """
        url：www.tianyancha.com/login
        在这个url下的登录模式
        :return:
        """
        input1 = self.driver.find_element_by_xpath('//div[contains(@class,"in-block")'
                                                   ' and contains(@class, "vertical-top")'
                                                   ' and contains(@class, "float-right")'
                                                   ' and contains(@class, "right_content")'
                                                   ' and contains(@class, "mt50")'
                                                   ' and contains(@class, "mr5")'
                                                   ' and contains(@class, "mb5")'
                                                   ']/div[2]/div[2]/div[2]/input')

        input2 = self.driver.find_element_by_xpath('//div[contains(@class,"in-block")'
                                                   ' and contains(@class, "vertical-top")'
                                                   ' and contains(@class, "float-right")'
                                                   ' and contains(@class, "right_content")'
                                                   ' and contains(@class, "mt50")'
                                                   ' and contains(@class, "mr5")'
                                                   ' and contains(@class, "mb5")'
                                                   ']/div[2]/div[2]/div[3]/input')
        print(input1.get_attribute('placeholder'))
        input1.send_keys("")
        print(input2.get_attribute('placeholder'))
        input2.send_keys('')

        login_button = self.driver.find_element_by_xpath('//div[contains(@class,"in-block")'
                                                         ' and contains(@class, "vertical-top")'
                                                         ' and contains(@class, "float-right")'
                                                         ' and contains(@class, "right_content")'
                                                         ' and contains(@class, "mt50")'
                                                         ' and contains(@class, "mr5")'
                                                         ' and contains(@class, "mb5")'
                                                         ']/div[2]/div[2]/div[5]')

        print(login_button.text)
        time.sleep(1)
        login_button.click()

    def get_company_info(self, company_name, company_onwer):
        """
        获取想要的公司信息
        :param company_name:
        :param company_onwer:
        :return:
        """
        try:
            time.sleep(1)
            index_input_company = self.driver.find_element_by_xpath('//input[@id="home-main-search"]')  # 主页搜索框

            index_input_company.send_keys(company_name)
            self.driver.find_element_by_xpath('//div[contains(@class, "input-group-addon")'
                                              ' and contains(@class, "search_button")'
                                              ' and contains(@class, " white-btn")'
                                              ']').click()  # 点击搜索
            # button_name = find_company_button.find_element_by_xpath('//span').text    # span中的文本应该为【天眼一下】
            # print(button_name)

            # time.sleep(1)
            company_list = self.driver.find_elements_by_xpath('//div[contains(@class, "b-c-white")'
                                                              ' and contains(@class, "search_result_container")'
                                                              ']/div')  # 获取当前页面所有公司的div
            company_info = list()
            for each_company in company_list:
                company_name_from_web = each_company.find_element_by_tag_name('img').get_attribute('alt')
                company_url = each_company.find_element_by_tag_name('a').get_attribute('href')
                company_reg_money = each_company.\
                    find_element_by_css_selector('div .search_row_new.pt20 div div:nth-child(2) span').text
                company_reg_time = each_company.\
                    find_element_by_css_selector('div .search_row_new.pt20 div div:nth-child(3) span').text
                company_score = each_company.find_element_by_css_selector('.c9.f20').text
                company_info.append([company_name_from_web, company_url, company_reg_money,
                                     company_reg_time, company_score + '分'])   # 获取URL
                print(company_info[-1])

            print('当前匹配公司数：', len(company_info))
            if company_info:
                for each_list in company_info:
                    if each_list[0] == company_name:
                        return '爬取成功： ' + str(each_list)
                        # self.driver.get(each_list[1])     # 进入公司详情页
                        # score = self.driver.find_element_by_class_name('td-score-img').get_attribute('alt')
                        # print(score)
                return '爬取成功'
            else:
                return '爬取失败'
        except Exception as e:
            print(e)

    def main(self):

        self.login()
        msg = self.get_company_info('*****软件有限公司', '')
        print(msg)
        print('crawl finish...')

        self.driver.close()


if __name__ == '__main__':

    # tt = GetCompanyInfo()
    # tt.test()
    time1 = time.time()
    new_crawl = GetCompanyInfo()
    new_crawl.main()
    time2 = time.time()
    print('用时：', int(time2-time1))