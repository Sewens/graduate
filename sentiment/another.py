#coding:utf-8
import re
import os
import MySQLdb
import SentimentAnalyzer

def sql_insert(fname='kaifulee'):
    create_query = "create table %s (id varchar(64) primary key,time varchar(64),cnt text)" %fname
    connection = MySQLdb.connect(host='localhost',user='root',passwd='root',db='test1',charset='utf8')
    cursor = connection.cursor()
    try :
        cursor.execute(create_query)
    except Exception,e:
        pass
    finally:
        pass

    insert_query = "insert into %s values('asdf','2012-12-32 12:32:51','今天是个好天气')"%fname
    cursor.execute(insert_query)
    connection.commit()
    connection.close()

print('hello')