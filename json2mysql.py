#-*- coding: utf8 -*-
import json
import pymysql
import demjson

# 读取review数据，并写入数据库
# 导入数据库成功，总共4736897条记录

def reviewdata_insert(db):

    with open('result.json', 'r') as f:
        i = 0
        while True:
            i += 1
            print(u'正在载入第%s行......' % i)
            try:
                lines = f.readline()  # 使用逐行读取的方法
                review_text = json.loads(lines)  # 解析每一行数据
                #new2json = demjson.encode(review_text)
                newjson = json.dumps(review_text, ensure_ascii=False)

                result = []
                result.append((newjson['company'], newjson['legal_owner'],newjson['status'],newjson['capital'], newjson['date']))
                print(result)

                inesrt_re = "insert into my_com.qixinbao (company,legal_owner,status,capital,creatdate)  values (%s, %s, %s, %s,%s)"
                cursor = db.cursor()
                cursor.executemany(inesrt_re, result)
                db.commit()
            except Exception as e:
                db.rollback()
                print(str(e))
                break


if __name__ == "__main__":  # 起到一个初始化或者调用函数的作用
    db = pymysql.connect("localhost", "root", "qaz,./123!", "my_com", charset='utf8')
    cursor = db.cursor()
    #prem(db)
    reviewdata_insert(db)
    cursor.close()