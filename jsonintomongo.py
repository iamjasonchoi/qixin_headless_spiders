#!/usr/bin/env python
#-*- coding: utf8 -*-

import pymysql
import json

datalist = []
# python 列表
with open('result.json','r') as f:
    for line in f: # 读取json文件中的行（也就是json的object）　　　
        datalist.append(json.loads(line)) # 将json的object转成 Python的dict，追加到Python 列表中, 结果都是unicode格式：[{},{},{},{},{}]
for dict in datalist:
    print dict # 打印显示 转换后的结果

for dict in datalist:
    #dict[u'legal_owner'] = dict[u'legal_owner'].replace('\r\n','\\r\\n').replace("'s","\\'s")  # 将字段中的特殊：回车换行以及's 转换，方便形成sql语句
    #sql = "insert into my_com.qixinbao (company,legal_owner,status,capital,creatdate) values('%s','%s','%s','%s','%s');" % (dict[u'company'],dict[u'legal_owner'],dict[u'status'],dict[u'capital'],dict[u'creatdate'])
    sql = "insert into my_com.qixinbao (company,legal_owner,status,capital,creatdate) values('%s','%s','%s','%s','%s');" % (
    dict[u'company'], dict[u'legal_owner'], dict[u'status'], dict[u'capital'], dict[u'creatdate'])
    print sql