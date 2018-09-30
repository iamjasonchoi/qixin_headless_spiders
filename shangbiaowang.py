# encoding=UTF-8
import requests
import logging
import time
import json
import pymysql
import os

log_name = 'sb_spider_log.log'
logging.basicConfig(  # 日志输出信息
    filename=log_name,
    filemode='a',
    level=logging.INFO,
    datefmt='%Y-%m-%d %A %H:%M:%S')
db = pymysql.connect(  # 数据库信息
    "127.0.0.1",  # 数据库地址
    "root",  # 数据库用户名
    "root",  # 数据库密码
    "brand",  # 数据库名称
    charset='utf8')  # 编码   utf8    不是utf-8


def get_proxy():  # 获取代理   我这里是动态代理ip    隐藏隐私信息了.
    manager_host = ''
    manager_port =''
    order = ''
    while True:
        url = 'http://%s:%d/get-proxy-api' % (manager_host, manager_port)
        params = {'order': order}
        res = requests.get(url, params=params)
        if res.status_code == 200 and res.text != '{}':
            proxy_config = json.loads(res.text)
            proxy_port = proxy_config['proxy']
            proxy = {'http': f'{proxy_port}'}
            break
        else:
            time.sleep(1)
            print(u'暂无可用代理')
    return proxy  # 返回 代理IP


def post_dg(url, data):  # main_spider
    session = requests.session()  # 日常保险session
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Referer': 'http://sbgg.saic.gov.cn:9080/tmann/annInfoView/annSearch.html?annNum=1605',
        'Host': 'sbgg.saic.gov.cn:9080',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Origin': 'http://sbgg.saic.gov.cn:9080'}  # 构造请求头
    proxies = get_proxy()
    res = session.post(url, headers=headers, data=data, proxies=proxies)  # 加入参数
    res.encoding = 'utf8'
    if res.status_code == 200 and res.text != '{}':  # 判断页面是否有数据
        logging.info('Page crawling succeeded')
        print('页面抓取成功')
        return res.text  # 成功返回数据
    else:

        print('页面无内容')
    if '出错啦！' or 'ERROR' in res.text:
        print('IP被封,页面ERROR')
        logging.info('IP is blocked, Page is ERROR')


def save_to_mysql(url, data):  # 储存到mysql
    html = post_dg(url, data)
    item = json.loads(html)
    for x in range(20):
        list = item['rows'][x]
        ROWstr = ''
        for key in list.keys():
            ROWstr = (ROWstr + '"%s"' + ',') % (list[key])
        sql = f'''INSERT INTO `brand`.`review` (page_no, tm_name, ann_type_code, tmname, reg_name, ann_type, ann_num, reg_num,id,rn,ann_date,regname)  VALUES ({ROWstr[:-1]}) '''
        cur = db.cursor()
        cur.execute(sql)
        db.commit()


def main(i=1):
    url = 'http://sbgg.saic.gov.cn:9080/tmann/annInfoView/annSearchDG.html'
    try:
        while True:
            data = {  # post数据   当前爬取1605页
                'page': f'{i}',
                'rows': '20',
                'annNum': '1605',
                'totalYOrN': 'true',
            }
            save_to_mysql(url, data)
            logging.info(
                f'Page {i} page 20 data successfully written to the database')
            logging.info('``' * 30)
            i += 1
    except BaseException:
        with open('i.txt', 'w') as f:  # 创建文件夹保存断点处的网址ID
            f.write(str(i))
        print('本次爬取中断，中断原因可能为IP被封，现在为您切换Uers-Agent与IP。您也可以手动结束本程序，下次启动时将会从中断处的网址继续爬取。')
        logging.info('Replace the agent..........')
        proxies = get_proxy()  # 随机更换一个代理
        print('本次使用代理为：' + str(proxies))
        logging.info(
            'After the agent is replaced, the agent is' +
            str(proxies))
        main(i)


if __name__ == '__main__':

    if 'i.txt' in os.listdir(
            '.'):  # 在当前文件夹下寻找i.txt文件，如果有的话，读取里面的值，接着上次发生中断的网址继续爬取
        with open('i.txt', 'r') as f:
            i = int(f.read())
            main(i)
    else:  # 如果没有，那么默认从第一个网址开始
        main()